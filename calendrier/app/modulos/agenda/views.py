from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
#from werkzeug.urls import url_parse
from app import db
from datetime import timedelta, date

from app.modulos.agenda.forms import AgendaForm
from app.modulos.agenda.models import Agenda
from app.modulos.cliente.models import Cliente
from app.modulos.servico.models import Servico
from app.modulos.formaPagamento.models import FormaPagamento
#from app.modulos.utils.interface import ICadastro


class AgendaView():

    @login_required
    def exibir():
        form = AgendaForm()
        try:
            events = Agenda.query.with_entities(
                Agenda.id,
                Cliente.id.label('id_cliente'),
                Servico.id.label('id_servico'),
                FormaPagamento.id.label('id_forma_pagamento'),
                Cliente.nome.label('nome'),
                Servico.descricao.label('servico'),
                FormaPagamento.descricao.label('forma_pagamento'),
                Agenda.data_agenda_inicio.label('start'),
                Agenda.data_agenda_fim.label('end'),
                Agenda.ausencia.label('ausencia'),
                Agenda.confirmado.label('confirmado')
                ).outerjoin(Cliente, Servico, FormaPagamento)
        
            #le jour de départ du calendrier
            date_default = date.today()
        except Exception as ex:
            flash('Não foi possível carregar os dados da agenda: {}'.format(ex), 'error')
        
        return render_template('agenda/fullcalendar.html', titulo='Agenda', form=form, 
            operacao=1, events=events, date_default=date_default)


    @login_required
    def salvar():
        form = AgendaForm()

        if request.method ==  "POST": 
            try:
                agenda = Agenda()
                agenda.confirmado = False
                agenda.data_agenda_inicio = form.data_agenda_inicio.data

                if form.data_agenda_fim.data:
                    agenda.data_agenda_fim = form.data_agenda_fim.data
                else:
                    agenda.data_agenda_fim = form.data_agenda_inicio.data + timedelta(minutes=40)

                agenda.ausencia = form.ausencia.data
                
                if not(form.ausencia.data):
                    agenda.cliente_id = form.cliente.data.id
                    agenda.servico_id = form.servico.data.id
                    qdesc =  Cliente.query.get(agenda.cliente_id)
                
                db.session.add(agenda)
                db.session.commit()
                if agenda.ausencia:
                    desc = 'Ausencia'
                else:
                    desc = qdesc.nome
                
                flash('Agendamento para "{}" realizado com sucesso'.format(desc), 'success')
                
                return redirect(url_for('agendalistar'))
            except Exception as ex:
                flash('Erro ao salvar os dados: {}'.format(ex), 'error')

        return render_template('agenda/cadastro.html', titulo='Agenda', form=form, operacao=0)


    @login_required
    def editar(id):        
        try:
            
            #form = AgendaForm()
            agenda = Agenda.query.get(int(id))

            #agenda.confirmado = False
            #date_teste = request.form.get('data_agenda_inicio')
            #date_teste = datetime.strptime(request.form.get('data_agenda_inicio'),  '%Y-%m-%d %H:%M:%S')
            #agenda.data_agenda_inicio = parser.parse(request.form.get('data_agenda_inicio'))
            #agenda.data_agenda_fim = agenda.data_agenda_inicio + timedelta(minutes=40)
            '''
            print(request.form.get('data_agenda_inicio')
            print(request.form.get('data_agenda_fim')
            agenda.data_agenda_inicio = request.form.data_agenda_inicio.data
            agenda.data_agenda_fim = request.form.data_agenda_fim.data
            '''
            agenda.cliente_id = request.form.get('cliente')
            agenda.servico_id = request.form.get('servico')
            
            desc =  Cliente.query.get(agenda.cliente_id)

            if request.form.get('forma_pagamento') !=  "":
                agenda.confirmado = True
                agenda.forma_pagamento_id = request.form.get('forma_pagamento')

                formapaga_dados = FormaPagamento.query.with_entities(
                    FormaPagamento.contas_id
                ).filter(FormaPagamento.id == request.form.get('forma_pagamento'))

                #servico_dados = Servico.query.with_entities(
                #    Servico.valor,
                #    Servico.descricao
                #).filter(Servico.id == agenda.servico_id)

                servico_dados = Servico.query.get(agenda.servico_id)
                print(servico_dados.valor)

                agenda.valor_servico = servico_dados.valor

                #adicionar o lançamento para o fluxo de caixa
                from app.modulos.lancamentos.views import LancamentosView
                
                descricao = '{} - {}'.format(desc.nome, servico_dados.descricao)

                obj_lanc = LancamentosView()
                msg = obj_lanc.registrar(descricao, formapaga_dados, 'C', date.today(), agenda.valor_servico)

                print(msg)
            

            db.session.add(agenda)
            db.session.commit()
            flash('Agendamento da "{}" alterado com sucesso.'.format(desc.nome), 'success')

        except Exception as ex:
            flash('Não foi possível alterar os dados {}'.format(ex), 'error')
        
        return redirect(url_for('agendalistar'))


    @login_required
    def excluir(id):
        try:
            agenda = Agenda.query.get(int(id))
            desc = Cliente.query.get(int(id))
            db.session.delete(agenda)
            db.session.commit()
            flash('Agendamento da "{}" excluído com sucesso'.format(desc.nome), 'success')
            return redirect(url_for('agendalistar'))
        except Exception as ex:
            flash('Não foi possível excluir os dados {}'.format(ex), 'error')
        return redirect(url_for('agendalistar'))
