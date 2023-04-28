import sqlalchemy

from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'progress'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mmr = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)