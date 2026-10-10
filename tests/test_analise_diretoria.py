"""Testes de regressão de indicadores, filtros, agrupamentos e totais.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import unittest
import pandas as pd
from core.analise import preparar_dados, filtrar_dados, resumo_alunos, resumo_grupos, contar_alunos


def exemplo():
    base=dict(unidade='A',NumeroMatricula='7',Sacado='Alice',Turma='2026/1 - English 4.1',Curso='ENGLISH COURSE',Estagio='English 4',NumeroParcela=1,SemestreReferencia='1º Semestre',DataInicio='2025-11-10',DataVencimento='2020-01-10',ValorComDesconto=100,ValorPago=0,Situacao='Pendente')
    return pd.DataFrame([
        base,
        dict(base,NumeroParcela=2,Situacao='Quitada',ValorPago=100),
        dict(base,NumeroParcela=3,DataVencimento='2099-01-10'),
        dict(base,NumeroParcela=4,Situacao='Cancelada'),
        dict(base,Turma='2026/2 - English 5.1',Estagio='English 5',SemestreReferencia='2º Semestre',NumeroParcela=1,DataVencimento='2099-01-10'),
        dict(base,unidade='B',Sacado='Bia',Curso='KIDS´ COURSE',Turma='2026/1 - Kids 2.1',Estagio='Kids 2',Situacao='Paga',ValorPago=100),
        dict(base,NumeroMatricula='8',Sacado='Carlos',Situacao='Não paga'),
        dict(base,NumeroMatricula='9',Sacado='Ana [N]',Turma=None,DataInicio=None,DataVencimento='2099-01-10')])


class AnaliseTests(unittest.TestCase):
    """Verifica os cenários de Analise usando dados de teste e dependências isoladas."""
    def setUp(self):self.df=preparar_dados(exemplo(),hoje='2026-10-08')
    def test_aluno_com_varias_turmas_contado_uma_vez(self):
        self.assertEqual(contar_alunos(self.df),4)
        resumo=resumo_alunos(self.df)
        self.assertEqual(len(resumo),4)
        alice=resumo.loc[resumo.unidade.eq('A') & resumo.NumeroMatricula.eq('7')].iloc[0]
        self.assertEqual(alice.Parcelas,5)
        self.assertEqual(alice.ParcelasVencidas,1)
        self.assertEqual(alice.StatusAluno,'Inadimplente')
    def test_matriculas_iguais_em_unidades_diferentes(self):
        resumo=resumo_alunos(self.df)
        self.assertEqual(len(resumo.loc[resumo.NumeroMatricula.eq('7')]),2)
        self.assertEqual(resumo.loc[resumo.unidade.eq('B'),'StatusAluno'].iloc[0],'Em dia')
    def test_canceladas_nao_entram_em_divida_ou_previsao(self):
        cancelada=self.df.loc[self.df.Situacao.eq('Cancelada')].iloc[0]
        self.assertFalse(cancelada.IsVencida)
        self.assertEqual(cancelada.ValorPrevisto,0)
        self.assertEqual(cancelada.ValorPendente,0)
    def test_nao_paga_nao_e_identificada_como_paga(self):
        linha=self.df.loc[self.df.Situacao.eq('Não paga')].iloc[0]
        self.assertEqual(linha.SituacaoParcela,'Pendente');self.assertTrue(linha.IsVencida)
    def test_parcela_futura_nao_e_vencida(self):
        futuras=self.df.loc[self.df.DataVencimento.dt.year.eq(2099)]
        self.assertFalse(futuras.IsVencida.any());self.assertTrue(futuras.ValorPendente.gt(0).all())
    def test_filtro_pago_nao_esconde_status_do_aluno(self):
        pagas=filtrar_dados(self.df,SituacaoParcela='Paga')
        resumo=resumo_alunos(pagas,self.df)
        self.assertEqual(resumo.loc[resumo.unidade.eq('A'),'StatusAluno'].iloc[0],'Inadimplente')
    def test_filtros_semestre_curso_ano_combinados(self):
        d=filtrar_dados(self.df,AnoLetivo=2026,SemestreReferencia='2º Semestre',Curso='ENGLISH COURSE')
        self.assertEqual(len(d),1);self.assertEqual(d.iloc[0].Estagio,'English 5')
    def test_busca_literal_e_acentos(self):
        self.assertEqual(len(filtrar_dados(self.df,busca='[N]')),1)
        self.assertEqual(len(filtrar_dados(self.df,busca='alice')),5)
    def test_ano_turma_tem_precedencia_e_ausente_nao_e_inventado(self):
        r=dict(exemplo().iloc[0],DataInicio='2024-01-01')
        self.assertEqual(preparar_dados(pd.DataFrame([r])).AnoLetivo.iloc[0],2026)
        self.assertTrue(pd.isna(self.df.loc[self.df.NumeroMatricula.eq('9'),'AnoLetivo'].iloc[0]))
    def test_agrupamento_conta_alunos_sem_repetir_parcelas(self):
        grupos=resumo_grupos(self.df,['unidade','Turma'])
        primeira=grupos.loc[grupos.unidade.eq('A') & grupos.Turma.eq('2026/1 - English 4.1')].iloc[0]
        self.assertEqual(primeira.Alunos,2);self.assertEqual(primeira.Parcelas,5)
        self.assertAlmostEqual(grupos.Recebido.sum(),self.df.ValorRecebido.sum())
        self.assertAlmostEqual(grupos.Vencido.sum(),self.df.ValorVencido.sum())
    def test_grupo_por_numero_parcela_tambem_funciona(self):
        r=resumo_grupos(self.df,['NumeroParcela']);self.assertEqual(r.Parcelas.sum(),len(self.df))
    def test_base_vazia_preserva_estrutura(self):
        d=preparar_dados(exemplo().iloc[:0]);self.assertTrue(resumo_alunos(d).empty)
        self.assertTrue(resumo_grupos(d,['Turma']).empty)


class NovosEstagiosNaCargaAnteriorTests(unittest.TestCase):
    """Verifica os cenários de NovosEstagiosNaCargaAnterior usando dados de teste e dependências isoladas."""
    def test_estagio_deduzido_sem_exigir_nova_sincronizacao(self):
        r=dict(exemplo().iloc[0],Turma='2026 - English T 2.1',Estagio=None)
        d=preparar_dados(pd.DataFrame([r]))
        self.assertEqual(d.iloc[0].Estagio,'English T 2')


class SeparacaoGruposTests(unittest.TestCase):
    """Verifica os cenários de SeparacaoGrupos usando dados de teste e dependências isoladas."""
    def test_preserva_todas_as_linhas_colunas_e_totais(self):
        from core.analise import separar_grupos
        d=preparar_dados(exemplo())
        partes=list(separar_grupos(d,['Curso']))
        self.assertEqual(len(partes),2)
        reunido=pd.concat([linhas for _,linhas in partes]).sort_index()
        pd.testing.assert_frame_equal(reunido,d)
        for _,linhas in partes:self.assertEqual(linhas.Curso.nunique(),1)
    def test_multiplos_campos_e_grupo_nulo(self):
        from core.analise import separar_grupos
        d=pd.DataFrame({'Curso':['A','A','B',None],'Unidade':['X','Y','X','X'],'Valor':[1,2,3,4]})
        partes=list(separar_grupos(d,['Curso','Unidade']))
        self.assertEqual(len(partes),4)
        self.assertEqual(sum(linhas.Valor.sum() for _,linhas in partes),10)
        self.assertTrue(any(pd.isna(chave[0]) for chave,_ in partes))


class TotaisTabelaTests(unittest.TestCase):
    """Verifica os cenários de TotaisTabela usando dados de teste e dependências isoladas."""
    def test_resumo_nao_soma_alunos_repetidos_entre_turmas(self):
        from core.analise import totais_tabela
        base=preparar_dados(exemplo(),hoje='2026-10-08')
        resumo=resumo_grupos(base,['unidade','Turma'])
        total=totais_tabela(resumo,base,['unidade','Turma'])
        self.assertEqual(total['Alunos'],4)
        self.assertGreater(resumo.Alunos.sum(),total['Alunos'])
        self.assertEqual(total['Devedores'],2)
        self.assertEqual(total['Vencido'],200)
        self.assertEqual(total['Recebido'],200)
        self.assertEqual(total['Pendente'],500)
    def test_totais_separados_por_curso_sem_inflar_valores(self):
        from core.analise import totais_tabela,separar_grupos
        base=preparar_dados(exemplo(),hoje='2026-10-08')
        resumo=resumo_grupos(base,['unidade','Curso','Turma'])
        totais=[totais_tabela(p,base,['unidade','Curso','Turma']) for _,p in separar_grupos(resumo,['Curso'])]
        self.assertEqual(sum(t['Vencido'] for t in totais),200)
        self.assertEqual(sum(t['Recebido'] for t in totais),200)
        self.assertEqual(sum(t['Pendente'] for t in totais),500)
    def test_detalhamento_usa_apenas_linhas_da_tabela(self):
        from core.analise import totais_tabela
        base=preparar_dados(exemplo(),hoje='2026-10-08')
        parte=base.loc[base.IsVencida]
        total=totais_tabela(parte,base)
        self.assertEqual(total['Alunos'],2)
        self.assertEqual(total['Vencido'],200)
        self.assertEqual(total['Recebido'],0)
    def test_filtro_pago_preserva_contagem_de_inadimplentes(self):
        from core.analise import totais_tabela,ALUNO
        base=preparar_dados(exemplo(),hoje='2026-10-08')
        pagas=base.loc[base.IsQuitada]
        total=totais_tabela(resumo_alunos(pagas,base),pagas,ALUNO,base)
        self.assertEqual(total['Devedores'],1)
        self.assertEqual(total['Vencido'],0)
