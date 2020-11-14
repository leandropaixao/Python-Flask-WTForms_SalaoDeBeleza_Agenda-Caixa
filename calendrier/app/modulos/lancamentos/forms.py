from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, DateField, DecimalField, SelectField
from wtforms.validators import DataRequired
from app.modulos.contas.models import Contas


class LancamentosForm(FlaskForm):

    # > Tipo movimentação (debito/credito)
    tipo_movimentacao = SelectField('Tipo de movimentção', choices=[('D','Débito'),('C','Crédito')])
    # > Descrição
    descricao = StringField('Descrição', render_kw={"placeholder": "Descrição"})
    # > Data lançamento
    data_lancamento = DateField('Data lançamento', render_kw={"palceholder": "Data lançamento"}, format='%d/%m/%Y')
    # > Data prevista: data prevista da operação a ser realizada
    data_prevista = DateField('Data prevista', render_kw={"palceholder": "Data prevista"}, format='%d/%m/%Y')
    # > Data efetivação: data real da entrada ou do pagamento
    data_efetivacao = DateField('Data efetivação', render_kw={"palceholder": "Data efetivação"}, format='%d/%m/%Y')
    # > Valor Previsto
    valor_previsto = DecimalField('Valor previsto', render_kw={"placeholder": "Valor previsto"})
    # > Valor Realizado
    valor_realizado = DecimalField('Valor realizado', render_kw={"placeholder": "Valor realizado"})
    # > Vínculo da conta que será referenciada
    contas = QuerySelectField('Contas', query_factory=lambda: Contas.query)
    