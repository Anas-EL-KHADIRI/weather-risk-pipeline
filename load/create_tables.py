from load.database import engine
from load.models import Base
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully.")