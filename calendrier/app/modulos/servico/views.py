from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db

from app.modulos.servico.forms import ServicoForm
from app.modulos.servico.models import Servico
from app.modulos.utils.interface import ICadastro


class ServicoView(ICadastro):

    @login_required
    def salvar():
        form = ServicoForm()
        if request.method ==  "POST":
            if form.validate_on_submit():
                try:
                    servico = Servico()
                    servico.descricao = form.descricao.data
                    servico.valor = form.valor.data
                    db.session.add(servico)
                    db.session.commit()
                    flash('Registro "{}" salvo com sucesso'.format(servico.descricao), 'success')
                    return redirect(url_for('servicolistar'))
                except Exception as ex:
                    flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            else:
                flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')

        return render_template('servico/cadastro.html', titulo='Serviço', form=form, operacao=0)
   

    @login_required
    def excluir():
        try:
            if request.method ==  "POST":
                id = request.form.get('codigo')
                servico = Servico.query.get(int(id))
                desc = servico.descricao
                db.session.delete(servico)
                db.session.commit()
                flash('Registro "{}" excluído com sucesso'.format(desc), 'success')
                return redirect(url_for('servicolistar'))
        except Exception as ex:
             flash('Erro ao excluir registro: {}'.format(ex), 'danger')
    

    @login_required
    def exibir(id):
        form = ServicoForm()
        try:
            servico = Servico.query.get(int(id))
            form.id = int(id)
            form.descricao.data = servico.descricao
            form.valor.data = servico.valor 
            
            return render_template('servico/cadastro.html', titulo='Serviço', form=form, operacao=1)
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')


    @login_required
    def editar(id):
        form = ServicoForm()
        try:
            servico = Servico.query.get(int(id))
            if request.method == 'GET':
                form.id = int(id)
                form.descricao.data = servico.descricao
                form.valor.data = servico.valor
                return render_template('servico/cadastro.html', titulo='Serviço', form=form, operacao=2)
            else:
                if form.validate_on_submit():
                    servico.descricao = form.descricao.data
                    servico.valor = form.valor.data
                    db.session.add(servico)
                    db.session.commit()
                    flash('Registro "{}" alterado com sucesso.'.format(servico.descricao), 'success')
                    return redirect(url_for('servicolistar'))
                else:
                    flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')
                    return render_template('servico/cadastro.html', titulo='Serviço', form=form, operacao=2)

        except Exception as ex:
            flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            return render_template('servico/cadastro.html', titulo='Serviço', form=form, operacao=2)


    @login_required
    def listar():
        try:
            form = Servico.query.all()
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')
        
        return render_template('servico/listagem.html', titulo='Serviço', forms=form)