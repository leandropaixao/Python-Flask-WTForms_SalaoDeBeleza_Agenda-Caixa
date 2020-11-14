from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ContasForm(FlaskForm):

    descricao = StringField('Descrição da conta', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Descrição da conta"})
