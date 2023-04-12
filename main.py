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
    instance_name = Column((String(255))) #255 maximum characters.
    generatedNumber = Column(Integer)

class InstanceCounter(Base):
    __tablename__ = "instance_counter"
    instance_name = Column(String(255), primary_key=True)
    count_Generated = Column(Integer)

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)
    instance_id = os.environ.get('GAE_INSTANCE')

    Session = sessionmaker(bind=engine)
    session = Session()

    #check to see whether the instance is already in the InstanceCounter table
    instance_counter = session.query(InstanceCounter).filter_by(instance_name=instance_id).first()

    if instance_counter:
        instance_counter.count_Generated +=1
    else:
        #create a new row for that instance and set it to 1
        new_instance_counter = InstanceCounter(instance_name=instance_id, count_Generated=1)
        session.add(new_instance_counter)

    new_number = TableOfNumbers(instance_name=instance_id, generatedNumber=numbers)

    # Add new instance to session and commit changes to database
    session.add(new_number)
    session.commit()

    return "Random Number generated: " + str(numbers) 

print(GenerateRandomNumber())

@app.route('/GetResults')
def GetResults():
    Session = sessionmaker(bind=engine)
    session = Session()

    #Get the count of total random numbers generated by each instance from the Table InstanceCounter
    instance_counters = session.query(InstanceCounter).all()

    for instance_counter in instance_counters:
        print(f"{instance_counter.instance_name}: {instance_counter.count_Generated}")

    return "Instance counters printed to console"

if __name__ == '__main__':
    app.run()