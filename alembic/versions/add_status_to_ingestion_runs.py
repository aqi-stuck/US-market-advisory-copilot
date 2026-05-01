"""add status column to ingestion_runs table

Revision ID: 001add_status
Revises: ce098e453d66
Create Date: 2026-05-01 09:15:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "001add_status"
down_revision = "ce098e453d66"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add status column with default value
    op.add_column(
        "ingestion_runs",
        sa.Column("status", sa.String(30), server_default="pending", nullable=False),
    )


def downgrade() -> None:
    # Remove status column
    op.drop_column("ingestion_runs", "status")
