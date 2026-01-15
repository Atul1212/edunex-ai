import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        print(' SUCCESS: Database Connected! EduNex AI is ready.')
except Exception as e:
    print(f' ERROR: Connection Failed. Reason: {e}')

