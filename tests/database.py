from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(bind=engine)
