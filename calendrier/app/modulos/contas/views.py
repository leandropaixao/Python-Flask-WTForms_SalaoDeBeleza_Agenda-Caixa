from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db

from app.modulos.contas.forms import ContasForm
from app.modulos.contas.models import Contas
from app.modulos.utils.interface import ICadastro


class ContasView(ICadastro):

    @login_required
    def salvar():
        form = ContasForm()
        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    obj_model = Contas()
                    obj_model.descricao = form.descricao.data
                    db.session.add(obj_model)
                    db.session.commit()
                    flash('Registro "{}" salvo com sucesso.'.format(obj_model.descricao), 'success')
                    return redirect(url_for('contaslistar'))
                except Exception as ex:
                    flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            else:
                flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')

        return render_template('contas/cadastro.html', titulo='Contas', form=form, operacao=0)


    @login_required
    def excluir():
        try:
            if request.method ==  "POST":
                id = request.form.get('codigo')
                obj_model = Contas.query.get(int(id))
                desc = obj_model.descricao
                db.session.delete(obj_model)
                db.session.commit()
                flash('Registro "{}" excluído com sucesso'.format(desc), 'success')                
        except Exception as ex:
             flash('Erro ao excluir o registro: {}'.format(ex), 'danger')

        return redirect(url_for('contaslistar'))


    @login_required
    def exibir(id):
        form = ContasForm()
        try:
            obj_model = Contas.query.get(int(id))
            form.id = int(id)
            form.descricao.data = obj_model.descricao
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('contas/cadastro.html', titulo='Contas', form=form, operacao=1)


    @login_required
    def editar(id):
        form = ContasForm()
        try:
            obj_model = Contas.query.get(int(id))
            if request.method == 'GET':
                form.id = int(id)
                form.descricao.data = obj_model.descricao
            else:
                if form.validate_on_submit():
                    obj_model.descricao = form.descricao.data
                    
                    db.session.add(obj_model)
                    db.session.commit()
                    flash('Registro "{}" alterado com sucesso.'.format(obj_model.descricao), 'success')
                    return redirect(url_for('formapagamentolistar'))
                else:
                   flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning') 
                    
        except Exception as ex:
            flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
        
        return render_template('contas/cadastro.html', titulo='Contas', form=form, operacao=2)

    @login_required
    def listar():
        try:
            form = Contas.query.all()
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('contas/listagem.html', titulo='Contas', forms=form)
