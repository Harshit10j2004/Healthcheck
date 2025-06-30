import mysql.connector
from fastapi import FastAPI, Form
from dotenv import load_dotenv
import os
import logging

load_dotenv(os.getenv("DOTENV_PATH", "healthcheck.env"))

log_path = os.getenv("LOG_PATH", "logs/logs.txt")
log_dir = os.path.dirname(log_path)

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level= logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename = log_path,
    filemode='a'
)


app = FastAPI()


@app.post("/signup")

def adduser(id: int = Form(...),name: str = Form(...) , email: str = Form(...) ,url : str = Form(...)):

        print("data coming")



        try:

            con = mysql.connector.connect(
                host=os.getenv("db_host"),
            	user=os.getenv("db_user"),
            	password=os.getenv("db_password"),
            	database=os.getenv("db_database"),
	    	    port=int(os.getenv("db_port"))

            )

            cursor = con.cursor()

            sql = (f"insert into user (id, name, email, url,response_time,lastcheck,percantage,status) values (%s,%s,%s,%s,%s,%s,%s,%s)")
            values = (id,name,email,url,0,None,0,0)

            cursor.execute(sql,values)
            con.commit()
            cursor.close()
            con.close()

            print("user saved")

            return{"response": f"user added {id}"}

        except Exception as e:

            logging.error(f"Error raised during db connection during adding user ,{e}")

            return{"issue" : str(e)}



@app.post("/login")
def login(email: str = Form(...)):


    con = mysql.connector.connect(
        	host=os.getenv("db_host"),
            	user=os.getenv("db_user"),
            	password=os.getenv("db_password"),
            	database=os.getenv("db_database"),
	    	    port=int(os.getenv("db_port"))
    )

    cursor = con.cursor()

    cursor.execute("select email from user where email = %s",(email,))
    letsee = cursor.fetchone()

    if not letsee:
        logging.info("!unauthrize user try to login!")
        return{"value" : "failed"}



    try:
            cursor.execute(f"select url,response_time,lastcheck,percantage from user where email = %s",(email,))

            rows = cursor.fetchone()

            if rows:

                url , response , lastcheck , percantage = rows

                dictresponse = {
                    "your url" : url,
                    "response time": response,
                    "last checked on" : lastcheck,
                    "the changement percantage from last check" : percantage
                }
            return{"result": dictresponse}

    except Exception as e:

            logging.error(f"Error raised during data showing to user {email} ,{e}")

            return{"issue" : str(e)}


if __name__ == "__main__":
    
    uvicorn.run("loginandsignupapi:app", host="0.0.0.0", port=8001)