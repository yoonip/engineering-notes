"""MySQL 풀이의 관계 결과를 SQLite 호환 환경에서 검사합니다."""
from pathlib import Path
import sqlite3,json,re,datetime,decimal,math

def prepare(connection):
    def date(value):
        return datetime.datetime.fromisoformat(str(value)) if value is not None else None
    def component(value,part):
        parsed=date(value)
        return getattr(parsed,part) if parsed is not None else None
    connection.create_function('CONCAT',-1,lambda *xs:None if None in xs else ''.join(map(str,xs)))
    connection.create_function('CONCAT_WS',-1,lambda sep,*xs:None if sep is None else str(sep).join(str(x) for x in xs if x is not None))
    connection.create_function('MYSQL_LEFT',2,lambda s,n:None if s is None else s[:n])
    connection.create_function('MYSQL_RIGHT',2,lambda s,n:None if s is None else s[-n:] if n else '')
    connection.create_function('MONTH',1,lambda v:component(v,'month'))
    connection.create_function('YEAR',1,lambda v:component(v,'year'))
    connection.create_function('HOUR',1,lambda v:component(v,'hour'))
    connection.create_function('DATE_FORMAT',2,lambda value,fmt:date(value).strftime(fmt) if value is not None else None)
    connection.create_function('DATEDIFF',2,lambda a,b:(date(a).date()-date(b).date()).days)
    connection.create_function('TIMESTAMPDIFF',3,lambda unit,a,b:int((date(b)-date(a)).total_seconds()))
    connection.create_function('FLOOR',1,lambda v:math.floor(v) if v is not None else None)
    connection.create_function('IF',3,lambda test,a,b:a if test else b)
    def mysql_round(value,places=0):
        if value is None:return None
        return float(decimal.Decimal(str(value)).quantize(decimal.Decimal(1).scaleb(-places),rounding=decimal.ROUND_HALF_UP))
    connection.create_function('ROUND',2,mysql_round)

def query(connection,sql):
    # 연산 의미를 보존하는 문법·함수 어댑터입니다. 실제 MySQL 실행은 아닙니다.
    sql=re.sub(r'\bLEFT\s*\(', 'MYSQL_LEFT(',sql,flags=re.I)
    sql=re.sub(r'\bRIGHT\s*\(', 'MYSQL_RIGHT(',sql,flags=re.I)
    sql=re.sub(r'TIMESTAMPDIFF\(\s*SECOND\s*,',"TIMESTAMPDIFF('SECOND',",sql,flags=re.I)
    sql=sql.replace('<=>','IS')
    cursor=connection.execute(sql)
    return [list(row) for row in cursor.fetchall()]

def run():
    root=Path(__file__).parent
    fixtures=json.loads((root/'query_fixtures.json').read_text('utf8'))
    checked=0
    for fixture in fixtures:
        connection=sqlite3.connect(':memory:');prepare(connection)
        for name,table in fixture['tables'].items():
            columns=table['columns'];types=table['types']
            connection.execute('CREATE TABLE "'+name+'" ('+','.join('"'+c+'" '+t for c,t in zip(columns,types))+')')
            if table['rows']:
                connection.executemany('INSERT INTO "'+name+'" VALUES ('+','.join('?' for c in columns)+')',table['rows'])
        actual=[]
        for filename in ('solution.sql','alternative.sql'):
            rows=query(connection,(root/filename).read_text('utf8'))
            if rows!=fixture['expected']:
                raise AssertionError((fixture['name'],filename,rows,fixture['expected']))
            actual.append(rows);checked+=1
        connection.close()
    print(str(checked)+' SQL compatibility checks passed (SQLite '+sqlite3.sqlite_version+')')
    return checked

if __name__=='__main__':run()
