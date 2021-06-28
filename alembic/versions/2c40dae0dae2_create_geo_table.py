"""create geo table

Revision ID: 2c40dae0dae2
Revises: 
Create Date: 2021-06-28 23:48:52.022746

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2c40dae0dae2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "geo",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("ip", sa.String, unique=True),
        sa.Column("continent", sa.String),
        sa.Column("continent_code", sa.String),
        sa.Column("country", sa.String),
        sa.Column("country_iso", sa.String),
        sa.Column("city", sa.String, nullable=True),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("time_zone", sa.String),
        sa.Column("postal", sa.String, nullable=True),
        sa.Column("metro_code", sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_table("geo")
