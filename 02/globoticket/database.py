# import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///events.db"
# SQLALCHEMY_DATABASE_URL = URL.create(os.getenv("SQLALCHEMY_DATABASE_URL"))  # type: ignore

print("---------------------------")
print(SQLALCHEMY_DATABASE_URL)
print("---------------------------")

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL.strip(),  # type: ignore
    SQLALCHEMY_DATABASE_URL,  # type: ignore
    connect_args={"check_same_thread": False},
    echo=True,
)
SessionLocal = sessionmaker(bind=engine)
