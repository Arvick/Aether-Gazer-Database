"""This module holds the code for the API that communicates with the database."""
from flask import Flask
from flask_restful import Api, Resource, reqparse
from database import *
'''
search options:
modifier name
name
gen zone
meeele/ranged


How search filter work:

Resource?(arg1 = arg) or Resource?arg1=arg&arg2=arg&.....
'''


'''
possible blueprint

class Resourcename(Resource):
    def get(self):
        1. use parse_args to get any keywords
        2. use those keywords in SQL query
        3. send query, get results (separate function in db_queries)
        4. format all results into specifc dict format
        5. return list[dict], where each dict is a result

'''

MAIN_APP = Flask(__name__)
API = Api(MAIN_APP)

@MAIN_APP.route("/")
def home():
    """Represents the home page of the API. 
    Provides a welcome message + navigation guide."""
    return '''Welcome to the Aether Gazer API.

Basic Commands:
    mod: looks up modifiers ++++++++++
        - Optional Arguments:
            1. name (name of modifier)
            2. modifier_name (modifier's codename)
            3. gen_zone (modifier's Gen-Zone)
            4. combat type (modifier's combat type (meele or ranged))
            5. dmg_type (modifier's damage type (fire, water, etc.))
            6. combat_rsc (modifier's used combat resource (energy, rage, etc.))
---------------------------------------------------------------------------------
    functor: looks up functors +++++++++++
        - Optional Arguments
            1. functor_name (name of functor)
            2. gen_zone (functor's Gen-Zone)
            3. sig_modifier (recommended modifier of Functor
                if it has none, enter N/A)
            4. rarity (of functor: 3, 4, or 5)
----------------------------------------------------------------------------------------
    sigil: looks up sigil sets ++++++++++++++
        - Optional Arguments
            1. set_name: name of the sigil set
            2. keyword: a keyword in the sigil set's description
'''


mod_get_args = reqparse.RequestParser()
mod_get_args.add_argument("name", type = str, required = False)
mod_get_args.add_argument("modifier_name", type = str, required = False)
mod_get_args.add_argument("gen_zone", type = str, required = False)
mod_get_args.add_argument("combat_type", type = str, required = False)
mod_get_args.add_argument("dmg_type", type = str, required = False)
mod_get_args.add_argument("combat_rsc", type = str, required = False)



class Modifier(Resource):
    """This class is for handling modifier requests, and retrives
    all functors that meet the conditions specified in arguments.
    
    GET:
        The arguments are parsed (with None values being filtered out)
        and sent to the SQL query function to get the data, which is formatted and returned
        in a dict"""
    def get(self) -> list[dict]:
        data = database_queries.query_interface("mod", {key : value for key,value in dict(mod_get_args.parse_args()).items() if value})
        return data, 200

API.add_resource(Modifier, "/mod")



functor_get_args = reqparse.RequestParser()
functor_get_args.add_argument("functor_name", type = str, required = False)
functor_get_args.add_argument("gen_zone", type = str, required = False)
functor_get_args.add_argument("sig_modifier", type = str, required = False)
functor_get_args.add_argument("rarity", type = int, required = False)

class Functor(Resource):
    """This class is for handling functor requests, and retrives
    all functors that meet the conditions specified in arguments"""

    def get(self) -> list[dict]:
        data = database_queries.query_interface("functor", {key : value for key,value in dict(functor_get_args.parse_args()).items() if value})
        return data, 200


API.add_resource(Functor, "/func")


sigil_get_args = reqparse.RequestParser()
sigil_get_args.add_argument("set_name", type = str, required = False)
sigil_get_args.add_argument("keyword", type = str, required = False)

class Sigil(Resource):
    """This class is for handling sigil requests, and retrives
    all sigil sets that meet the conditions specified in arguments"""

    def get(self) -> list[dict]:
        data = database_queries.query_interface("sigil", {key : value for key,value in dict(sigil_get_args.parse_args()).items() if value})
        return data


API.add_resource(Sigil, "/sigil")



def run():
    """runs the API."""
    MAIN_APP.run(debug=False)

if __name__ == "__main__":
    MAIN_APP.run(debug=True)

