"""create alfred table

Revision ID: b5f220464acf
Revises: 
Create Date: 2020-10-01 21:19:54.496558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5f220464acf"
down_revision = None
branch_labels = None
depends_on = None
uuid_type = sa.dialects.postgresql.UUID


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table(
        "customer",
        sa.Column(
            "id",
            uuid_type,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("phone_number", sa.String, nullable=False),
        sa.Column("birthday", sa.Date, nullable=False),
    )

    op.create_table(
        "friend",
        sa.Column(
            "id",
            uuid_type,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("client_id", uuid_type, nullable=False),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("phone_number", sa.String, nullable=False),
        sa.Column("birthday", sa.Date, nullable=False),
    )


def downgrade():
    op.drop_table("customer")
    op.drop_table("friend")
