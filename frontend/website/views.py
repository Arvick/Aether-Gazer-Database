from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("base.html")


@views.route("/mod")
def modifiers():
    data = request.args
    print(dict(data))
    return render_template("mod.html")

'''
dict(data) v
{'gen_zone': 'Asterim', 'combat_type': 'Ranged', 'dmg_type': 'Fire', 'combat_rsc': 'Energy', 'name': '', 
'modifier_name': ''}
'''