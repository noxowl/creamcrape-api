"""
:mod: 'creamcrape.db.orm'

-------------------------------------------------------------------------------

Set ORM.

.. :moduleauthor: Mirai Kim <me@euc-kr.net>

"""

from flask_sqlalchemy import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ('Base', 'Session', 'initialize_database')

Base = declarative_base()
Session = sessionmaker(autocommit=True, autoflush=True, expire_on_commit=False)


def initialize_database(engine):
    Base.metadata.create_all(engine)
