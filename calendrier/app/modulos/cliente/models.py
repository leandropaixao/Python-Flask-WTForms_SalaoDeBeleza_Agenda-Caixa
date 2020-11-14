from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(16), nullable=False)
    data_nasc = db.Column(db.Date)

    agenda = db.relationship('Agenda', backref='cliente_agenda', lazy=True, uselist=False)

    def __repr__(self):
        return '{} - {}'.format(self.nome, self.telefone)
