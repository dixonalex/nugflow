"""create liquor license geolocation sat

Revision ID: 729f262bd636
Revises: 9035b7d68565
Create Date: 2019-11-30 12:08:31.422223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "729f262bd636"
down_revision = "9035b7d68565"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "liquor_license_geolocation_sat",
        sa.Column(
            "hkey",
            sa.String(32),
            sa.ForeignKey("liquor_license_hub.hkey"),
            primary_key=True,
        ),
        sa.Column("load_date", sa.DateTime(), nullable=False, primary_key=True),
        sa.Column("source_service", sa.String(), nullable=False),
        sa.Column("hash_diff", sa.String(32), nullable=False),
        sa.Column("license_number", sa.String(), nullable=False),
        sa.Column("full_address", sa.String()),
        sa.Column("match_type", sa.String()),
        sa.Column("match_exactness", sa.String()),
        sa.Column("full_address_calculated", sa.String()),
        sa.Column("latitude", sa.Float()),
        sa.Column("longitude", sa.Float()),
        sa.Column("tiger_line_id", sa.String()),
        sa.Column("tiger_line_side", sa.String()),
    )


def downgrade():
    op.drop_table("liquor_license_geolocation_sat")
