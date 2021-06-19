from .init_pre import Base, engine


# recreate databases

import psycopg2
from psycopg2 import sql

from ..settings import POSTGRES_PARAMS


# # drop
cnn = psycopg2.connect(**POSTGRES_PARAMS)
cur = cnn.cursor()
cur.execute("""
    select s.nspname as s, t.relname as t
    from pg_class t join pg_namespace s on s.oid = t.relnamespace
    where t.relkind = 'r'
    and s.nspname !~ '^pg_' and s.nspname != 'information_schema'
    order by 1,2
    """)
tables = cur.fetchall()  # make sure they are the right ones
for t in tables:
    cur.execute(
        sql.SQL("drop table if exists {}.{} cascade")
        .format(sql.Identifier(t[0]), sql.Identifier(t[1])))
cnn.commit()
Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

__all__ = ['Session']
