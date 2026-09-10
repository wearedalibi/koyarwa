"""user profile fields

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "email_visibility",
            sa.String(length=20),
            nullable=False,
            server_default="hidden",
        ),
    )
    op.add_column(
        "users", sa.Column("city", sa.String(length=100), nullable=False, server_default="")
    )
    op.add_column(
        "users", sa.Column("country", sa.String(length=100), nullable=False, server_default="")
    )
    op.add_column(
        "users", sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC")
    )
    op.add_column(
        "users", sa.Column("description", sa.Text(), nullable=False, server_default="")
    )


def downgrade() -> None:
    op.drop_column("users", "description")
    op.drop_column("users", "timezone")
    op.drop_column("users", "country")
    op.drop_column("users", "city")
    op.drop_column("users", "email_visibility")
