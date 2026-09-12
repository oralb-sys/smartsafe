"""seed smartreport event types

Revision ID: REEMPLAZAR_POR_LA_REVISION_GENERADA
Revises: ab906b15b928
Create Date: 2026-09-12

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "da8052053107"
down_revision: Union[str, Sequence[str], None] = "ab906b15b928"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SMART_REPORT_TYPES = [
    {
        "id": "10000000-0000-0000-0000-000000000001",
        "code": "POTHOLE",
        "name": "Bache",
        "description": "Bache o deterioro de la vía pública.",
        "module": "SMART_REPORT",
    },
    {
        "id": "10000000-0000-0000-0000-000000000002",
        "code": "WASTE",
        "name": "Residuos",
        "description": "Acumulación o disposición inadecuada de residuos.",
        "module": "SMART_REPORT",
    },
    {
        "id": "10000000-0000-0000-0000-000000000003",
        "code": "STREET_LIGHT",
        "name": "Alumbrado público",
        "description": "Falla o ausencia de alumbrado público.",
        "module": "SMART_REPORT",
    },
    {
        "id": "10000000-0000-0000-0000-000000000004",
        "code": "WATER_LEAK",
        "name": "Fuga de agua",
        "description": "Fuga de agua en infraestructura urbana.",
        "module": "SMART_REPORT",
    },
]


def upgrade() -> None:
    connection = op.get_bind()

    event_types = sa.table(
        "event_types",
        sa.column("id", sa.String(36)),
        sa.column("code", sa.String(50)),
        sa.column("name", sa.String(100)),
        sa.column("description", sa.String(500)),
        sa.column("module", sa.String(20)),
    )

    for item in SMART_REPORT_TYPES:
        existing = connection.execute(
            sa.select(event_types.c.id).where(
                event_types.c.code == item["code"]
            )
        ).scalar_one_or_none()

        if existing is None:
            connection.execute(
                event_types.insert().values(**item)
            )


def downgrade() -> None:
    connection = op.get_bind()

    event_types = sa.table(
        "event_types",
        sa.column("code", sa.String(50)),
        sa.column("module", sa.String(20)),
    )

    connection.execute(
        event_types.delete().where(
            event_types.c.code.in_(
                [
                    "POTHOLE",
                    "WASTE",
                    "STREET_LIGHT",
                    "WATER_LEAK",
                ]
            ),
            event_types.c.module == "SMART_REPORT",
        )
    )