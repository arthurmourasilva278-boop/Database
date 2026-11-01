
from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class GuildSettings(Base):
    __tablename__ = 'guild_settings'
    guild_id = Column(BigInteger, primary_key=True)
    log_sales_channel_id = Column(BigInteger, nullable=True)
    log_general_channel_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MerchantProfile(Base):
    __tablename__ = 'merchant_profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(BigInteger, unique=True, nullable=False)
    roblox_nick = Column(String, nullable=False)
    discord_nick = Column(String, nullable=False)
    wallet_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(BigInteger, nullable=False)
    buyer_nick = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    status = Column(String, default="PENDING")
    receipt_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CommissionPayment(Base):
    __tablename__ = 'commission_payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(BigInteger, nullable=False)
    amount = Column(Float, nullable=False)
    paid_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    executor_id = Column(BigInteger, nullable=False)
    target_id = Column(BigInteger, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
