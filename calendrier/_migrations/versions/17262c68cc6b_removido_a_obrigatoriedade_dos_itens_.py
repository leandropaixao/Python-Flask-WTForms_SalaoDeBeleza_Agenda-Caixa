"""Removido a obrigatoriedade dos itens realizados

Revision ID: 17262c68cc6b
Revises: bda15847b1ee
Create Date: 2020-03-10 12:37:35.210388

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17262c68cc6b'
down_revision = 'bda15847b1ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lancamentos', 'data_efetivacao',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('lancamentos', 'valor_realizado',
               existing_type=mysql.FLOAT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lancamentos', 'valor_realizado',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('lancamentos', 'data_efetivacao',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
