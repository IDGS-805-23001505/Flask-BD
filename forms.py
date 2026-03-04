from wtforms import Form
from wtforms import IntegerField, StringField, PasswordField
from wtforms import EmailField
from wtforms import validators

##Dentro de los parentesis se esta haciendo la herencia
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