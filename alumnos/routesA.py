import cursos
import forms
from . import alumnos
from flask import render_template, request, redirect, url_for
from models import db, Alumnos,Cursos



@alumnos.route("/Alumnos",methods=['GET','POST'])
def alumnos_lista():
     create_form=forms.UserForm(request.form)
     if request.method=='POST':
            alum=Alumnos(nombre=create_form.nombre.data,
                     apellidos=create_form.apellidos.data,
                     email=create_form.email.data,
                     telefono=create_form.telefono.data)
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('index'))
     return render_template("alumnos/alumnos.html",form=create_form)
 
 
 
@alumnos.route("/alumnos/detalles", methods=['GET'])
def detalles():
    id = request.args.get('id')
    alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    return render_template('alumnos/detalles.html', alumno=alumno)


@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
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
    return render_template("alumnos/modificar.html", form=create_form)


@alumnos.route("/alumnos/eliminar",methods=['GET','POST'])
def eliminar():
     create_form=forms.UserForm(request.form)
     if request.method=='GET':
         id=request.args.get('id')
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
            db.session.commit()
            return redirect(url_for('index'))
     return render_template("alumnos/eliminar.html",form=create_form)