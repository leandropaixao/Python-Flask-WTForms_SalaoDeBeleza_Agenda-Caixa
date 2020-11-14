from app import db


class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float(15,2), nullable=False)

    agenda = db.relationship('Agenda', backref='servico_agenda', lazy=True, uselist=False)
    
    
    def __repr__(self):
        return '{} - R$ {}'.format(self.descricao, "%.2f" % self.valor)