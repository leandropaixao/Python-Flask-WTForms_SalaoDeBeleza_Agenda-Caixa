from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db
from datetime import date

from app.modulos.cliente.forms import ClienteForm
from app.modulos.cliente.models import Cliente
from app.modulos.utils.interface import ICadastro


class ClienteView(ICadastro):

    @login_required
    def salvar():
        form = ClienteForm()
        if request.method ==  "POST":
            '''
            if (form.data_nasc.data == None):
                data_agora = date(2000,1,1)
                form.data_nasc = data_agora
            print(form.data_nasc.data)
            '''
            if form.validate_on_submit():
                try:
                    cliente = Cliente()
                    cliente.nome = form.nome.data
                    cliente.telefone = form.telefone.data
                    cliente.data_nasc = form.data_nasc.data
                    db.session.add(cliente)
                    db.session.commit()
                    flash('Registro "{}" salvo com sucesso.'.format(cliente.nome),'success')
                    return redirect(url_for('clientelistar'))
                except Exception as ex:
                    flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            else:
                flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')
    
        return render_template('cliente/cadastro.html', titulo='Cliente', form=form, operacao=0)


    @login_required
    def excluir():
        try:
            if request.method ==  "POST":
                id = request.form.get('codigo')
                cliente = Cliente.query.get(int(id))
                desc = cliente.nome
                db.session.delete(cliente)
                db.session.commit()
                flash('Registro "{}" excluído com sucesso'.format(desc), 'success')
        except Exception as ex:
             flash('Erro ao excluir o registro: {}'.format(ex), 'danger')
        
        return redirect(url_for('clientelistar'))


    @login_required
    def exibir(id):
        form = ClienteForm()
        try:
            cliente = Cliente.query.get(int(id))
            form.id = int(id)
            form.nome.data = cliente.nome
            form.telefone.data = cliente.telefone
            form.data_nasc.data = cliente.data_nasc 
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')
        
        return render_template('cliente/cadastro.html', titulo='Cliente', form=form, operacao=1)


    @login_required
    def editar(id):
        form = ClienteForm()
        try:
            cliente = Cliente.query.get(int(id))
            if request.method == 'GET':
                form.id = int(id)
                form.nome.data = cliente.nome
                form.telefone.data = cliente.telefone
                form.data_nasc.data = cliente.data_nasc
                return render_template('cliente/cadastro.html', titulo='Cliente', form=form, operacao=2)
            else:
                if form.validate_on_submit():
                    cliente.nome = form.nome.data
                    cliente.telefone = form.telefone.data
                    cliente.data_nasc = form.data_nasc.data

                    db.session.add(cliente)
                    db.session.commit()
                    flash('Registro "{}" alterado com sucesso.'.format(cliente.nome), 'success')
                    return redirect(url_for('clientelistar'))
                else:
                    flash('Não foi possível validar os dados: {}'.format(form.errors), 'warning')
                    return render_template('cliente/cadastro.html', titulo='Cliente', form=form, operacao=2)

        except Exception as ex:
            flash('Erro ao salvar os dados: {}'.format(ex), 'danger')
            return render_template('cliente/cadastro.html', titulo='Cliente', form=form, operacao=2)


    @login_required
    def listar():
        try:
            form = Cliente.query.all()
        except Exception as ex:
            flash('Não foi possível carregar os dados: {}'.format(ex), 'danger')

        return render_template('cliente/listagem.html', titulo='Cliente', forms=form)
        