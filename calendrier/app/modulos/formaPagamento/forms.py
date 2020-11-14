from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.modulos.contas.models import Contas


class FormaPagamentoForm(FlaskForm):

    descricao = StringField('Descrição', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Descrição"})
    contas = QuerySelectField('Contas', query_factory=lambda: Contas.query)

