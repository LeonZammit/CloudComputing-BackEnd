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

Base = declarative_base()

class TableOfNumbers(Base):
    __tablename__ = "NumbersGenerated"
    id = Column(Integer, primary_key=True)
    instanceName = Column((String(255))) #255 maximum characters.
    generatedNumber = Column(Integer)

class InstanceCounter(Base):
    __tablename__ = "instanceCount"
    instanceName = Column(String(255), primary_key=True)
    countGenerated = Column(Integer)

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_number = TableOfNumbers(instanceName=cloud_sql_instance_name, generatedNumber=numbers)

    # Add new instance to session and commit changes to database
    session.add(new_number)
    session.commit()

    return "Random Number generated: " + str(numbers) 

print(GenerateRandomNumber())

#@app.route('/GetResults')
#def GetResults():
    #session = Session()

if __name__ == '__main__':
    app.run()