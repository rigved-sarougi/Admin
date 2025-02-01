from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///sales.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # 'admin' or 'distributor'

class SalesRecord(Base):
    __tablename__ = 'sales_records'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    outlet_name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    owner_name = Column(String(100), nullable=False)
    contact_number = Column(String(15), nullable=False)
    gstin_un = Column(String(20), nullable=False)
    products_ordered = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_value = Column(Float, nullable=False)
    payment_status = Column(String(20), default='Pending')
    delivery_status = Column(String(20), default='Pending')
    remarks = Column(String(200))
    distributor_id = Column(Integer, ForeignKey('users.id'))

# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Pre-populate users
def populate_users():
    session = Session()
    users = [
        {"username": "admin1", "password": "12345", "role": "admin"},
        {"username": "admin2", "password": "12345", "role": "admin"},
        {"username": "distributor1", "password": "12345", "role": "distributor"},
        {"username": "distributor2", "password": "12345", "role": "distributor"},
        {"username": "distributor3", "password": "12345", "role": "distributor"},
        {"username": "distributor4", "password": "12345", "role": "distributor"},
    ]
    for user in users:
        if not session.query(User).filter(User.username == user["username"]).first():
            new_user = User(username=user["username"], password=user["password"], role=user["role"])
            session.add(new_user)
    session.commit()
    session.close()

# Run the population function
populate_users()
