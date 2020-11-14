from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db
from datetime import datetime

from app.modulos.lancamentos.forms import LancamentosForm
from app.modulos.lancamentos.models import Lancamentos
from app.modulos.utils.interface import ICadastro


class LancamentosView(ICadastro):

    @login_required
    def salvar():
        form = LancamentosForm()
        if request.method == "POST":
            try:
                obj_model = Lancamentos()
                obj_model.descricao = form.descricao.data
                
                obj_model.contas_id = form.contas.data.id
                obj_model.tipo_movimentacao = form.tipo_movimentacao.data
                
                # data atual do servidor
                obj_model.data_lancamento = datetime.today()

                obj_model.data_prevista = form.data_prevista.data

                obj_model.valor_previsto = float(form.valor_previsto.data)

                if (form.data_efetivacao.data):
                    obj_model.data_efetivacao = form.data_efetivacao.data

                if (form.valor_realizado.data):
                    obj_model.valor_realizado = form.valor_realizado.data

                db.session.add(obj_model)
                db.session.commit()
                flash('Registro "{}" salvo com sucesso.'.format(obj_model.descricao), 'success')
                return redirect(url_for('lancamentoslistar'))
            except Exception as ex:
                flash('Erro ao salvar os dados: {}'.format(ex), 'danger')

        return render_template('lancamentos/cadastro.html', titulo='Lançamentos', form=form, operacao=0)


    @login_required
    def excluir():
        try:
            if request.method ==  "POST":
                id = request.form.get('codigo')
                obj_model = Lancamentos.query.get(int(id))
                desc = obj_model.descricao
                db.session.delete(obj_model)
                db.session.commit()
                flash('Registro "{}" excluído com sucesso'.format(desc), 'success')                
        except Exception as ex:
             flash('Erro ao excluir o registro: {}'.format(ex), 'danger')

        return redirect(url_for('lancamentoslistar'))


    @login_required
    def exibir(id):
        form = LancamentosForm()
        try:
            obj_model = Lancamentos.query.get(int(id))
            form.id = int(id)
            form.descricao.data = obj_model.descricao
            form.tipo_movimentacao.data = obj_model.tipo_movimentacao
            form.contas = obj_model.contas
            form.data_lancamento.data = obj_model.data_lancamento
            form.data_prevista.data = obj_model.data_prevista
            form.data_efetivacao.data = obj_model.data_efetivacao
            form.valor_previsto.data = obj_model.valor_previsto
            form.valor_realizado.data = obj_model.valor_realizado

        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('lancamentos/cadastro.html', titulo='Lançamentos', form=form, operacao=1)


    @login_required
    def editar(id):
        form = LancamentosForm()
        try:
            obj_model = Lancamentos.query.get(int(id))
            if request.method == 'GET':
                form.id = int(id)
                form.descricao.data = obj_model.descricao
                form.tipo_movimentacao.data = obj_model.tipo_movimentacao
                form.contas.data = obj_model.contas
                form.data_lancamento.data = obj_model.data_lancamento
                form.data_prevista.data = obj_model.data_prevista
                form.data_efetivacao.data = obj_model.data_efetivacao
                form.valor_previsto.data = obj_model.valor_previsto
                form.valor_realizado.data = obj_model.valor_realizado
            else:
                obj_model.descricao = form.descricao.data
                obj_model.contas_id = form.contas.data.id
                obj_model.tipo_movimentacao = form.tipo_movimentacao.data

                obj_model.data_prevista = form.data_prevista.data
                obj_model.valor_previsto = float(form.valor_previsto.data)

                if (form.data_efetivacao.data):
                    obj_model.data_efetivacao = form.data_efetivacao.data

                if (form.valor_realizado.data):
                    obj_model.valor_realizado = form.valor_realizado.data

                obj_model.contas_id = form.contas.data.id

                db.session.add(obj_model)
                db.session.commit()
                flash('Registro "{}" alterado com sucesso.'.format(obj_model.descricao), 'success')
                return redirect(url_for('lancamentoslistar'))
                    
        except Exception as ex:
            flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            db.session.rollback()

        return render_template('lancamentos/cadastro.html', titulo='Lançamentos', form=form, operacao=2)

    @login_required
    def listar():
        try:
            form = Lancamentos.query.all()
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('lancamentos/listagem.html', titulo='Lançamentos', forms=form)


    def registrar(self, descricao, conta_id, tipomov_id, data, valor):
        try:
            obj_model = Lancamentos()
            obj_model.descricao = descricao
            
            obj_model.contas_id = conta_id
            obj_model.tipo_movimentacao = tipomov_id
            
            # data atual do servidor
            obj_model.data_lancamento = datetime.today()
            obj_model.data_prevista = data
            obj_model.valor_previsto = valor
            obj_model.data_efetivacao = data
            obj_model.valor_realizado = valor

            db.session.add(obj_model)
            db.session.commit()
            return ''
        except Exception as ex:
            return 'Erro ao salvar os dados: {}'.format(ex)