import databases
import sqlalchemy


DATABASE_URL = "sqlite:///video_hosting.db"

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
database = databases.Database(DATABASE_URL)
