"""create initial diagnosis tables"""

from alembic import op
import sqlalchemy as sa

revision = "20260902_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "diseases",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_table(
        "symptoms",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("label", sa.String(180), nullable=False),
        sa.Column("affected_part", sa.String(30), nullable=False),
    )
    op.create_table(
        "questions",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("answer_type", sa.String(30), nullable=False),
        sa.Column("affected_part", sa.String(30), nullable=True),
    )
    op.create_table(
        "rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("disease_id", sa.String(80), sa.ForeignKey("diseases.id"), nullable=False),
        sa.Column("definition", sa.JSON(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
    )
    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("disease_id", sa.String(80), sa.ForeignKey("diseases.id"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
    )
    op.create_table(
        "diagnosis_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
    )
    op.create_table(
        "diagnosis_answers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("diagnosis_sessions.id"), nullable=False),
        sa.Column("question_id", sa.String(100), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
    )
    op.create_table(
        "diagnosis_results",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("diagnosis_sessions.id"), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    for table in [
        "diagnosis_results",
        "diagnosis_answers",
        "diagnosis_sessions",
        "recommendations",
        "rules",
        "questions",
        "symptoms",
        "diseases",
    ]:
        op.drop_table(table)

