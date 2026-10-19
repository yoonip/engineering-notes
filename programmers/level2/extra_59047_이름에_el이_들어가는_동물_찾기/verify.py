import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
NUMERIC = {'ID', 'PARENT_ID', 'SIZE_OF_COLONY', 'GENOTYPE', 'FISH_TYPE',
           'LENGTH', 'SAL', 'ITEM_ID', 'PARENT_ITEM_ID', 'PRICE'}

def database(tables, schemas):
    connection = sqlite3.connect(':memory:')
    # 날짜·시각 함수 등 MySQL 표현의 결과를 작은 테이블에서 대조한다.
    connection.create_function('DATE_FORMAT', 2, lambda value, fmt: None if value is None else value[:10].replace('/', '-'))
    connection.create_function('DATE', 1, lambda value: None if value is None else value[:10].replace('/', '-'))
    connection.create_function('HOUR', 1, lambda value: None if value is None else int(value.split()[1].split(':')[0]))
    connection.create_function('LOCATE', 2, lambda needle, value: None if value is None or needle is None else value.find(needle) + 1)
    connection.create_function('IF', 3, lambda condition, yes, no: yes if condition else no)
    for name, rows in tables.items():
        columns = schemas[name]
        connection.execute('CREATE TABLE ' + name + '(' + ','.join(column + (' NUMERIC' if column in NUMERIC else ' TEXT') for column in columns) + ')')
        connection.executemany('INSERT INTO ' + name + ' VALUES (' + ','.join('?' for _ in columns) + ')', rows)
    return connection

def canonical(rows):
    return [[str(int(value)) if isinstance(value, float) and value.is_integer()
             else str(value) if value is not None else None for value in row] for row in rows]

def main():
    payload = json.loads((ROOT / 'cases.json').read_text(encoding='utf-8'))
    for case in payload['cases']:
        connection = database(case['tables'], payload['schemas'])
        for filename in ('solution.sql', 'alternative.sql'):
            actual = connection.execute((ROOT / filename).read_text(encoding='utf-8')).fetchall()
            assert canonical(actual) == canonical(case['expected']), (case['label'], filename, actual, case['expected'])
        connection.close()
    print(json.dumps({'problem_id': payload['problem_id'], 'cases_passed': len(payload['cases']),
                      'engine': 'SQLite with compatibility functions'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
