from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired

class ServicoForm(FlaskForm):
    descricao = StringField('Serviço', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Serviço"})
    valor = DecimalField('Valor', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Valor"})
