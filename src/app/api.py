from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import schemas, tools
from app.db import crud, get_db, models

router = APIRouter()


@router.get("/wells/{well_number}/reports")
async def get_reports(
        well_number: str,
        day: date | None = None,
        db: Session = Depends(get_db)):
    db_well = db.query(models.Well).get(well_number)
    if not db_well:
        raise HTTPException(
            status_code=404, detail=f"Well: {well_number}, not exists")

    x = []
    y = []
    for report in crud.get_reports(db, well_number, day):
        x.append(str(datetime.fromtimestamp(report.ts)))
        y.append(report.value)
    return {
        "x": x,
        "y": y,
        "marker": {"size": db_well.size, "color": db_well.color},
        "type": db_well.type
    }


@router.post("/wells/{well_number}/reports/", status_code=201)
async def upload_reports(
        well_number: str,
        file: UploadFile,
        day: date | None = None,
        db: Session = Depends(get_db)):
    db_well = db.query(models.Well).get(well_number)
    if not db_well:
        raise HTTPException(
            status_code=404, detail=f"Well: {well_number}, not exists")

    if not day:
        # file name is date with .xlsx suffix
        day = datetime.strptime(file.filename[:-5], "%d.%m.%Y")

    contents = await file.read()
    df = tools.read_excel(contents)
    crud.create_reports(db, db_well.number, day, df['v'].tolist())
    return {"detail": "Reports successfully uploaded"}


@router.post("/wells/")
async def create_item(item: schemas.WellInfo):
    # Validation api only
    return item
