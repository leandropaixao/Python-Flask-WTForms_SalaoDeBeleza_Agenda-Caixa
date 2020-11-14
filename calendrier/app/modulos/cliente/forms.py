
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired

class ClienteForm(FlaskForm):

    nome = StringField('None', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Nome"})
    telefone = StringField('Telefone', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Telefone"})
    data_nasc = DateField('Data de nasc.', render_kw={"palceholder": "Data de nascimento"}, format='%d/%m/%Y')
