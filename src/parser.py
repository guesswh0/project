import os
from datetime import datetime

import click
from sqlalchemy.orm import Session

from app import schemas, tools
from app.db import SessionLocal, models, init_db, crud

init_db()
session: Session = SessionLocal()


@click.command()
@click.option('-s', '--source', default='data')
def main(source):
    """Explicitly populate database from source data folder"""
    if not os.path.exists(source):
        # source path not exists
        return 1

    for dir_ in os.listdir(source):
        for file_ in os.listdir(os.path.join(source, dir_)):
            if not file_.endswith('.xlsx'):
                continue
            df = tools.read_excel(os.path.join(source, dir_, file_))
            # dir name is well_number
            well = session.query(models.Well).get(dir_)
            # create well if not exists
            if not well:
                well = crud.create_well(session, schemas.Well(number=dir_))
            # file name is date with .xlsx suffix
            day = datetime.strptime(file_[:-5], "%d.%m.%Y")
            crud.create_reports(session, well.number, day, df['v'].tolist())

            # todo message to display


if __name__ == '__main__':
    main()
