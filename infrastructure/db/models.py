from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    block_number: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    block_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    parent_hash: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    mined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="block",
        cascade="all, delete-orphan",
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    chain_id: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    tx_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tx_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    block_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("blocks.id", ondelete="SET NULL"),
        index=True,
    )
    from_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    to_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    value: Mapped[Decimal] = mapped_column(Numeric(78, 0), default=0, nullable=False)
    gas_used: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="confirmed", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    block: Mapped[Block | None] = relationship(back_populates="transactions")
    token_transfers: Mapped[list["TokenTransfer"]] = relationship(
        back_populates="transaction",
        cascade="all, delete-orphan",
    )


class TokenTransfer(Base):
    __tablename__ = "token_transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tx_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("transactions.id", ondelete="SET NULL"),
        index=True,
    )
    tx_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    token_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    from_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    to_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(78, 0), default=0, nullable=False)
    raw_log: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    transaction: Mapped[Transaction | None] = relationship(back_populates="token_transfers")
