from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import DateTimeField, IntegerField, DecimalField, BooleanField
from wtforms.validators import DataRequired
from app.modulos.agenda.models import Agenda
from app.modulos.cliente.models import Cliente
from app.modulos.servico.models import Servico
from app.modulos.formaPagamento.models import FormaPagamento


class AgendaForm(FlaskForm):
    
    id = IntegerField()
    data_agenda_inicio =  DateTimeField('Data da agenda', validators=[DataRequired(message="Campo obrigatório")], render_kw={"palceholder": "Data inicio da agenda"}, format='%d/%m/%Y %H:%M')
    data_agenda_fim =  DateTimeField('Data de fim', render_kw={"palceholder": "Data fim da agenda"}, format='%d/%m/%Y %H:%M' )
    ausencia = BooleanField('Ausência')
    valor = DecimalField('Valor')

    cliente = QuerySelectField('Cliente', query_factory=lambda: Cliente.query, allow_blank=True)
    servico = QuerySelectField('Serviço', query_factory=lambda: Servico.query,allow_blank=True)
    forma_pagamento = QuerySelectField('Forma de pagamento', query_factory=lambda: FormaPagamento.query, allow_blank=True)

