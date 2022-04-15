import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.String)
    src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
