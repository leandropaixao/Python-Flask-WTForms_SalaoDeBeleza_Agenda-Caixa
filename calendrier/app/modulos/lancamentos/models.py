from app import db
from app.modulos.contas.models import Contas


class Lancamentos(db.Model):

    #identificador único
    id = db.Column(db.Integer, primary_key=True)

    # > Tipo movimentação (debito/credito)
    tipo_movimentacao = db.Column(db.String(1), nullable=False)
    # > Descrição
    descricao = db.Column(db.String(150), nullable=False)
    # > Data lançamento
    data_lancamento = db.Column(db.Date, nullable=False)
    # > Data prevista: data prevista da operação a ser realizada
    data_prevista = db.Column(db.Date, nullable=False)
    # > Data efetivação: data real da entrada ou do pagamento
    data_efetivacao = db.Column(db.Date, nullable=True)
    # > Valor Previsto
    valor_previsto = db.Column(db.Float(15,2), nullable=False)
    # > Valor Realizado
    valor_realizado = db.Column(db.Float(15,2), nullable=True)
    # > Vínculo da conta que será referenciada
    contas_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    contas = db.relationship(Contas, backref='contas', lazy=True, uselist=True)

    def __repr__(self):
        return self.descricao
