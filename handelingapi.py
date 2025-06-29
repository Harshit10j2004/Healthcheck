import mysql.connector
import time
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level= logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename = os.getenv("LOG_PATH", "logs/logs.txt"),
    filemode='a'
)

load_dotenv(os.getenv("DOTENV_PATH", "healthcheck.env"))



class urlcheck(BaseModel):
    url: str
    response_time: int
    percantage: int
    lastcheck: int
    status: int

handelapp = FastAPI()




def request_check(record):

    url = record[0]



    try:

        start = time.time()
        response = requests.get(url,timeout=5)
        end = time.time()
        current_time =((end-start)*1000)
        status = response.status_code
        lastcheck = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        con = mysql.connector.connect(
            host=os.getenv("db_host"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            database=os.getenv("db_database"),
	        port=int(os.getenv("db_port"))

        )

        cursor = con.cursor()

        cursor.execute("select response_time,email from user where url = %s",(url,))
        result = cursor.fetchone()

        if not result:
            print(f"[ERROR] URL '{url}' not found in database.")
            cursor.close()
            con.close()
            return

        last_time, email = result

        if last_time == 0 or current_time == last_time:
            percantage = 0

        else:

            percantage = round(((current_time - last_time) / last_time) * 100)

        sql = ("update user set response_time = %s,lastcheck = %s,percantage = %s,status = %s where url = %s")
        value = (current_time,lastcheck,percantage,status,url)

        cursor.execute(sql,value)



        if current_time > 1000:

            try:

                alert_data = {
                    "email": email,
                    "url": url,
                    "response_time": int(current_time),
                    "threshold": 1000
                }
                requests.post("http://emailapi:8000/alert_mail", json=alert_data)

            except Exception as e:
                logging.error(f"error occured during send alert request from handeling {e}")
                print(e)


        con.commit()
        cursor.close()
        con.close()


    except Exception as e:
        logging.error(f"Error occured in handeling {e}")
        print(e)


@handelapp.post("/handeling")
def handeling():

    try:

        con = mysql.connector.connect(
            host=os.getenv("db_host"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            database=os.getenv("db_database"),
	        port=int(os.getenv("db_port"))

        )

        cursor = con.cursor()



        pool = ThreadPool(5)

        cursor.execute("select url from user")
        url = cursor.fetchall()

        pool.map(request_check,url)

        pool.close()
        pool.join()


        return {"status": "completed", "total_checked": len(url)}

    except Exception as e:
        logging.error(f"Error occured in handeling api {e}")
        return{"issue" : str(e)}
