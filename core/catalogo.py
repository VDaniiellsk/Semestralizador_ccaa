"""Reconhece cursos e estágios a partir dos nomes das turmas.

As variantes conhecidas são padronizadas sem descartar uma parcela quando
o estágio não pode ser reconhecido. Os padrões mais específicos têm prioridade."""
import re
import unicodedata
import pandas as pd

STAGE_COURSES = {}
def _add(prefix, levels, course):
    """Registra um estágio e seu curso no catálogo de reconhecimento."""
    for level in levels: STAGE_COURSES[f'{prefix}{level}'] = course
_add('BABY ', range(1,7), 'BABY CLASS')
_add('English ', range(4,12), 'ENGLISH COURSE')
_add('English A ', range(1,4), 'ENGLISH COURSE')
STAGE_COURSES['English A C 1-2'] = 'ENGLISH COURSE'
_add('English A VIP ', range(1,4), 'ENGLISH COURSE')
STAGE_COURSES['English A VIP C 1-2'] = 'ENGLISH COURSE'
_add('English I', range(4,12), 'ENGLISH COURSE')
_add('English T ', range(1,4), 'ENGLISH COURSE')
_add('English T I', range(1,4), 'ENGLISH COURSE')
_add('English T VIP ', range(1,4), 'ENGLISH COURSE')
_add('English VIP ', range(4,12), 'ENGLISH COURSE')
_add('Español ', range(1,10), 'ESPAÑOL')
_add('Español VIP ', range(1,10), 'ESPAÑOL')
_add('Kids ', range(1,9), 'KIDS´ COURSE')
_add('Preteen ', range(1,3), 'PRETEEN COURSE')
STAGE_COURSES['TEACHERS'] = "TEACHERS' COURSE"

# Estágios adicionais encontrados nas turmas da base de produção.
for stage in ['English 1', 'English 2', 'English 3', 'English C 1-2', 'English T 9', 'English A 4', 'English T 4']:
    STAGE_COURSES[stage] = 'ENGLISH COURSE'

def _normalizar_nome(value):
    """Uniformiza grafia, acentos e espaços para reconhecer variantes de nomes."""
    if value is None or pd.isna(value): return ''
    text=unicodedata.normalize('NFKD',str(value)).replace('’', "'")
    text=''.join(c for c in text if not unicodedata.combining(c)).casefold()
    text = re.sub(r'\b(?:esptnol|espanhol)\b', 'espanol', text)
    text = re.sub(r'\bengliisah\b', 'english', text)
    return re.sub(r'\bbaby\s+class\b', 'baby', text)

def normalizar_curso(value):
    """Converte nomes conhecidos para o catálogo e preserva cursos desconhecidos."""
    text=_normalizar_nome(value)
    if not text.strip(): return None
    for token,course in [('teacher', "TEACHERS' COURSE"),('preteen','PRETEEN COURSE'),
                         ('kids','KIDS´ COURSE'),('baby','BABY CLASS'),
                         ('espanol','ESPAÑOL'),('english','ENGLISH COURSE')]:
        pattern=r"\bteacher(?:'?s)?\b" if token=='teacher' else r'\b'+token+r'\b'
        if re.search(pattern,text): return course
    return str(value).strip()

def _pattern(stage):
    """Monta o padrão de busca de um estágio respeitando seus limites no nome da turma."""
    tokens=re.findall(r'[a-z]+|\d+|-',_normalizar_nome(stage))
    body=r'\s*'.join(re.escape(t) for t in tokens)
    return re.compile(r'\b'+body+r'(?![a-z0-9]|\s*-\s*\d)')
_PATTERNS=[(_pattern(s),s) for s in sorted(STAGE_COURSES,key=len,reverse=True) if s!='TEACHERS']

def deduzir_estagio(value):
    """Procura um estágio conhecido, priorizando variantes mais específicas."""
    text=_normalizar_nome(value)
    for pattern,stage in _PATTERNS:
        if pattern.search(text): return stage
    if re.search(r"\bteacher(?:'?s)?\b",text): return 'TEACHERS'
    return None

def classificar(df):
    """Atualiza somente as duas classificações, preservando todas as linhas."""
    turma=df['Turma']
    inferred=turma.map(deduzir_estagio)
    reported=df['Estagio'].map(deduzir_estagio) if 'Estagio' in df else pd.Series(None,index=df.index,dtype=object)
    df['Estagio']=inferred.combine_first(reported)
    existing=df['Curso'].map(normalizar_curso) if 'Curso' in df else pd.Series(None,index=df.index,dtype=object)
    missing=existing.isna() | existing.astype(str).str.strip().isin(['','S/I','Não informado'])
    from_turma=turma.map(normalizar_curso)
    from_turma=from_turma.where(from_turma.isin(set(STAGE_COURSES.values())))
    existing=existing.mask(missing,from_turma)
    df['Curso']=df['Estagio'].map(STAGE_COURSES).combine_first(existing).fillna('S/I')
    return df
