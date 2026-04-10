
from pydantic import BaseModel
from pydantic.fields import Field
from utils.datetime import format_date_now, format_time_now
from enum import Enum
import datetime

class Currency(str, Enum):
    CDF = "CDF"
    USD = "USD"

class Type(str, Enum):
    Incoming = "Incoming"
    Outcoming = "Outcoming"

class Transaction(BaseModel):
    date: datetime.date = Field(default_factory=format_date_now)
    time: datetime.time = Field(default_factory=format_time_now)
    amount: int
    currency: Currency
    type: Type
    category: str
    description: str = ""
