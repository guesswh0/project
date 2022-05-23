from datetime import datetime, date, time

from sqlalchemy.orm import Session

from . import models
from app import schemas


def create_well(db: Session, well: schemas.Well):
    well_db = models.Well(**well.dict())
    db.add(well_db)
    db.commit()
    return well_db


def create_reports(db: Session, well_number: str, day: date, values: list):
    """Create reports by time and value series"""
    ts = datetime.combine(day, time.min).timestamp()
    reports = [
        models.Report(ts=ts + i, value=v, well_num=well_number)
        for i, v in enumerate(values)]
    db.add_all(reports)
    db.commit()
    return reports


def get_reports(db: Session, well_number: str, day: date):
    """Get daily reports from database"""
    ts = datetime.combine(day, time.min).timestamp()
    return db.query(models.Report).filter(
        models.Report.well_num == well_number,
        models.Report.ts >= ts,
        models.Report.ts < (ts + 24 * 60 * 60)
    ).all()


def get_cold_reports(db: Session, well_number, day: date):
    """Get non productive (cold) daily reports from database"""
    ts = datetime.combine(day, time.min).timestamp()
    return db.query(models.Report).filter(
        models.Report.well_num == well_number,
        models.Report.ts >= ts,
        models.Report.ts < (ts + 24 * 60 * 60),
        models.Report.value == 0
    ).all()
