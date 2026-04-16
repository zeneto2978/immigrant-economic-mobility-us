import pandas as pd
from sqlalchemy import create_engine

USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5433"
DATABASE = "immigrant_mobility_db"

CSV_PATH = "data/raw/immigrant_data.csv"
TABLE_NAME = "immigrant_data"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

df = pd.read_csv(CSV_PATH)

df.to_sql(
    TABLE_NAME,
    engine,
    if_exists="append",
    index=False
)

print("Dados carregados com sucesso no PostgreSQL.")