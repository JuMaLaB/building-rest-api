"""
Documentation of JSON data model class
=> helpfull for having some information in FASTApi swagger like
"""

import datetime
import decimal

from pydantic import BaseModel


class Event(BaseModel):
    id: int
    date: datetime.date
    price: decimal.Decimal
    # product_code: str
    # category_id: int
    artist: str
    name: str
    content: str
    image: str
