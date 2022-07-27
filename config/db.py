import databases
import sqlalchemy


metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine("sqlite:///video_hosting.db")
database = databases.Database("sqlite:///video_hosting.db")
