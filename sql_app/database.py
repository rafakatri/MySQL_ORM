from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import mysql.connector


load_dotenv(override=True)
host=os.getenv('MD_DB_SERVER')
user=os.getenv('MD_DB_USERNAME')
password=os.getenv('MD_DB_PASSWORD')
database='academia'

mydb = mysql.connector.connect(
 host= host,
 user= user,
 password= password,
 database=database
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE academia IF NOT EXISTS")

mydb.commit()

mydb.close()


SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{user}:{password}@{host}/{database}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   
