from flask import render_template, flash
from flask_login import login_required
from app import app
from app.modulos.agenda.models import Agenda
from app.modulos.agenda.forms import AgendaForm
from app.modulos.servico.models import Servico
from app.modulos.formaPagamento.models import FormaPagamento

from datetime import datetime, date

from sqlalchemy.sql import func


class IndexView():

    @app.route('/')
    @app.route('/index', methods=['GET'])
    @login_required
    def index():
        try:
            #data_atual = date.today()
            
            confirmado = Agenda.query.with_entities(
                func.sum(Agenda.valor_servico).label('valor')
            ).filter(Agenda.confirmado==1).join(Servico.agenda)

            naocompareceu = Agenda.query.with_entities(
                func.sum(Servico.valor).label('valor')
            ).filter(Agenda.confirmado==0, Agenda.ausencia==0, 
                func.DATE(Agenda.data_agenda_inicio) < date.today()).join(Servico.agenda)

            previsto = Agenda.query.with_entities(
                func.sum(Servico.valor).label('valor')
            ).filter(Agenda.ausencia==0).join(Servico.agenda)

            atendimento = Agenda.query.with_entities(
                func.count(Agenda.id).label('totalagenda')
            ).filter( func.DATE(Agenda.data_agenda_inicio) == date.today(),
                    Agenda.ausencia==0)

            total = Agenda.query.with_entities(
                func.sum(Agenda.valor_servico).label('valor')
            ).join(FormaPagamento).filter( #func.DATE(Agenda.data_agenda_inicio) == date.today(),
            Agenda.confirmado == True, Agenda.ausencia==0).all()

            #montagem dos totalizadores de entradas confirmadas no sistema no mês
            recebimentos = Agenda.query.with_entities(
                FormaPagamento.descricao.label('descricao'),
                func.sum(Agenda.valor_servico).label('valorservico'),
                (func.sum(Agenda.valor_servico) * 100 / total[0][0]).label('perc')
            ).join(FormaPagamento).filter( #func.DATE(Agenda.data_agenda_inicio) == date.today(),
            Agenda.confirmado == True, Agenda.ausencia==0).group_by(FormaPagamento.descricao).all()
            
            return render_template('index.html', 
                confirmado=confirmado,
                naocompareceu=naocompareceu,
                previsto=previsto,
                atendimento=atendimento,
                recebimentos=recebimentos,
                total=total[0][0])
        except Exception as ex:
            flash('Não foi possível carregar os dados {}'.format(ex), 'error')
        
        return render_template('index.html', form='')
