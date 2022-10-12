import databases
import sqlalchemy


DATABASE_URL = "postgresql://postgres:postgres@postgres_db:5432/postgres"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/video_hosting"

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
database = databases.Database(DATABASE_URL)
