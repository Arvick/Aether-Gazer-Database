"""This module holds the code for the API that communicates with the database."""
from flask import Flask
from flask_restful import Api, Resource
'''
search options:
modifier name
name
gen zone
meeele/ranged
'''

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return {"Data": "shsh"}

api.add_resource(Test, "/Test")

if __name__ == "__main__":
    app.run(debug=True)