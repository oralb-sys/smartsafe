"""support initial sos emergency

Revision ID: 9478ad0ed621
Revises: da8052053107
Create Date: 2026-09-14 21:21:40.876934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9478ad0ed621'
down_revision: Union[str, Sequence[str], None] = 'da8052053107'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "event_records",
        "latitude",
        existing_type=sa.DECIMAL(precision=9, scale=6),
        nullable=True,
    )

    op.alter_column(
        "event_records",
        "longitude",
        existing_type=sa.DECIMAL(precision=9, scale=6),
        nullable=True,
    )

    op.execute(
        """
        INSERT INTO event_types (
            id,
            code,
            name,
            description,
            module
        )
        SELECT
            UUID(),
            'SOS',
            'Alerta SOS',
            'Alerta inicial del módulo SmartSOS',
            'SMART_SOS'
        WHERE NOT EXISTS (
            SELECT 1
            FROM event_types
            WHERE code = 'SOS'
        )
        """
    )

def downgrade() -> None:
    op.execute(
        """
        DELETE FROM event_types
        WHERE code = 'SOS'
          AND module = 'SMART_SOS'
        """
    )

    op.alter_column(
        "event_records",
        "longitude",
        existing_type=sa.DECIMAL(precision=9, scale=6),
        nullable=False,
    )

    op.alter_column(
        "event_records",
        "latitude",
        existing_type=sa.DECIMAL(precision=9, scale=6),
        nullable=False,
    )
