# from database import engine
# from models import Base

# Base.metadata.create_all(bind=engine)

# print("Database Created")

from database.database import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

print("Database Created")