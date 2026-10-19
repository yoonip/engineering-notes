from pathlib import Path
import datetime
import decimal
import json
import math
import re
import sqlite3
import unittest

def date(value):
    return datetime.datetime.fromisoformat(str(value).replace('/','-'))

class BitOr:
    def __init__(self):self.value=0
    def step(self,value):self.value|=int(value)
    def finalize(self):return self.value

def connection():
    db=sqlite3.connect(':memory:')
    db.create_function('YEAR',1,lambda v:date(v).year if v is not None else None)
    db.create_function('MONTH',1,lambda v:date(v).month if v is not None else None)
    db.create_function('QUARTER',1,lambda v:(date(v).month-1)//3+1 if v is not None else None)
    db.create_function('CONCAT',-1,lambda *values:None if None in values else ''.join(str(v) for v in values))
    db.create_function('DATE_FORMAT',2,lambda v,f:date(v).strftime(f) if v is not None else None)
    db.create_function('DATEDIFF',2,lambda a,b:(date(a).date()-date(b).date()).days)
    db.create_function('FLOOR',1,math.floor)
    db.create_function('REGEXP',2,lambda pattern,text:int(bool(re.search(pattern,text or ''))))
    db.create_aggregate('BIT_OR',1,BitOr)
    return db

def numeric_type(type_):
    return bool(re.search(r'INT|NUMBER|NUMERIC|DECIMAL|FLOAT|DOUBLE',type_,re.I))

def create(db,fixtures):
    for fixture in fixtures:
        names=fixture['columns']
        db.execute('CREATE TABLE '+fixture['name']+' ('+','.join('`'+n+'` '+('NUMERIC' if numeric_type(t) else 'TEXT') for n,t in zip(names,fixture['types']))+')')
        db.executemany('INSERT INTO '+fixture['name']+' VALUES ('+','.join('?' for _ in names)+')',fixture['rows'])

def adapt(query):
    query=re.sub(r'\bLEFT\s*\(\s*([\w.]+)\s*,\s*(\d+)\s*\)',r'SUBSTR(\1,1,\2)',query,flags=re.I)
    # MySQL /는 실수 나눗셈이다. SQLite 정수 나눗셈과 다른 곳만 명시적으로 맞춘다.
    query=re.sub(r'PRICE\s*/\s*10000',r'PRICE/10000.0',query,flags=re.I)
    return query

def normalized(rows):
    def value(x):
        if isinstance(x,str) and re.fullmatch(r'-?\d+(\.\d+)?km',x):
            return str(decimal.Decimal(x[:-2]).normalize())+'km'
        if isinstance(x,float):return round(x,8)
        return x
    return sorted([tuple(value(x) for x in row) for row in rows],key=repr)
HERE=Path(__file__).resolve().parent


class QueryTests(unittest.TestCase):
    def test_query_results(self):
        cases=json.loads((HERE/'test_cases.json').read_text(encoding='utf-8'))
        for case in cases:
            with self.subTest(source=case['source']):
                db=connection()
                create(db,case['fixtures'])
                for name in ('solution.sql','alternative.sql'):
                    actual=db.execute(adapt((HERE/name).read_text(encoding='utf-8'))).fetchall()
                    self.assertEqual(normalized(actual),normalized(case['expected']))
                db.close()


if __name__=='__main__':
    unittest.main()
