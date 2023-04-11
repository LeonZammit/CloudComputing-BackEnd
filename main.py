import random
import os 
from flask import Flask
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#Configure database connection
db_user = "number-handler"
db_pass = "fxcQ25c84dFhWTrfoBzUdlyj"
db_name = "storage-number"
cloud_sql_instance_name = "cloudassignment-383409:europe-west1:db-instance"

connection_string = ('mysql+mysqlconnector://{0}:{1}@/{2}?unix_socket={3}'.
                       format(db_user, db_pass, db_name, f'/cloudsql/{cloud_sql_instance_name}'))
engine = create_engine(connection_string)

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)

    return "Random Number generated: " + str(numbers) 

print(GenerateRandomNumber())

Base = declarative_base()

class TableOfNumbers(Base):
    __tablename__ = "Numbers Generated"
    id = Column(Integer, primary_key=True)
    instanceName = Column((String(255))) #255 maximum characters.
    generatedNumber = Column(Integer)

class InstanceCounter(Base):
    __tablename__ = "instanceCount"
    instanceName = Column(String(255), primary_key=True)
    countGenerated = Column(Integer)

Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    app.run()