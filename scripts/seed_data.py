# scripts/seed_data.py
import asyncio
import os
import sys

sys.path.append(os.getcwd())

from sqlmodel import select
from app.core.database import async_session_maker
from app.models.user import User
from app.models.order import Order, OrderStatus

# 手动处理密码哈希
import bcrypt

def hash_password(password: str) -> str:
    """手动密码加密"""
    # 确保密码不超过 72 字节
    password = password[:72]
    # 使用 bcrypt 直接加密
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


async def seed_data():
    async with async_session_maker() as session:
        # 1. 创建测试账号
        test_users = [
            {"username": "alice", "email": "alice@example.com", "full_name": "Alice Wang", "password": "alice123", "is_admin": False},
            {"username": "bob", "email": "bob@example.com", "full_name": "Bob Smith", "password": "bob123", "is_admin": False},
            {"username": "admin", "email": "admin@example.com", "full_name": "Admin User", "password": "admin123", "is_admin": True}
        ]
        
        for user_data in test_users:
            result = await session.exec(select(User).where(User.username == user_data["username"]))
            existing_user = result.first()
            
            if not existing_user:
                print(f"🌱 Creating user: {user_data['username']}...")
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    password_hash=hash_password(user_data["password"]),
                    is_admin=user_data["is_admin"]
                )
                session.add(user)
                await session.flush()

        # 2. 为每个用户创建 Mock 订单
        for user_data in test_users:
            result = await session.exec(select(User).where(User.username == user_data["username"]))
            user = result.first()
            
            if user:
                # 检查用户是否已有订单
                result = await session.exec(select(Order).where(Order.user_id == user.id))
                orders = result.all()
                
                if not orders:
                    print(f"📦 Creating mock orders for user: {user.username}...")
                    
                    # 为 Alice 创建订单
                    if user.username == "alice":
                        order1 = Order(
                            order_sn="SN20240001",
                            user_id=user.id,
                            status=OrderStatus.SHIPPED,
                            total_amount=128.50,
                            items=[{"name": "运动内衣", "qty": 1, "price": 128.50}],
                            tracking_number="SF123456789",
                            shipping_address="上海市浦东新区张江高科技园区"
                        )
                        order2 = Order(
                            order_sn="SN20240002",
                            user_id=user.id,
                            status=OrderStatus.PENDING,
                            total_amount=50.00,
                            items=[{"name": "全棉袜子", "qty": 5, "price": 10.00}],
                            shipping_address="北京市朝阳区三里屯"
                        )
                        order3 = Order(
                            order_sn="SN20240003",
                            user_id=user.id,
                            status=OrderStatus.SHIPPED,  # 已发货，符合退货条件
                            total_amount=199.00,
                            items=[
                                {"name": "运动T恤", "qty": 1, "price": 99.00},
                                {"name": "运动短裤", "qty": 1, "price": 100.00}
                            ],
                            tracking_number="SF987654321",
                            shipping_address="上海市浦东新区张江高科技园区"
                        )
                        session.add_all([order1, order2, order3])
                    
                    # 为 Bob 创建订单
                    elif user.username == "bob":
                        order4 = Order(
                            order_sn="SN20240004",
                            user_id=user.id,
                            status=OrderStatus.DELIVERED,  # 已签收，符合退货条件
                            total_amount=599.00,
                            items=[{"name": "耐克篮球鞋", "qty": 1, "price": 599.00}],
                            tracking_number="SF555666777",
                            shipping_address="北京市海淀区中关村"
                        )
                        order5 = Order(
                            order_sn="SN20240005",
                            user_id=user.id,
                            status=OrderStatus.SHIPPED,
                            total_amount=299.00,
                            items=[{"name": "运动背包", "qty": 1, "price": 299.00}],
                            tracking_number="SF111222333",
                            shipping_address="广州市天河区珠江新城"
                        )
                        session.add_all([order4, order5])
            
        # 最终统一提交事务
        await session.commit()
        print("✅ Seed data completed.")

if __name__ == "__main__":
    asyncio.run(seed_data())