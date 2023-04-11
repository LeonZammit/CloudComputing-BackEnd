import random 
from flask import Flask

app = Flask(__name__)

@app.route('/GenerateRandomNumber')
def GenerateRandomNumber():
    numbers = random.randint(0,100000)

    return "Random Number generated: " + str(numbers) 

print(GenerateRandomNumber())

if __name__ == '__main__':
    app.run()