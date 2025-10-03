from back.app.core.database import Base, engine
from back.app.models.user import User

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")