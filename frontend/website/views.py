from flask import Blueprint, render_template, request
import requests

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("base.html")


@views.route("/mod")
def modifiers():
    return render_template("mod.html", func=requests.get)

@views.route("/func")
def functors():
    return render_template("func.html", func=requests.get)

@views.route("/sigil")
def sigils():
    return render_template("sigil.html", func=requests.get)


'''
dict(data) v
{'gen_zone': 'Asterim', 'combat_type': 'Ranged', 'dmg_type': 'Fire', 'combat_rsc': 'Energy', 'name': '', 
'modifier_name': ''}
'''