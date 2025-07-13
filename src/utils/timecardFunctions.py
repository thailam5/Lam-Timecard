from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from loguru import logger


def calcTime(startTime: datetime, endTime: datetime):

    if endTime is not None:
        workTime = endTime - startTime

    else:
        workTime = startTime - startTime

    return round(workTime.seconds / 3600, 2)


def tableCleanUp(df):

    try:
        df["Worked (hrs)"] = df.apply(
            lambda x: calcTime(x.clock_in, x.clock_out), axis=1
        )
        df["clock_in"] = df.clock_in.apply(
            lambda x: (
                x.strftime("%H:%M")
                if type(x) is not pd._libs.tslibs.nattype.NaTType
                else np.nan
            )
        )
        df["clock_out"] = df.clock_out.apply(
            lambda x: (
                x.strftime("%H:%M")
                if type(x) is not pd._libs.tslibs.nattype.NaTType
                else np.nan
            )
        )

        df.rename(
            columns={"date": "Date", "clock_in": "Start", "clock_out": "End"},
            inplace=True,
        )

    except Exception as e:
        logger.error(e)
        df = pd.DataFrame()
    return df


def getDateRange():

    todays_date = date.today()

    start_date = todays_date + timedelta(
        days=1 - todays_date.isoweekday(),
    )

    end_date = todays_date + timedelta(
        days=5 - todays_date.isoweekday(),
    )

    pay_date = todays_date + timedelta(
        days=6 - todays_date.isoweekday() - 1,
    )

    return todays_date, start_date, end_date, pay_date


def dataPrep(df: pd.DataFrame):
    if df.shape[0] == 0:
        df_display = pd.DataFrame(
            {"Date": [], "Start": [], "End": [], "Worked (hrs)": []}
        )

    else:

        df_display = tableCleanUp(df.copy())

    return df_display


def calcPay(df: pd.DataFrame):
    try:
        pay = df["Worked (hrs)"].sum() * 14

    except Exception as e:
        logger.error(e)
        pay = 0.00

    return pay
