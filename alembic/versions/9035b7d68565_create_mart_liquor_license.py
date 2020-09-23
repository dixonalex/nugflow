"""create mart liquor license

Revision ID: 9035b7d68565
Revises: 1342f15d329d
Create Date: 2019-11-29 18:06:04.949300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9035b7d68565"
down_revision = "1342f15d329d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mart_liquor_license",
        sa.Column("id", sa.String(32), nullable=False, primary_key=True),
        sa.Column("load_date", sa.DateTime(), nullable=False, primary_key=True),
        sa.Column("source_service", sa.String(), nullable=False),
        sa.Column("license_number", sa.String(), nullable=False),
        sa.Column("address_1", sa.String()),
        sa.Column("address_2", sa.String()),
        sa.Column("city", sa.String()),
        sa.Column("state", sa.String()),
        sa.Column("zip", sa.String()),
        sa.Column("doing_business_as", sa.String()),
        sa.Column("expiration_date", sa.String()),
    )


def downgrade():
    op.drop_table("mart_liquor_license")
