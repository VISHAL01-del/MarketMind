from src.database.connection import Base,engine
from src.database import models

Base.metadata.create_all(bind=engine)

print("MarketMind database tables created successfully")