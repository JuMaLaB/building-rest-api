import decimal
from datetime import date

from database import SessionLocal
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

Base: DeclarativeBase = declarative_base()


class DBCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    events: Mapped[list["DBEvent"]] = relationship(back_populates="category")


class DBEvent(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(unique=True)
    date: Mapped[date]
    price: Mapped[decimal.Decimal]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    # category: Mapped[DBCategory] = relationship()
    # category: Mapped[DBCategory] = relationship(lazy="joined")
    category: Mapped[DBCategory] = relationship(back_populates="events")

    """ def __str__(self):
        return f"{self.id}: {self.product_code:10}
            {self.category.name:10} {self.date} ${self.price}" """


session = SessionLocal()
events = session.execute(select(DBEvent)).scalars()
print("\n".join(str(event) for event in events))

cats = session.execute(select(DBCategory)).scalars()
# lazy query again
print("\n".join(f"{cat.name}: {len(cat.events)}" for cat in cats))
