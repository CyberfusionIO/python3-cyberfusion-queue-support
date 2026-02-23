"""Queue items: add {started,ended}_at

Revision ID: 19e77347a42d
Revises: 93c79cb2baba
Create Date: 2026-02-20 13:32:09.803951

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "19e77347a42d"
down_revision = "93c79cb2baba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("queue_items", schema=None) as batch_op:
        batch_op.add_column(sa.Column("started_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("ended_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("queue_items", schema=None) as batch_op:
        batch_op.drop_column("ended_at")
        batch_op.drop_column("started_at")
