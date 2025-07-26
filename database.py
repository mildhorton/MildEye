from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from passlib.context import CryptContext

# 1. Setup a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Define the User model (no changes here)
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

# 3. Database engine setup (no changes here)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url) # echo=True is optional for less verbose logs

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# --- NEW DATABASE FUNCTIONS ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email)).first()

def create_user(email, password):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user