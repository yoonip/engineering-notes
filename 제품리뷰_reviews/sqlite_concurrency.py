"""Observe SQLite journal behavior using two connections to a temporary file."""
import json
import platform
import sqlite3
import tempfile
from pathlib import Path


def observe(mode):
    with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent, prefix='sqlite-review-') as folder:
        path = Path(folder) / 'review.sqlite'
        a = sqlite3.connect(path, isolation_level=None, timeout=0)
        b = sqlite3.connect(path, isolation_level=None, timeout=0)
        try:
            selected = a.execute(f'PRAGMA journal_mode={mode}').fetchone()[0]
            assert selected == mode.lower()
            a.execute('CREATE TABLE readings(value INTEGER)')
            a.execute('INSERT INTO readings VALUES (10)')
            a.execute('BEGIN')
            before = a.execute('SELECT value FROM readings').fetchone()[0]
            b.execute('BEGIN IMMEDIATE')
            b.execute('UPDATE readings SET value=20')
            try:
                b.execute('COMMIT')
                commit = 'committed'
            except sqlite3.OperationalError as error:
                assert error.sqlite_errorcode == sqlite3.SQLITE_BUSY
                commit = error.sqlite_errorname
                b.execute('ROLLBACK')
            during = a.execute('SELECT value FROM readings').fetchone()[0]
            a.execute('COMMIT')
            after = a.execute('SELECT value FROM readings').fetchone()[0]
            assert before == during == 10
            assert (commit, after) == (('committed', 20) if mode == 'WAL' else ('SQLITE_BUSY', 10))
            return {'mode': selected, 'reader_before': before, 'writer_commit': commit,
                    'reader_same_transaction': during, 'reader_new_transaction': after}
        finally:
            b.close()
            a.close()


if __name__ == '__main__':
    result = {'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version,
              'timeout_seconds': 0, 'observations': [observe('DELETE'), observe('WAL')]}
    Path(__file__).with_name('sqlite_result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
