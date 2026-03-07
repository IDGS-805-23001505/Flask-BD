import forms
from . import inscripciones
from flask import render_template, request, redirect, url_for
from models import db, Inscripcion, Alumnos, Cursos, Maestros


@inscripciones.route("/inscripciones", methods=['GET','POST'])
def lista_inscripciones():
    inscripciones = db.session.query(
        Inscripcion.id,
        Inscripcion.fecha_inscripcion,
        Alumnos.nombre.label('alumno_nombre'),
        Alumnos.apellidos.label('alumno_apellidos'),
        Cursos.nombre.label('curso_nombre'),
        Maestros.nombre.label('maestro_nombre'),
        Maestros.apellidos.label('maestro_apellidos')
    ).join(Alumnos, Inscripcion.alumno_id == Alumnos.id
    ).join(Cursos, Inscripcion.curso_id == Cursos.id
    ).join(Maestros, Cursos.maestro_id == Maestros.matricula
    ).all()
    
    return render_template("inscripciones/listadoIns.html", 
                         inscripciones=inscripciones)


@inscripciones.route("/inscripciones/agregar", methods=['GET', 'POST'])
def agrega_inscripcion():
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')
        existe = Inscripcion.query.filter_by(
            alumno_id=alumno_id,
            curso_id=curso_id
        ).first()
        
        if existe:
            return redirect(url_for('inscripciones.agrega_inscripcion'))
        
        alumno = Alumnos.query.get(alumno_id)
        curso = Cursos.query.get(curso_id)
        
        curso.alumnos.append(alumno)
        db.session.commit()
        
        return redirect(url_for('cursos.lista_cursos'))
    
    alumnos = Alumnos.query.all()
    cursos = Cursos.query.all()
    return render_template("inscripciones/inscripcion.html", 
                         alumnos=alumnos, 
                         cursos=cursos)
    
    

@inscripciones.route("/inscripciones/detalle", methods=['GET'])
def detalle_inscripcion():
    if request.method == 'GET':
        id = request.args.get('id')
        resultado = db.session.query(
            Inscripcion.id,
            Inscripcion.fecha_inscripcion,
            Alumnos.nombre.label('alumno_nombre'),
            Alumnos.apellidos.label('alumno_apellidos'),
            Cursos.nombre.label('curso_nombre'),
            Maestros.nombre.label('maestro_nombre'),
            Maestros.apellidos.label('maestro_apellidos')
        ).join(Alumnos, Inscripcion.alumno_id == Alumnos.id
        ).join(Cursos, Inscripcion.curso_id == Cursos.id
        ).join(Maestros, Cursos.maestro_id == Maestros.matricula
        ).filter(Inscripcion.id == id).first()
        
        if resultado:
            return render_template("inscripciones/detalles.html",
                                 id=resultado.id,
                                 alumno_nombre=resultado.alumno_nombre,
                                 alumno_apellidos=resultado.alumno_apellidos,
                                 curso_nombre=resultado.curso_nombre,
                                 maestro_nombre=resultado.maestro_nombre,
                                 maestro_apellidos=resultado.maestro_apellidos,
                                 fecha_inscripcion=resultado.fecha_inscripcion)
    
    return redirect(url_for('inscripciones.lista_inscripciones'))