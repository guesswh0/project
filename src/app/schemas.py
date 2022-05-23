from datetime import date, time
from typing import List

from pydantic import BaseModel


# @dataclass
class Well(BaseModel):
    number: str
    type: str | None = None
    size: int | None = None
    color: str | None = None


class HeadInfo(BaseModel):
    well_number: str
    programmes_target: str | None = None
    machine_type: str | None = None
    contractor: str | None = None


class BottomInfo(BaseModel):
    master_day_shift: str
    master_day_shift_number: str | None = None
    chief: str | None = None
    master_night_shift: str
    master_night_shift_number: str | None = None
    report_data: date | None = date.today()


class Work(BaseModel):
    dbeg: time | None = time.min
    dend: time | None = time.min
    value: str


class Item(BaseModel):
    value: float
    type: int


class WellInfo(BaseModel):
    head_info: HeadInfo
    bottom_info: BottomInfo
    allWorks: List[Work]
    pvNpv: List[Item]
