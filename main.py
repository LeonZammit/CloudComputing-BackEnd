import random
import os 
from flask import Flask
import mysql.connector

app = Flask(__name__)

#Configure database connection
db_user = "number-handler"
db_pass = "fxcQ25c84dFhWTrfoBzUdlyj"
db_name = "storage-number"
cloud_sql_instance_name = "cloudassignment-383409:europe-west1:db-instance"

def ConnectToDatabase():
    config = {
        'user': db_user,
        'password': db_pass,
        'database': db_name,
        'unix_socket': f'/cloudsql/{cloud_sql_instance_name}'
    }

    return mysql.connector.connect(**config)

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)

    return "Random Number generated: " + str(numbers) 

print(GenerateRandomNumber())

if __name__ == '__main__':
    app.run()