"""create ilcc tables

Revision ID: 646683095d59
Revises:
Create Date: 2019-05-21 22:32:15.993890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "646683095d59"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "liquor_license_hub",
        sa.Column("hkey", sa.String(32), primary_key=True),
        sa.Column("load_date", sa.DateTime(), nullable=False),
        sa.Column("source_service", sa.String(), nullable=False),
        sa.Column("license_number", sa.String(), nullable=False),
    )

    op.create_table(
        "liquor_license_illinois_sat",
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
        sa.Column("license_class", sa.String()),
        sa.Column("retail_type", sa.String()),
        sa.Column("sales_tax_account_number", sa.String()),
        sa.Column("issue_date", sa.String()),
        sa.Column("expiration_date", sa.String()),
        sa.Column("application_status", sa.String()),
        sa.Column("license_status", sa.String()),
        sa.Column("licensee_name", sa.String()),
        sa.Column("business_name", sa.String()),
        sa.Column("street_address", sa.String()),
        sa.Column("city", sa.String()),
        sa.Column("state", sa.String()),
        sa.Column("zip", sa.String()),
        sa.Column("county", sa.String()),
        sa.Column("type", sa.String()),
        sa.Column("owners", sa.String()),
    )

    op.create_table(
        "liquor_license_colorado_sat",
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
        sa.Column("licensee_name", sa.String()),
        sa.Column("doing_business_as", sa.String()),
        sa.Column("license_type", sa.String()),
        sa.Column("expires", sa.String()),
        sa.Column("street_address", sa.String()),
        sa.Column("city", sa.String()),
        sa.Column("state", sa.String()),
        sa.Column("zip", sa.String()),
    )


def downgrade():
    op.drop_table("liquor_license_hub")
    op.drop_table("liquor_license_illinois_sat")
    op.drop_table("liquor_license_colorado_sat")
