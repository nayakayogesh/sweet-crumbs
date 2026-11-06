"""
create 5 models:
users (id, name, email/phone, password_hash, role: customer/admin)
products (id, name, price, is_available)
orders (id, user_id, order_date, status, notes, total)
order_items (order_id, product_id, quantity, price_at_order)
daily_capacity (date, max_orders, booked, is_blocked)
"""