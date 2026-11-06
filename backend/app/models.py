"""
create 5 models:
"""
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, Date, Boolean, ForeignKey, Text, func, Enum
from decimal import Decimal
from datetime import date

from .database import Base

class OrderStatus(str, enum.Enum):
    pending_approval = "pending_approval"
    confirmed = "confirmed"
    preparing = "preparing"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"
    rejected = "rejected"

#users (id, name, email/phone, password_hash, role: customer/admin)
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(25), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(35), nullable=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str]= mapped_column(String(10), nullable=False)

# products (id, name, price, is_available)
class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String)
    product_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    product_available: Mapped[bool] = mapped_column(Boolean, default=False)

# orders (id, user_id, order_date, status, notes, total)
class Orders(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    items: Mapped[list["OrderItems"]] = relationship(back_populates="orders")
    order_date: Mapped[date] = mapped_column(server_default=func.now())
    pickup_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
                OrderStatus,
                native_enum=False,
                length=20
            ),
            default=OrderStatus.confirmed,
            )
    is_custom: Mapped[bool] = mapped_column(Boolean)
    notes: Mapped[str] = mapped_column(Text)
    total: Mapped[float] = mapped_column(Numeric(precision=2))

# order_items (order_id, product_id, quantity, price_at_order)
class OrderItems(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped["Orders"] = relationship(back_populates="order_items")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_order: Mapped[float] = mapped_column(Numeric(precision=2))

# daily_capacity (date, max_orders, booked, is_blocked)
class DailyCapacity(Base):
    __tablename__ = "daily_capacity"
    booking_date: Mapped[date] = mapped_column(Date, primary_key=True)
    max_orders: Mapped[int] = mapped_column(Integer)
    booked: Mapped[int] = mapped_column(Integer, default=0)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(
        Enum(
            OrderStatus,
            native_enum=False,
            length=20
        ),
        default=OrderStatus.confirmed,
    )
    note: Mapped[str] = mapped_column(Text)
    changed_at: Mapped[date] = mapped_column(Date)

class Settings(Base):
    __tablename__ = 'settings'
    default_max_orders: Mapped[int] = mapped_column(Integer, default=10)