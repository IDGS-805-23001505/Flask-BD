import forms
from . import maestros
from flask import render_template, request, redirect, url_for
from models import db, Maestros, Cursos


@maestros.route("/maestros", methods=['GET','POST'])
def lista_maestros():
    create_form=forms.UserForm(request.form)
    maestros=Maestros.query.all()
    return render_template("maestros/listadoMest.html",form=create_form,
                           maestros=maestros)
    
    
@maestros.route("/detalles", methods=['GET'])
def detalles_maestros():
    if request.method == 'GET':
        id = request.args.get('id')
        mae1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        
        if mae1:
            nombre = mae1.nombre
            apellidos = mae1.apellidos
            especialidad = mae1.especialidad
            email = mae1.email
            return render_template('maestros/detalles.html', 
                                   id=id, nombre=nombre,apellidos=apellidos, 
                                   especialidad=especialidad, 
                                   email=email)
    return redirect(url_for('maestros.lista_maestros'))



@maestros.route("/agregar",methods=['GET','POST'])
def agrega_maestros():
     create_form=forms.MaestroForm(request.form)
     if request.method=='POST':
            maes=Maestros(nombre=create_form.nombre.data,
                     apellidos=create_form.apellidos.data,
                     especialidad=create_form.especialidad.data,
                     email=create_form.email.data)
            db.session.add(maes)
            db.session.commit()
            return redirect(url_for('maestros.lista_maestros'))
     return render_template("maestros/maestros.html",form=create_form)
 
 
 
  
@maestros.route("/eliminar", methods=['GET', 'POST'])
def eliminar_maestros():
    create_form = forms.MaestroForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        mae1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        create_form.id.data = mae1.matricula
        create_form.nombre.data = mae1.nombre
        create_form.apellidos.data = mae1.apellidos
        create_form.especialidad.data = mae1.especialidad
        create_form.email.data = mae1.email
        
    if request.method == 'POST':
        id = create_form.id.data
        maes = Maestros.query.get(id)
        
        otro_maestro = Maestros.query.filter(Maestros.matricula != id).first()
        
        if otro_maestro:
            Cursos.query.filter_by(maestro_id=maes.matricula).update({'maestro_id': otro_maestro.matricula})
        
        db.session.delete(maes)
        db.session.commit()
        return redirect(url_for('maestros.lista_maestros'))
        
    return render_template("maestros/eliminar.html", form=create_form)



 
  
@maestros.route("/modificar", methods=["GET", "POST"])
def modificar_maestros():
    create_form = forms.MaestroForm(request.form)
    
    if request.method == "GET":
        id = request.args.get("id")
        mae1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        if mae1:
            create_form.id.data = mae1.matricula
            create_form.nombre.data = mae1.nombre
            create_form.apellidos.data = mae1.apellidos
            create_form.especialidad.data = mae1.especialidad
            create_form.email.data = mae1.email
        else:
            return redirect(url_for("maestros.lista_maestros"))
    if request.method == "POST":
        id = create_form.id.data
        maes = db.session.query(Maestros).filter(Maestros.matricula == id).first()
        
        if maes:
            maes.nombre = create_form.nombre.data
            maes.apellidos = create_form.apellidos.data
            maes.especialidad = create_form.especialidad.data
            maes.email = create_form.email.data
            
            db.session.add(maes)
            db.session.commit()
        return redirect(url_for("maestros.lista_maestros"))
    return render_template("maestros/modificar.html", form=create_form)