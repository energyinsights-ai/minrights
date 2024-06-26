from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Table
from sqlalchemy import orm
from sqlalchemy.orm import reconstructor


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    __table_args__={'schema':'minrights'}

    user_id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]