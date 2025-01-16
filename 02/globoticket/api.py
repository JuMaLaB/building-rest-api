"""
api.py
---

The REST Api for the Globoticket events database.
"""

from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from globoticket.crud import get_all_dbevents, get_dbevent
from globoticket.database import SessionLocal
from globoticket.models import DBEvent
from globoticket.schemas import Event
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent


# create db session/connection every time we need to answer a request
def get_session() -> Session:  # type: ignore
    session = SessionLocal()
    try:
        # session will be closed after get_event call
        yield session  # type: ignore
    finally:
        session.close()


@app.get("/event/{id}", response_model=Event)
def get_event(id: int, db: Annotated[Session, Depends(get_session)]) -> DBEvent:
    """Retrieve a single event by id. Returns status 404 if event is not found."""
    # event = db.get(DBEvent, id)
    event = get_dbevent(id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"No product with id {id}")
    return event


# shouyld come fater get_event otherwise first will endpoint intercept all /event/{id} request
@app.get("/event/", response_model=list[Event])
def get_all_events(db: Annotated[Session, Depends(get_session)]) -> list[DBEvent]:
    return get_all_dbevents(db)


# should come after all other endpoints
app.mount("/", StaticFiles(directory=PROJECT_ROOT / "static", html=True))
