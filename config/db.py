import databases
import sqlalchemy


DATABASE_URL = "postgresql://postgres:postgres@postgres/video_hosting"

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
database = databases.Database(DATABASE_URL)
