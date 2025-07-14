import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
from loguru import logger
from datetime import datetime


class postgres_conn:
    def __init__(self):
        self.host = "10.0.0.143"
        self.port = 5432
        self.database = "timecard"
        self.table = "timecard"
        self.user = "test"
        self.password = "password"
        self.conn = pg.connect(
            database=self.database,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    def query(self, query):
        df = pd.read_sql(query, self.conn)
        self.conn.close()
        return df

    def insert_df(self, data, table, if_exists):
        df = data
        df.to_sql(name=table, con=self.engine, if_exists=if_exists, index=False)
        self.conn.close()
        return f'[+] "{table}" inserted successfully'


class postgres_conn_tst:
    def __init__(self):
        self.host = "10.0.0.143"
        self.port = 5432
        self.database = "timecard"
        self.table = "timecard"
        self.user = "test"
        self.password = "password"
        self.conn = pg.connect(
            database=self.database,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    def query(self, query):
        df = pd.read_sql(query, self.conn)
        self.conn.commit()
        return df

    def insertDf(self, data, table, if_exists):
        df = data
        df.to_sql(name=table, con=self.engine, if_exists=if_exists, index=False)
        self.conn.commit()
        return f'[+] "{table}" inserted successfully'

    def writeTimeStamp(
        self,
    ):
        
        logger.info("Write Timestamp")

        nextAction = {"clock_in": "clock_out", "clock_out": "clock_in"}

        lastAction = self.query("select action from timecard order by time desc").iloc[
            0, 0
        ]
        logger.info("Last Action:", lastAction)

        self.insertDf(
            data=pd.DataFrame({"action": [nextAction.get(lastAction)]}),
            table="timecard",
            if_exists="append",
        )

        logger.info("Write Timestamp Success")

        return logger.info(f"{datetime.today()} {nextAction.get(lastAction)}")
