from wtforms import Form
from wtforms import IntegerField, StringField, PasswordField
from wtforms import EmailField
from wtforms import validators
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from models import Maestros 

class UserForm(Form):
    id=IntegerField("Id")
    nombre=StringField("Nombre",[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=10, message="Ingrese nombre valido")
    ])
    apellidos=StringField("Apellidos",[
        validators.DataRequired(message="El campo es requerido"),
    ])
    email=EmailField("Correo",[
        validators.Email(message="Ingresa un correo valido")
    ])
    telefono=EmailField("Telefono",[
        validators.Email(message="Ingresa la cantidad correcta")
    ])
    
    
class MaestroForm (Form):
    id=IntegerField("Matricula")
    nombre=StringField("Nombre",[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=10, message="Ingrese nombre valido")
    ])
    apellidos=StringField("Apellidos",[
        validators.DataRequired(message="El campo es requerido"),
    ])
    especialidad=StringField("Especialidad",[
        validators.Email(message="Ingresa un correo valido")
    ])
    email=EmailField("Correo",[
        validators.Email(message="Ingresa la cantidad correcta")
    ])
    
    
class CursoForm (Form):
    id=IntegerField("Id")
    nombre=StringField("Nombre",[
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=10, message="Ingrese nombre valido")
    ])
    descripcion=StringField("Descripcion",[
        validators.DataRequired(message="El campo es requerido"),
    ])
    maestro_id = SelectField('Maestro', coerce=int, validators=[DataRequired(message="Selecciona un maestro")])
    
    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
        self.maestro_id.choices.insert(0, (0, 'Selecciona un maestro'))
    
    
class InscripcionForm(Form):
    id = IntegerField("Id") 
    alumno_id = SelectField('Alumno', coerce=int, validators=[DataRequired()])
    curso_id = SelectField('Curso', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Inscribir')