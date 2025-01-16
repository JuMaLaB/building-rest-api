import decimal
from datetime import date

from globoticket.frontmatter import get_frontmatter
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    reconstructor,
    relationship,
)

Base: DeclarativeBase = declarative_base()


class DBCategory(Base):  # type: ignore
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    events: Mapped[list["DBEvent"]] = relationship(back_populates="category")


class DBEvent(Base):  # type: ignore
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

    @reconstructor  # method will be called each time sql aclchemy will read an object from db
    def _get_frontmatter(self):
        frontmatter = get_frontmatter(self.product_code)
        for k, v in frontmatter.items():
            if not hasattr(self, k):
                setattr(self, k, v)


"""
session = SessionLocal()
events = session.execute(select(DBEvent)).scalars()
print("\n".join(str(event) for event in events))

cats = session.execute(select(DBCategory)).scalars()
# lazy query again
print("\n".join(f"{cat.name}: {len(cat.events)}" for cat in cats))
"""
