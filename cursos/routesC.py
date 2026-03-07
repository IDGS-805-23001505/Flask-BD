import forms
from . import cursos
from flask import render_template, request, redirect, url_for

from models import db, Cursos, Inscripcion, Alumnos, Maestros



@cursos.route("/cursos", methods=['GET','POST'])
def lista_cursos():
    create_form=forms.CursoForm(request.form)
    cursos=Cursos.query.all()
    return render_template("cursos/listadoCur.html",form=create_form,
                           cursos=cursos)
    
    
@cursos.route("/curso/agregar",methods=['GET','POST'])
def agrega_curso():
     create_form=forms.CursoForm(request.form)
     if request.method=='POST':
            cur=Cursos(nombre=create_form.nombre.data,
                     descripcion=create_form.descripcion.data,
                     maestro_id=create_form.maestro_id.data)
            db.session.add(cur)
            db.session.commit()
            return redirect(url_for('cursos.lista_cursos'))
     return render_template("cursos/cursos.html",form=create_form)
 
 
@cursos.route("/curso/modificar", methods=["GET", "POST"])
def modificar_curso():
    create_form = forms.CursoForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        cur1 = db.session.query(Cursos).filter(Cursos.id == id).first()
        create_form.id.data = cur1.id
        create_form.nombre.data = cur1.nombre
        create_form.descripcion.data = cur1.descripcion
    if request.method == "POST":
        id= create_form.id.data
        cur = db.session.query(Cursos).filter(Cursos.id==id).first()
        cur.nombre=create_form.nombre.data
        cur.descripcion=create_form.descripcion.data
        db.session.add(cur)
        db.session.commit()
        return redirect(url_for("cursos.lista_cursos"))
    return render_template("cursos/modificar.html", form=create_form)



@cursos.route("/cursos/detalles", methods=['GET'])
def detalle_curso():
    if request.method == 'GET':
        id = request.args.get('id')
        
        cur1 = db.session.query(Cursos).filter(Cursos.id == id).first()
        
        if cur1:
            nombre = cur1.nombre
            descripcion = cur1.descripcion
            
            from models import Inscripcion, Alumnos, Maestros
            
            # Obtener TODAS las inscripciones de este curso
            inscripciones = Inscripcion.query.filter_by(curso_id=id).all()
            
            # Lista para guardar todos los alumnos
            alumnos_inscritos = []
            
            for insc in inscripciones:
                alumno = Alumnos.query.get(insc.alumno_id)
                if alumno:
                    alumnos_inscritos.append(alumno)
            
            # Datos del maestro
            maestro_nombre = ''
            maestro_apellidos = ''
            if cur1.maestro_id:
                maestro = Maestros.query.get(cur1.maestro_id)
                if maestro:
                    maestro_nombre = maestro.nombre
                    maestro_apellidos = maestro.apellidos
            
            return render_template('cursos/detalles.html',
                                 id=id,
                                 nombre=nombre,
                                 descripcion=descripcion,
                                 alumnos=alumnos_inscritos,
                                 curso_nombre=nombre,
                                 maestro_nombre=maestro_nombre,
                                 maestro_apellidos=maestro_apellidos)
    
    return redirect(url_for('cursos.lista_cursos'))
    
    

@cursos.route("/cursos/eliminar",methods=['GET','POST'])
def eliminar_curso():
     create_form=forms.CursoForm(request.form)
     if request.method=='GET':
         id=request.args.get('id')
         cur1=db.session.query(Cursos).filter(Cursos.id==id).first()
         create_form.id.data=cur1.id
         create_form.nombre.data=cur1.nombre
         create_form.descripcion.data=cur1.descripcion
     if request.method=='POST':
            id=create_form.id.data
            cur=Cursos.query.get(id)
            db.session.delete(cur)
            db.session.commit()
            return redirect(url_for('cursos.lista_cursos'))
     return render_template("cursos/eliminar.html",form=create_form)
