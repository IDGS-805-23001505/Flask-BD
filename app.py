from alumnos import alumnos
from flask import Flask, render_template, request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate, migrate
from config import DevelopmentConfig
from maestros.routes import maestros
from cursos.routesC import cursos
from inscripciones.routesI import inscripciones
import forms

from models import db, Alumnos



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(alumnos)
app.register_blueprint(maestros)
app.register_blueprint(cursos) 
app.register_blueprint(inscripciones ) 
db.init_app(app)
migrate=Migrate(app,db)
csrf=CSRFProtect(app)


@app.errorhandler(404)
def page_not_fount(e):
    return render_template ("404.html"), 404


@app.route("/", methods=['GET','POST'])
@app.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    alumno=Alumnos.query.all()
    return render_template("alumnos/index.html",form=create_form,alumno=alumno)
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
app.run()





