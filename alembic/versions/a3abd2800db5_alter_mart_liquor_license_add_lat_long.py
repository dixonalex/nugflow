"""alter mart liquor license add lat long

Revision ID: a3abd2800db5
Revises: 729f262bd636
Create Date: 2019-12-01 07:29:47.055410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3abd2800db5"
down_revision = "729f262bd636"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("mart_liquor_license") as bop:
        bop.add_column(sa.Column("geo_match_type", sa.String()))
        bop.add_column(sa.Column("geo_match_exactness", sa.String()))
        bop.add_column(sa.Column("latitude", sa.Float()))
        bop.add_column(sa.Column("longitude", sa.Float()))


def downgrade():
    with op.batch_alter_table("mart_liquor_license") as bop:
        bop.drop_column(sa.Column("geo_match_type"))
        bop.drop_column(sa.Column("geo_match_exactness"))
        bop.drop_column(sa.Column("latitude"))
        bop.drop_column(sa.Column("longitude"))
