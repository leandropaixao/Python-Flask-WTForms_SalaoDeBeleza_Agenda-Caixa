from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db

from app.modulos.lancamentos.models import Lancamentos
from app.modulos.contas.models import Contas
from sqlalchemy.sql import func
from sqlalchemy import text
from textwrap import dedent

class DashboardView():

    @login_required
    def dashboard():
        
        #next_page = request.args.get('next')
        '''
        Agenda.query.with_entities(
                func.sum(Agenda.valor_servico).label('valor')
            ).filter(Agenda.confirmado==1).join(Servico.agenda)
        '''
        #saldo das contas
        sql = text('''SELECT DESCRICAO, SUM(VALOR) AS TOTAL FROM  (
                       SELECT
                        CONT.DESCRICAO,
                        SUM(LANC.VALOR_REALIZADO) AS VALOR
                    FROM LANCAMENTOS AS LANC
                    LEFT JOIN CONTAS AS CONT ON LANC.CONTAS_ID = CONT.ID
                    WHERE TIPO_MOVIMENTACAO = 'C'
                    GROUP BY CONT.DESCRICAO
                    UNION
                    SELECT
                        CONT.DESCRICAO,
                        SUM(LANC.VALOR_REALIZADO)*-1 AS VALOR
                    FROM LANCAMENTOS AS LANC
                    LEFT JOIN CONTAS AS CONT ON LANC.CONTAS_ID = CONT.ID
                    WHERE TIPO_MOVIMENTACAO = 'D'
                    GROUP BY CONT.DESCRICAO
                    ) AS A
                GROUP BY DESCRICAO
                ''')
        
        result = db.engine.execute(sql)
        saldo_contas = [row for row in result]

        # movimentações realizadas
        realizado_debito = Lancamentos.query.with_entities(
            Lancamentos.descricao,
            Lancamentos.data_efetivacao,
            func.sum(Lancamentos.valor_realizado).label('total_realizado'),
            func.month(Lancamentos.data_efetivacao).label('mes')
        ).filter(Lancamentos.tipo_movimentacao=='D', Lancamentos.data_efetivacao!=None).group_by(Lancamentos.descricao,
            Lancamentos.data_efetivacao).all()
        
        realizado_credito = Lancamentos.query.with_entities(
            Lancamentos.descricao,
            Lancamentos.data_efetivacao,
            func.sum(Lancamentos.valor_realizado).label('total_realizado'),
            func.month(Lancamentos.data_efetivacao).label('mes')
        ).filter(Lancamentos.tipo_movimentacao=='C',Lancamentos.data_efetivacao!=None).group_by(Lancamentos.descricao,
            Lancamentos.data_efetivacao).all()
        ######################################
        
        # movimentações previstas
        previsto_debito = Lancamentos.query.with_entities(
            Lancamentos.descricao,
            Lancamentos.data_prevista,
            func.sum(Lancamentos.valor_previsto).label('total_previsto'),
            func.month(Lancamentos.data_prevista).label('mes')
        ).filter(Lancamentos.tipo_movimentacao=='D', Lancamentos.data_efetivacao==None).group_by(Lancamentos.descricao,
            Lancamentos.data_prevista).all()

        previsto_credito = Lancamentos.query.with_entities(
            Lancamentos.descricao,
            Lancamentos.data_prevista,
            func.sum(Lancamentos.valor_previsto).label('total_previsto'),
            func.month(Lancamentos.data_prevista).label('mes')
        ).filter(Lancamentos.tipo_movimentacao=='C',Lancamentos.data_efetivacao==None).group_by(Lancamentos.descricao,
            Lancamentos.data_prevista).all()
        ######################################

        '''
        previsto_total = Lancamentos.query.with_entities(
            Lancamentos.descricao,
            Lancamentos.data_prevista,
            func.sum(Lancamentos.valor_previsto).label('total_previsto')
        ).group_by(Lancamentos.descricao,
            Lancamentos.data_prevista).all()
        '''

        return render_template('fluxocaixa/dashboard.html', titulo='Fluxo caixa',
            previsto_debito=previsto_debito,
            previsto_credito=previsto_credito,
            realizado_debito=realizado_debito,
            realizado_credito=realizado_credito,
            saldo_contas=saldo_contas)
