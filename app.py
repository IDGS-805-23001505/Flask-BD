from flask import Flask, render_template, request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate, migrate
from config import DevelopmentConfig
import forms

from models import db, Alumnos



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
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
    return render_template("index.html",form=create_form,alumno=alumno)


@app.route("/Alumnos",methods=['GET','POST'])
def alumnos():
     create_form=forms.UserForm(request.form)
     if request.method=='POST':
            alum=Alumnos(nombre=create_form.nombre.data,
                     apellidos=create_form.apellidos.data,
                     email=create_form.email.data,
                     telefono=create_form.telefono.data)
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('index'))
     return render_template("alumnos.html",form=create_form)
 
 
 
@app.route("/detalles",methods=['GET','POST'])
def detalles():
    if request.method=='GET':
         id=request.args.get('id')
         #select * from alumnos where id=id
         alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
         nombre=alum1.nombre
         apellidos=alum1.apellidos
         email=alum1.email
         telefono=alum1.telefono
    return render_template('detalles.html',id=id, nombre=nombre, 
                           apellidos=apellidos,email=email)
        


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono
    if request.method == "POST":
        id= create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.email=create_form.email.data
        alum.telefono=create_form.telefono.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("modificar.html", form=create_form)


@app.route("/eliminar",methods=['GET','POST'])
def eliminar():
     create_form=forms.UserForm(request.form)
     if request.method=='GET':
         id=request.args.get('id')
         #select * from alumnos where id=id
         alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
         create_form.id.data=alum1.id
         create_form.nombre.data=alum1.nombre
         create_form.apellidos.data=alum1.apellidos
         create_form.email.data=alum1.email
         create_form.telefono.data=alum1.telefono
     if request.method=='POST':
            id=create_form.id.data
            alum=Alumnos.query.get(id)
            db.session.delete(alum)
            ##Se hacer el commit para que guarde
            db.session.commit()
            ##Reedirige a la pagina del index
            return redirect(url_for('index'))
     return render_template("eliminar.html",form=create_form)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
app.run()





