import datetime
from typing import List

from sqlalchemy import BIGINT, TIMESTAMP, func, ForeignKey, FLOAT, CheckConstraint, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    lang: Mapped[str] = mapped_column()
    join_date: Mapped[str] = mapped_column(__type_pos=TIMESTAMP, default=func.current_timestamp)
    freelancers : Mapped[List['Freelancer']] = relationship(back_populates="user")
    customers : Mapped[List['Customer']] = relationship(back_populates="user")

class ProgLang(Base):
    __tablename__ = "prog_langs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    freelancers : Mapped[List['Freelancer']] = relationship(back_populates="prog_lang")


class Freelancer(Base):
    __tablename__ = "freelancers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    prog_lang_id: Mapped[int] = mapped_column(ForeignKey("prog_langs.id"))
    join_date: Mapped[str] = mapped_column(__type_pos=TIMESTAMP, default=datetime.datetime.now())
    prog_lang : Mapped["ProgLang"] = relationship(back_populates="freelancers")
    user : Mapped["User"] = relationship(back_populates="freelancers")

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    join_date: Mapped[str] = mapped_column(__type_pos=TIMESTAMP, default=datetime.datetime.now())
    user : Mapped["User"] = relationship(back_populates="customers")
    products : Mapped[List['Product']] = relationship(back_populates="customer")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    price : Mapped[float] = mapped_column("price",FLOAT, CheckConstraint("price > 0") )
    prog_lang: Mapped[str]
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    join_date: Mapped[str] = mapped_column(__type_pos=TIMESTAMP, default=datetime.datetime.now())
    customer : Mapped['Customer'] = relationship(back_populates="products")




