"""init

Revision ID: f41c68fccef0
Revises:
Create Date: 2025-02-04 14:56:24.518566

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f41c68fccef0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_number", sa.String(length=50), nullable=False),
        sa.Column("contract_date", sa.Date(), nullable=False),
        sa.Column("place_of_signing", sa.String(length=255), nullable=False),
        sa.Column("valid_date", sa.Date(), nullable=True),
        sa.Column("supplier_name", sa.String(length=255), nullable=False),
        sa.Column("supplier_representative", sa.String(length=255), nullable=False),
        sa.Column("supplier_address", sa.String(length=255), nullable=False),
        sa.Column("supplier_inn", sa.String(length=50), nullable=True),
        sa.Column("supplier_bik", sa.String(length=50), nullable=True),
        sa.Column("supplier_ogrn", sa.String(length=50), nullable=True),
        sa.Column("supplier_bank", sa.String(length=255), nullable=False),
        sa.Column("supplier_swift", sa.String(length=50), nullable=True),
        sa.Column("supplier_account", sa.String(length=50), nullable=False),
        sa.Column("buyer_name", sa.String(length=255), nullable=False),
        sa.Column("buyer_address", sa.String(length=255), nullable=False),
        sa.Column("buyer_bank", sa.String(length=255), nullable=False),
        sa.Column("buyer_swift", sa.String(length=50), nullable=True),
        sa.Column("buyer_account", sa.String(length=50), nullable=False),
        sa.Column("buyer_tax_id", sa.String(length=50), nullable=False),
        sa.Column("goods_name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price_per_unit", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("total_price", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("exchange_rate", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("delivery_terms", sa.String(length=50), nullable=False),
        sa.Column("incoterms", sa.String(length=50), nullable=False),
        sa.Column("claim_period", sa.Integer(), nullable=False),
        sa.Column("response_period", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_contracts_contract_number"),
        "contracts",
        ["contract_number"],
        unique=True,
    )
    op.create_index(op.f("ix_contracts_id"), "contracts", ["id"], unique=False)
    op.create_table(
        "addendums",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("addendum_number", sa.String(length=50), nullable=False),
        sa.Column("addendum_date", sa.Date(), nullable=False),
        sa.Column("invoice_number", sa.String(length=50), nullable=True),
        sa.Column("invoice_amount", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("exchange_rate", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contracts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_addendums_addendum_number"),
        "addendums",
        ["addendum_number"],
        unique=False,
    )
    op.create_index(op.f("ix_addendums_contract_id"), "addendums", ["contract_id"], unique=False)
    op.create_index(op.f("ix_addendums_id"), "addendums", ["id"], unique=False)
    op.create_index(
        op.f("ix_addendums_invoice_number"),
        "addendums",
        ["invoice_number"],
        unique=False,
    )
    op.create_table(
        "appendices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("appendix_number", sa.String(length=50), nullable=False),
        sa.Column("appendix_date", sa.Date(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_appendices_id"), "appendices", ["id"], unique=False)
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("invoice_number", sa.String(length=50), nullable=False),
        sa.Column("invoice_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contracts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_invoices_contract_id"), "invoices", ["contract_id"], unique=False)
    op.create_index(op.f("ix_invoices_id"), "invoices", ["id"], unique=False)
    op.create_index(op.f("ix_invoices_invoice_number"), "invoices", ["invoice_number"], unique=True)
    op.create_index(op.f("ix_invoices_status"), "invoices", ["status"], unique=False)
    op.create_table(
        "specifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("spec_number", sa.String(length=50), nullable=False),
        sa.Column("spec_date", sa.Date(), nullable=False),
        sa.Column("goods_description", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contracts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_specifications_contract_id"),
        "specifications",
        ["contract_id"],
        unique=False,
    )
    op.create_index(op.f("ix_specifications_id"), "specifications", ["id"], unique=False)
    op.create_index(
        op.f("ix_specifications_spec_number"),
        "specifications",
        ["spec_number"],
        unique=False,
    )
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoices.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payments_id"), "payments", ["id"], unique=False)
    op.create_index(op.f("ix_payments_invoice_id"), "payments", ["invoice_id"], unique=False)
    op.create_index(op.f("ix_payments_status"), "payments", ["status"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_payments_status"), table_name="payments")
    op.drop_index(op.f("ix_payments_invoice_id"), table_name="payments")
    op.drop_index(op.f("ix_payments_id"), table_name="payments")
    op.drop_table("payments")
    op.drop_index(op.f("ix_specifications_spec_number"), table_name="specifications")
    op.drop_index(op.f("ix_specifications_id"), table_name="specifications")
    op.drop_index(op.f("ix_specifications_contract_id"), table_name="specifications")
    op.drop_table("specifications")
    op.drop_index(op.f("ix_invoices_status"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_invoice_number"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_id"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_contract_id"), table_name="invoices")
    op.drop_table("invoices")
    op.drop_index(op.f("ix_appendices_id"), table_name="appendices")
    op.drop_table("appendices")
    op.drop_index(op.f("ix_addendums_invoice_number"), table_name="addendums")
    op.drop_index(op.f("ix_addendums_id"), table_name="addendums")
    op.drop_index(op.f("ix_addendums_contract_id"), table_name="addendums")
    op.drop_index(op.f("ix_addendums_addendum_number"), table_name="addendums")
    op.drop_table("addendums")
    op.drop_index(op.f("ix_contracts_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_contract_number"), table_name="contracts")
    op.drop_table("contracts")
    # ### end Alembic commands ###
