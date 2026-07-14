import os
import pandas as pd

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://"
    f"{os.getenv('mysql_user')}:"
    f"{os.getenv('mysql_password')}@"
    f"{os.getenv('mysql_host')}:"
    f"{os.getenv('mysql_port')}/"
    f"{os.getenv('mysql_database')}"
)