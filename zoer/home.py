from flask import Blueprint, render_template

#Creo el blueprint de inicio
bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

