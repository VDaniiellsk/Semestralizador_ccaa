"""Valida e persiste a fotografia financeira no SQLite.

A carga completa substitui a anterior em uma transação. Os valores monetários
são guardados em centavos e a view mantém os nomes esperados pelos painéis."""
import logging
import sqlite3
from contextlib import closing
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import pandas as pd
DB_PATH=Path(__file__).resolve().parents[1]/'data'/'auditoria_relatorios.db'
SCHEMA_PATH=Path(__file__).with_name('schema_relacional.sql')
TABLES=('unidade','aluno','curso','turma','parcela')
REQUIRED=('unidade','NumeroMatricula','NumeroParcela','Sacado','Turma','Curso',
          'TipoContrato','DataInicio','DataVencimento','ValorComDesconto','ValorPago','Situacao','SemestreReferencia')
logger=logging.getLogger('RPA_CCAA')

def _text(value, field, optional=False):
    """Converte um campo textual e trata ausências conforme sua obrigatoriedade."""
    if value is None or pd.isna(value):
        if optional:
            return None
        raise ValueError(f'{field}: valor obrigatório ausente.')
    value = str(value).strip()
    if not value:
        if optional:
            return None
        raise ValueError(f'{field}: valor obrigatório vazio.')
    return value


def _identifier(value, field):
    """Preserva identificadores como texto, evitando transformar matrícula em medida numérica."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value) or not float(value).is_integer():
            raise ValueError(f'{field}: identificador inválido.')
        return str(int(value))
    return _text(value, field)


def _integer(value, field):
    """Aceita somente números inteiros positivos para a sequência de parcelas."""
    try:
        number = Decimal(str(value))
        if isinstance(value, bool) or not number.is_finite() or number != number.to_integral_value() or number <= 0:
            raise ValueError
        return int(number)
    except (ValueError, InvalidOperation):
        raise ValueError(f'{field}: informe um inteiro positivo.') from None


def _date(value, field, optional=False):
    """Converte datas para o formato usado nesta camada e rejeita valores inválidos."""
    if value is None or pd.isna(value):
        if optional:
            return None
        raise ValueError(f'{field}: data obrigatória ausente.')
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    value = str(value).strip()
    if not value and optional:
        return None
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError
        return value
    except ValueError:
        raise ValueError(f'{field}: use uma data válida em AAAA-MM-DD.') from None


def _money(value, field, optional=False):
    """Converte reais em centavos com arredondamento decimal e rejeita valores negativos ou inválidos."""
    if (value is None or pd.isna(value)) and optional:
        return None
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            raise ValueError
        cents = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100
        if isinstance(value, bool) or not cents.is_finite() or cents < 0 or cents != cents.to_integral_value():
            raise ValueError
        if cents > 9223372036854775807:
            raise ValueError
        return int(cents)
    except (ValueError, InvalidOperation):
        raise ValueError(f'{field}: informe um valor monetário válido e não negativo.') from None


def _percentual(value):
    """Converte o percentual estimado em pontos-base; ausência continua sendo ausência."""
    if value is None or pd.isna(value):return None
    try:
        number=Decimal(str(value))
        if isinstance(value,bool) or not number.is_finite() or not 0<=number<=100:raise ValueError
        return int((number*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    except (ValueError,InvalidOperation):raise ValueError('DescontoEstimado inválido.') from None


def validar_lote(df,unidade):
    """Valida os registros da unidade e devolve os campos preparados para persistência.

    Uma falha identifica a linha problemática e interrompe a publicação do lote."""
    missing=sorted(set(REQUIRED)-set(df.columns))
    if missing:
        raise ValueError('Faltam campos do relatório tratado: '+', '.join(missing))
    records=[]
    for position,row in enumerate(df.to_dict('records'),start=1):
        try:
            if _text(row['unidade'],'unidade')!=unidade:
                raise ValueError('Lote contém registros de outra unidade.')
            reference=_text(row['SemestreReferencia'],'SemestreReferencia')
            if reference not in ('1º Semestre','2º Semestre','Não informado'):
                raise ValueError('SemestreReferencia inválido.')
            kind=_text(row['TipoContrato'],'TipoContrato').title()
            if kind.casefold()=='não informado':kind='Não informado'
            if kind not in ('Anual','Semestral','Não informado'):
                raise ValueError('TipoContrato inválido.')
            records.append(dict(unidade=unidade,linha=position,
                matricula=_identifier(row['NumeroMatricula'],'NumeroMatricula'),
                parcela=_integer(row['NumeroParcela'],'NumeroParcela'),
                aluno=_text(row['Sacado'],'Sacado'),
                situacao_aluno=_text(row.get('SituacaoAluno'),'SituacaoAluno',True),
                turma=_text(row['Turma'],'Turma',True),curso=_text(row['Curso'],'Curso'),tipo=kind,
                inicio=_date(row['DataInicio'],'DataInicio',True),termino=_date(row.get('DataTermino'),'DataTermino',True),
                vencimento=_date(row['DataVencimento'],'DataVencimento'),pagamento=_date(row.get('DataPagamento'),'DataPagamento',True),
                desconto=_money(row['ValorComDesconto'],'ValorComDesconto'),pago=_money(row['ValorPago'],'ValorPago'),
                juros=_money(row.get('ValorComJuros'),'ValorComJuros',True),
                situacao=_text(row['Situacao'],'Situacao'),referencia=reference,
                bolsa=_text(row.get('Bolsa'),'Bolsa',True),forma=_text(row.get('FormaCobranca'),'FormaCobranca',True),
                atendente=_text(row.get('NomeAtendente'),'NomeAtendente',True),
                operadora=_text(row.get('NomeOperadoraCartao'),'NomeOperadoraCartao',True),
                estagio=_text(row.get('Estagio'),'Estagio',True),
                estimado=_percentual(row.get('DescontoEstimado')),
                pacote_estimado=_text(row.get('PacoteEstimado'),'PacoteEstimado',True),
                parcelamento_estimado=None if row.get('ParcelamentoEstimado') is None or pd.isna(row.get('ParcelamentoEstimado')) else _integer(row['ParcelamentoEstimado'],'ParcelamentoEstimado'),
                resultado_estimativa=_text(row.get('ResultadoEstimativa'),'ResultadoEstimativa',True),
                fonte_estimativa=_text(row.get('FonteEstimativa'),'FonteEstimativa',True)))
        except (ValueError,TypeError) as exc:
            raise ValueError(f'Linha {position}: {exc}') from None
    return records

def _criar_schema(conn):
    """Executa as instruções do esquema, inclusive a view de compatibilidade."""
    statement=''
    for line in SCHEMA_PATH.read_text(encoding='utf-8').splitlines(keepends=True):
        statement+=line
        if sqlite3.complete_statement(statement):
            conn.execute(statement);statement=''
    if statement.strip():raise ValueError('SQL do esquema incompleto.')


def get_connection(path=None):
    """Abre o SQLite, habilita integridade referencial e prepara ou migra o esquema.

    O chamador deve fechar a conexão quando terminar."""
    path=Path(path or DB_PATH).resolve()
    if path.name.lower() in ('auditoria_financeira.db','auditoria_relacional.db','modelo_teste.db'):
        raise ValueError('Escolha a base de relatórios; bases anteriores permanecem separadas.')
    path.parent.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(path,timeout=30)
    try:
        conn.execute('PRAGMA foreign_keys=ON')
        tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        version=conn.execute('PRAGMA user_version').fetchone()[0]
        if not tables:
            conn.execute('BEGIN IMMEDIATE');_criar_schema(conn)
            conn.execute('PRAGMA user_version=4');conn.commit()
        elif tables!=set(TABLES) or version not in (2,3,4):
            raise ValueError('Esquema não reconhecido; carga anterior preservada.')
        elif version==2:
            # Migra a estrutura e seus registros na mesma transação.
            # Nenhum contrato, turma ou data é inventado para completar campos.
            conn.execute('BEGIN IMMEDIATE')
            units=[r[0] for r in conn.execute('SELECT nome FROM unidade ORDER BY id')]
            previous=pd.read_sql_query('SELECT * FROM recebiveis_auditados',conn)
            records=[r for u in units for r in validar_lote(previous.loc[previous.unidade.eq(u)],u)]
            conn.execute('DROP VIEW recebiveis_auditados')
            for table in reversed(TABLES):conn.execute(f'DROP TABLE {table}')
            _criar_schema(conn);_gravar(conn,records,units)
            if conn.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Falha ao migrar o banco.')
            conn.execute('PRAGMA user_version=4');conn.commit()
        elif version==3:
            # Adiciona somente campos da estimativa, preservando linhas, IDs e valores.
            conn.execute('BEGIN IMMEDIATE')
            for column in ['desconto_estimado_bp INTEGER CHECK(desconto_estimado_bp BETWEEN 0 AND 10000)',
                           'pacote_estimado TEXT','parcelamento_estimado INTEGER CHECK(parcelamento_estimado>0)',
                           'resultado_estimativa TEXT','fonte_estimativa TEXT']:
                conn.execute('ALTER TABLE parcela ADD COLUMN '+column)
            conn.execute('DROP VIEW recebiveis_auditados')
            view=SCHEMA_PATH.read_text(encoding='utf-8').split('CREATE VIEW recebiveis_auditados',1)[1]
            conn.execute('CREATE VIEW recebiveis_auditados'+view)
            conn.execute('PRAGMA user_version=4');conn.commit()
        return conn
    except Exception:
        conn.rollback();conn.close();raise


def _gravar(conn,records,units):
    """Substitui os registros dentro da transação iniciada pelo chamador.

    A ordem de exclusão e inserção respeita as chaves estrangeiras."""
    unit_ids={u:i+1 for i,u in enumerate(sorted(units))}
    course_ids={c:i+1 for i,c in enumerate(sorted({r['curso'] for r in records}))}
    students,classes={},{}
    for r in records:
        uid=unit_ids[r['unidade']]
        students.setdefault((uid,r['matricula']),r['aluno'])
        if r['turma'] is None:continue
        key=(uid,r['turma']);course=course_ids[r['curso']]
        if key in classes and classes[key]!=course:
            raise ValueError('A mesma turma está associada a cursos diferentes na mesma unidade.')
        classes[key]=course
    for table in reversed(TABLES):conn.execute(f'DELETE FROM {table}')
    conn.executemany('INSERT INTO unidade VALUES (?,?)',[(v,k) for k,v in unit_ids.items()])
    conn.executemany('INSERT INTO curso VALUES (?,?)',[(v,k) for k,v in course_ids.items()])
    conn.executemany('INSERT INTO aluno VALUES (?,?,?)',[key+(value,) for key,value in students.items()])
    conn.executemany('INSERT INTO turma VALUES (?,?,?)',[key+(value,) for key,value in classes.items()])
    for number,r in enumerate(records,start=1):
        values=(number,unit_ids[r['unidade']],r['linha'],r['matricula'],r['turma'],r['parcela'],r['aluno'],
                r['situacao_aluno'],r['tipo'],r['inicio'],r['termino'],r['vencimento'],r['pagamento'],
                r['desconto'],r['pago'],r['juros'],r['situacao'],r['referencia'],r['bolsa'],r['forma'],r['atendente'],r['operadora'],course_ids[r['curso']],r['estagio'],r['estimado'],r['pacote_estimado'],
                r['parcelamento_estimado'],r['resultado_estimativa'],r['fonte_estimativa'])
        conn.execute('INSERT INTO parcela VALUES ('+','.join('?' for _ in values)+')',values)

def salvar_carga_completa(lotes,unidades_esperadas,path=None):
    """Valida todas as unidades antes de substituir a fotografia financeira.

    Retorna sucesso e mensagem; falhas de validação ou gravação preservam a carga anterior."""
    try:
        expected=list(unidades_esperadas)
        if not expected or len(set(expected))!=len(expected) or set(lotes)!=set(expected):
            raise ValueError('A carga deve conter todas as unidades esperadas, inclusive as vazias.')
        records=[r for unit in expected for r in validar_lote(lotes[unit],unit)]
        if not records:raise ValueError('Carga inteiramente vazia; confira os filtros. Dados anteriores preservados.')
        with closing(get_connection(path)) as conn,conn:
            conn.execute('BEGIN IMMEDIATE');_gravar(conn,records,expected)
            if conn.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Falha de integridade referencial.')
        return True,f'Carga concluída: {len(records)} registros financeiros em {len(expected)} unidades.'
    except (ValueError,TypeError,sqlite3.Error,OverflowError) as exc:
        logger.error('Carga rejeitada: %s',exc)
        return False,str(exc)

def carregar_dados_auditados(path=None):
    """Lê a view financeira e encerra a conexão após montar o DataFrame."""
    with closing(get_connection(path)) as conn:return pd.read_sql_query('SELECT * FROM recebiveis_auditados',conn)
