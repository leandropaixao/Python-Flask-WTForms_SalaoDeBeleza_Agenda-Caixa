from app import db

class Contas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)

    lancamentos = db.relationship('Lancamentos', backref='contas_lancamentos', lazy=True, uselist=False)

    def __repr__(self):
        return self.descricao
