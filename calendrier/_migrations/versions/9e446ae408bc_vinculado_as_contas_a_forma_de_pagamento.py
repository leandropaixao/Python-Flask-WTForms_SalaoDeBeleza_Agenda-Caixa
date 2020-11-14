"""vinculado as contas a forma de pagamento

Revision ID: 9e446ae408bc
Revises: dd1ba9208f3f
Create Date: 2020-03-21 14:20:35.537179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e446ae408bc'
down_revision = 'dd1ba9208f3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forma_pagamento', sa.Column('contas_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'forma_pagamento', 'contas', ['contas_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'forma_pagamento', type_='foreignkey')
    op.drop_column('forma_pagamento', 'contas_id')
    # ### end Alembic commands ###
