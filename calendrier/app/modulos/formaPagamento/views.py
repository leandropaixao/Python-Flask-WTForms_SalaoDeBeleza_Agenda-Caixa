from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db

from app.modulos.formaPagamento.forms import FormaPagamentoForm
from app.modulos.formaPagamento.models import FormaPagamento
from app.modulos.utils.interface import ICadastro


class FormaPagamentoView(ICadastro):

    @login_required
    def salvar():
        form = FormaPagamentoForm()
        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    formaPag = FormaPagamento()
                    formaPag.descricao = form.descricao.data
                    formaPag.contas_id = form.contas.data.id
                    
                    db.session.add(formaPag)
                    db.session.commit()
                    flash('Registro "{}" salvo com sucesso.'.format(formaPag.descricao), 'success')
                    return redirect(url_for('formapagamentolistar'))
                except Exception as ex:
                    flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            else:
                flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')

        return render_template('formapagamento/cadastro.html', titulo='Forma de Pagamento', form=form, operacao=0)


    @login_required
    def excluir():
        try:
            if request.method ==  "POST":
                id = request.form.get('codigo')
                formaPag = FormaPagamento.query.get(int(id))
                desc = formaPag.descricao
                db.session.delete(formaPag)
                db.session.commit()
                flash('Registro "{}" excluído com sucesso'.format(desc), 'success')                
        except Exception as ex:
             flash('Erro ao excluir o registro: {}'.format(ex), 'danger')

        return redirect(url_for('formapagamentolistar'))


    @login_required
    def exibir(id):
        form = FormaPagamentoForm()
        try:
            formaPag = FormaPagamento.query.get(int(id))
            form.id = int(id)
            form.descricao.data = formaPag.descricao
            form.contas.data = formaPag.contas
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('formapagamento/cadastro.html', titulo='Forma de pagamento', form=form, operacao=1)


    @login_required
    def editar(id):
        form = FormaPagamentoForm()
        try:
            formaPag = FormaPagamento.query.get(int(id))
            if request.method == 'GET':
                form.id = int(id)
                form.descricao.data = formaPag.descricao
                form.contas.data = formaPag.contas
            else:
                if form.validate_on_submit():
                    formaPag.descricao = form.descricao.data
                    formaPag.contas_id = form.contas.data.id
                    
                    db.session.add(formaPag)
                    db.session.commit()
                    flash('Registro "{}" alterado com sucesso.'.format(formaPag.descricao), 'success')
                    return redirect(url_for('formapagamentolistar'))
                else:
                   flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning') 
                    
        except Exception as ex:
            flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
        
        return render_template('formapagamento/cadastro.html', titulo='Forma de pagamento', form=form, operacao=2)

    @login_required
    def listar():
        try:
            form = FormaPagamento.query.all()
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('formapagamento/listagem.html', titulo='Forma de pagamento', forms=form)
