from app import db
from app.modulos.cliente.models import Cliente
from app.modulos.servico.models import Servico
from app.modulos.formaPagamento.models import FormaPagamento


class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confirmado = db.Column(db.Boolean, nullable=False)
    ausencia = db.Column(db.Boolean, nullable=True, default=0)

    data_agenda_inicio = db.Column(db.DateTime, nullable=False)
    data_agenda_fim = db.Column(db.DateTime, nullable=False)
    valor_servico = db.Column(db.Float(15,2))

    #codigo do cliente
    # addresses = db.relationship('Address', backref='person', lazy=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    cliente = db.relationship(Cliente, backref='cliente', lazy=True, uselist=True)

    #servicos = db.relationship('Servico', backref='agenda_servico', lazy=True)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=True)
    servico = db.relationship(Servico, backref='servico', lazy=True, uselist=True)

    #codigo da forma de pagamento    
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey('forma_pagamento.id'))
    forma_pagamento = db.relationship(FormaPagamento, backref='forma_pagamento', lazy=True, uselist=True)

    def __repr__(self):
        return '{} - ({}) - '.format(self.cliente, self.servico)
