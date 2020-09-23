"""create california liquor license table

Revision ID: 1342f15d329d
Revises: 646683095d59
Create Date: 2019-11-29 16:20:45.194385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1342f15d329d"
down_revision = "646683095d59"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "liquor_license_california_sat",
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
        sa.Column("license_type", sa.String()),
        sa.Column("lic_or_app", sa.String()),
        sa.Column("type_status", sa.String()),
        sa.Column("type_orig_iss_date", sa.String()),
        sa.Column("expir_date", sa.String()),
        sa.Column("master_ind", sa.String()),
        sa.Column("term_in_#_of_months", sa.String()),
        sa.Column("geo_code", sa.String()),
        sa.Column("primary_name", sa.String()),
        sa.Column("prem_addr_1", sa.String()),
        sa.Column("prem_addr_2", sa.String()),
        sa.Column("prem_city", sa.String()),
        sa.Column("prem_state", sa.String()),
        sa.Column("prem_zip", sa.String()),
        sa.Column("dba_name", sa.String()),
        sa.Column("prem_county", sa.String()),
        sa.Column("prem_census_tract_#", sa.String()),
    )


def downgrade():
    op.drop_table("liquor_license_california_sat")
