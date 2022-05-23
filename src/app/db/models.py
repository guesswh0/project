from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from . import Base


class Well(Base):
    __tablename__ = "wells"

    number = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    color = Column(String, nullable=True)


class Report(Base):
    __tablename__ = "reports"

    ts = Column(Integer, primary_key=True)  # timestamp
    value = Column(Float)
    well_num = Column(Integer, ForeignKey('wells.number'), primary_key=True, index=True)


Report.well = relationship("Well", back_populates="reports")
Well.reports = relationship("Report", order_by=Report.ts, back_populates="well")
