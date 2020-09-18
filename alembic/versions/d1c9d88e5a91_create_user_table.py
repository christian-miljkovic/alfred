"""create alfred db

Revision ID: d1c9d88e5a91
Revises: 
Create Date: 2020-09-17 20:42:28.116505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c9d88e5a91'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        "user",
        sa.Column(
            "id",
            uuid_type,
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("phone_number", sa.String, nullable=False),
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
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("phone_number", sa.String, nullable=False),
        sa.Column("birthday", sa.Date, nullable=False),
        sa.Column("user_id", uuid_type, nullable=False),
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("friend")
