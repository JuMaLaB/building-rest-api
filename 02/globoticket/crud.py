from globoticket.models import DBEvent
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_dbevent(id: int, db: Session) -> DBEvent | None:
    return db.get(DBEvent, id)


def get_all_dbevents(db: Session) -> list[DBEvent]:
    # eventList = db.execute(select(DBEvent)).scalars()._raw_all_rows()
    eventList = db.execute(select(DBEvent)).scalars()
    return eventList  # type: ignore
