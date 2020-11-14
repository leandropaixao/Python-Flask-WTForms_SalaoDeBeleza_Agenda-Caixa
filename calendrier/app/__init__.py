from flask import Flask, Blueprint, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.modulos.utils.momentjs import MomentJs


app = Flask(__name__, static_folder="static", template_folder="templates")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#app.register_error_handler(404, page_not_found)

app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
app.jinja_env.globals['momentjs'] = MomentJs
login.login_view = 'login'
api_bp = Blueprint('api', __name__)

# importando as rotas dos modulos
from app.modulos.index.views import IndexView

#Modulo de usuarios
from app.modulos.user.views import UserView
app.add_url_rule('/login','login', view_func=UserView.login, methods=['GET', 'POST'])
app.add_url_rule('/logout','logout', view_func=UserView.logout, methods=['GET'])

#modulo de servico
from app.modulos.servico.views import ServicoView
app.add_url_rule('/servico', 'servicolistar', view_func=ServicoView.listar, methods=['GET'])
app.add_url_rule('/servico/cadastrar', 'servicocadastrar', view_func=ServicoView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/servico/editar/<int:id>', 'servicoeditar', view_func=ServicoView.editar, methods=['GET', 'POST'])
app.add_url_rule('/servico/exibir/<int:id>', 'servicoexibir', view_func=ServicoView.exibir, methods=['GET'])
app.add_url_rule('/servico/excluir', 'servicoexcluir', view_func=ServicoView.excluir, methods=['POST'])

#modulo de cliente
from app.modulos.cliente.views import ClienteView
app.add_url_rule('/cliente', 'clientelistar', view_func=ClienteView.listar, methods=['GET'])
app.add_url_rule('/cliente/cadastrar', 'clientecadastrar', view_func=ClienteView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/cliente/editar/<int:id>', 'clienteeditar', view_func=ClienteView.editar, methods=['GET', 'POST'])
app.add_url_rule('/cliente/exibir/<int:id>', 'clienteexibir', view_func=ClienteView.exibir, methods=['GET'])
app.add_url_rule('/cliente/excluir', 'clienteexcluir', view_func=ClienteView.excluir, methods=['POST'])

#modulo de forma de pagamento
from app.modulos.formaPagamento.views import FormaPagamentoView
app.add_url_rule('/formapagamento', 'formapagamentolistar', view_func=FormaPagamentoView.listar, methods=['GET'])
app.add_url_rule('/formapagamento/cadastrar', 'formapagamentocadastrar', view_func=FormaPagamentoView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/formapagamento/editar/<int:id>', 'formapagamentoeditar', view_func=FormaPagamentoView.editar, methods=['GET', 'POST'])
app.add_url_rule('/formapagamento/exibir/<int:id>', 'formapagamentoexibir', view_func=FormaPagamentoView.exibir, methods=['GET'])
app.add_url_rule('/formapagamento/excluir', 'formapagamentoexcluir', view_func=FormaPagamentoView.excluir, methods=['POST'])


#modulo de agenda
from app.modulos.agenda.views import AgendaView
app.add_url_rule('/agenda', 'agendalistar', view_func=AgendaView.exibir, methods=['GET'])
app.add_url_rule('/agenda/cadastrar', 'agendacadastrar', view_func=AgendaView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/agenda/editar/<int:id>', 'agendaeditar', view_func=AgendaView.editar, methods=['GET', 'POST'])
app.add_url_rule('/agenda/excluir/<int:id>', 'agendaexcluir', view_func=AgendaView.excluir, methods=['GET', 'POST'])


# módulo das movimentações financeiras e fluxo de caixa
# módulo de contas
from app.modulos.contas.views import ContasView
app.add_url_rule('/contas', 'contaslistar', view_func=ContasView.listar, methods=['GET'])
app.add_url_rule('/contas/cadastrar', 'contascadastrar', view_func=ContasView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/contas/editar/<int:id>', 'contaseditar', view_func=ContasView.editar, methods=['GET', 'POST'])
app.add_url_rule('/contas/exibir/<int:id>', 'contasexibir', view_func=ContasView.exibir, methods=['GET'])
app.add_url_rule('/contas/excluir', 'contasexcluir', view_func=ContasView.excluir, methods=['GET', 'POST'])

# módulo de Lacamentos
from app.modulos.lancamentos.views import LancamentosView
app.add_url_rule('/lancamentos', 'lancamentoslistar', view_func=LancamentosView.listar, methods=['GET'])
app.add_url_rule('/lancamentos/cadastrar', 'lancamentoscadastrar', view_func=LancamentosView.salvar, methods=['GET', 'POST'])
app.add_url_rule('/lancamentos/editar/<int:id>', 'lancamentoseditar', view_func=LancamentosView.editar, methods=['GET', 'POST'])
app.add_url_rule('/lancamentos/exibir/<int:id>', 'lancamentosexibir', view_func=LancamentosView.exibir, methods=['GET'])
app.add_url_rule('/lancamentos/excluir', 'lancamentosexcluir', view_func=LancamentosView.excluir, methods=['GET', 'POST'])

from app.modulos.fluxocaixa.views import DashboardView
app.add_url_rule('/fluxocaixa', 'fluxocaixa', view_func=DashboardView.dashboard, methods=['GET'])

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.102')
