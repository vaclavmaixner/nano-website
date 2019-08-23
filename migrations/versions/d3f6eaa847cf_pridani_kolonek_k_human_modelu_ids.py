"""Pridani kolonek k human modelu - ids

Revision ID: d3f6eaa847cf
Revises: daa79025f24b
Create Date: 2019-08-23 14:36:04.962158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f6eaa847cf'
down_revision = 'daa79025f24b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('human', sa.Column('orcid', sa.String(), nullable=True))
    op.add_column('human', sa.Column('researcher_id', sa.String(), nullable=True))
    op.add_column('human', sa.Column('scopus_id', sa.String(), nullable=True))
    op.drop_column('human', 'ids')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('human', sa.Column('ids', sa.VARCHAR(), nullable=True))
    op.drop_column('human', 'scopus_id')
    op.drop_column('human', 'researcher_id')
    op.drop_column('human', 'orcid')
    # ### end Alembic commands ###