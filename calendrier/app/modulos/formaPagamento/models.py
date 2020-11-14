from app import db
from app.modulos.contas.models import Contas

class FormaPagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)

    contas_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    contas = db.relationship(Contas, backref='contas_formapag', lazy=True, uselist=True)

    agenda = db.relationship('Agenda', backref='formaPagamento_agenda', lazy=True, uselist=False)

    def __repr__(self):
        return self.descricao
