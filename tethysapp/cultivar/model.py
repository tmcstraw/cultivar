import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
import os
import csv


from .app import Cultivar as app

yaque_csv_filename = "yaque_del_sur_parcel_data.csv"

def read_parcels_from_csv():
    folder_path = '/Users/travismcstraw/tethysdev/tethysapp-cultivar/tethysapp/cultivar/workspaces/app_workspace/'
    file_path = os.path.join(folder_path,yaque_csv_filename)

    yaque_parcels_csv = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parcel = ((row['OBJECTID']),float(row['AREA']),(row['DUENO']))
            yaque_parcels_csv.append(parcel)
    return yaque_parcels_csv


Base = declarative_base()


# SQLAlchemy ORM definition for the dams table
class Parcel(Base):
    """
    SQLAlchemy Dam DB Model
    """
    __tablename__ = 'Yaque del Sur'

    # Columns
    fid = Column(Integer, primary_key=True)
    object_id = Column(String)
    dueno = Column(String)
    AREA = Column(Float)
    Area_Planted = Column(Float)
    Crop_1 = Column(String)
    Area_Crop_1 = Column(Float)
    Crop_2 = Column(String)
    Area_Crop_2 = Column(Float)
    Crop_3 = Column(String)
    Area_Crop_3 = Column(Float)


def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    # Create all the tables
    Base.metadata.create_all(engine)

    # Add data
    # if first_time:
        # Make session
    Session = sessionmaker(bind=engine)
    session = Session()

    yaque_del_sur_parcels = read_parcels_from_csv()

    for item in yaque_del_sur_parcels:
        parcel = Parcel(
            object_id=item[0],
            dueno = item[2],
            AREA=item[1],
            Area_Planted = 0,
            Crop_1 ='',
            Area_Crop_1 = 0,
            Crop_2 = '',
            Area_Crop_2 = 0,
            Crop_3 = '',
            Area_Crop_3 = 0
        )
        session.add(parcel)



    session.commit()
    session.close()

def get_all_parcels():
    """
    Get all persisted dams.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query for all dam records
    all_parcels = session.query(Parcel).all()
    session.close()

    return all_parcels
