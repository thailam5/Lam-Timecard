import pandas as pd
import numpy as np
import psycopg2 as pg
from sqlalchemy import create_engine, text
from loguru import logger
from datetime import datetime

class postgres_conn():
    def __init__(self):
        self.host = '10.0.0.28'
        self.port = 5432
        self.database = 'timecard'
        self.table = 'timecard'
        self.user = 'test'
        self.password = 'password'
        self.conn = pg.connect(
            database = self.database
            ,host = self.host
            ,port = self.port
            ,user = self.user
            ,password = self.password
        )
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

    def query(self, query):
        df = pd.read_sql(query, self.conn)
        self.conn.close()
        return df
    
    def insert_df(self, data, table, if_exists):
        df = data
        df.to_sql(name = table, con = self.engine, if_exists = if_exists, index = False)
        self.conn.close()
        return f'[+] "{table}" inserted successfully'
    

class postgres_conn_tst():
    def __init__(self):
        self.host = '10.0.0.28'
        self.port = 5432
        self.database = 'timecard'
        self.table = 'timecard'
        self.user = 'test'
        self.password = 'password'
        self.conn = pg.connect(
            database = self.database
            ,host = self.host
            ,port = self.port
            ,user = self.user
            ,password = self.password
        )
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

    def query(self, query):
        df = pd.read_sql(query, self.conn)
        self.conn.commit()
        return df
    
    def insertDf(self, data, table, if_exists):
        df = data
        df.to_sql(name = table, con = self.engine, if_exists = if_exists, index = False)
        self.conn.commit()
        return f'[+] "{table}" inserted successfully'
    
    def writeTimeStamp(self,):

        nextAction = {"clock_in": "clock_out", "clock_out": "clock_in"}

        lastAction = self.query("select action from timecard order by time desc").iloc[0,0]
        logger.info("Last Action:", lastAction)

        self.insertDf(
            data=pd.DataFrame({
                "action": [nextAction.get(lastAction)]
            }),
            table="timecard",
            if_exists="append"
        )
        
        return logger.info(f"{datetime.today()} {nextAction.get(lastAction)}")
    

def calcTime(startTime: datetime, endTime: datetime):
    
    if endTime is not None:
        workTime = endTime - startTime

    else:
        workTime = startTime - startTime

    return round(workTime.seconds/3600, 2)
    

def tableCleanUp(df):

    try:
        df["Worked (hrs)"] = df.apply(lambda x: calcTime(x.clock_in, x.clock_out), axis=1)
        df["clock_in"] = df.clock_in.apply(lambda x: x.strftime("%H:%M") if type(x) is not pd._libs.tslibs.nattype.NaTType else np.nan)
        df["clock_out"] = df.clock_out.apply(lambda x: x.strftime("%H:%M") if type(x) is not pd._libs.tslibs.nattype.NaTType else np.nan)



        df.rename(columns={
            "date": "Date",
            "clock_in": "Start",
            "clock_out": "End"
        }, inplace=True)

    except:
        df = pd.DataFrame()
    return df