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

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)
    instance_id = os.environ.get('GAE_INSTANCE')

    Session = sessionmaker(bind=engine)
    session = Session()

    new_number = TableOfNumbers(instanceName=instance_id, generatedNumber=numbers)

    # Add new instance to session and commit changes to database
    session.add(new_number)
    session.commit()

    return "Random Number generated: " + str(numbers) 

@app.route('/GetResults')
def GetResults():
    Session = sessionmaker(bind=engine)
    session = Session()

     # Execute SQL query to get instance counts
    results = session.execute('SELECT instanceName, COUNT(*) AS instance_count FROM NumbersGenerated GROUP BY instanceName')

    # Create an HTML table to display the results
    tableOutput = '<table><thead><tr><th>Instance Name</th><th>Number of Generated Numbers</th></tr></thead><tbody>'
    for row in results:
        tableOutput += f'<tr><td>{row.instanceName}</td><td>{row.instance_count}</td></tr>'
    tableOutput += '</tbody></table>'

    return tableOutput

if __name__ == '__main__':
    app.run()