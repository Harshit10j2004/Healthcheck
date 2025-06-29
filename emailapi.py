import random
import mysql.connector
import smtplib
from fastapi import FastAPI,Form
from email.mime.text import MIMEText
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import uvicorn

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



sender = os.getenv("email_mail")
app_password = os.getenv("email_password")

class AlertData(BaseModel):
    email: str
    url: str
    response_time: int
    threshold: int = 400

emailapp = FastAPI()

@emailapp.post("/signup_mail")
def signupmail(email: str = Form(...)):

    otp = random.randint(100000,999999)

    subject = f"HealthMonitor - Your Secure signup Code"
    body = (f"YOUR OTP FOR SIGNUP {otp} \n Please do not share this with anyone, \n Thank you team heathmoniter")

    message = MIMEText(body, "plain")
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender,app_password)
            server.sendmail(sender,email,message.as_string())

        con = mysql.connector.connect(
            host=os.getenv("db_host"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            database=os.getenv("db_database"),
	        port=int(os.getenv("db_port"))
        )

        cursor = con.cursor()


        sql = "insert into otp (otp,email) values (%s,%s) on duplicate key update otp = values(otp)"
        values = (otp,email)
        cursor.execute(sql,values)
        con.commit()
        cursor.close()
        con.close()
        return {"otp": otp, "status": "mail sent"}


    except Exception as e:

        logging.error(f"!for signup mail error raised! {e}")

        return{"issue": str(e)}


@emailapp.post("/login_mail")
def loginmail(email: str = Form(...)):

    otp = random.randint(100000,999999)

    subject = f"HealthMonitor - Your Secure login Code"
    body = (f"YOUR OTP FOR Login {otp} \n Please do not share this with anyone, \n Thank you team heathmoniter")

    message = MIMEText(body, "plain")
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender,app_password)
            server.sendmail(sender,email,message.as_string())

        con = mysql.connector.connect(
            host=os.getenv("db_host"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            database=os.getenv("db_database"),
	        port=int(os.getenv("db_port"))

        )

        cursor = con.cursor()


        sql = "insert into otplogin (otp,email) values (%s,%s) on duplicate key update otp = values(otp)"
        values = (otp,email)
        cursor.execute(sql,values)
        con.commit()
        cursor.close()
        con.close()
        return {"otp": otp, "status": "mail sent"}

    except Exception as e:

        logging.error(f"!for logging mail error raised! {e}")

        return{"issue": str(e)}


@emailapp.post("/alert_mail")
def alertmail(data : AlertData):

    if data.response_time > data.threshold:


        subject = f"HealthMonitor - ALERT CHECK HEALTH"
        body = (f"THIS MESSAGE IS FROM HEALTHMONITOR, \n YOUR WEBSITE RESPONSE TIME IS SLOW VISIT HEALTHCHECK TO CHECK RESPONSETIME, \n THANK YOU TEAM HEALTHMONITER")

        message = MIMEText(body, "plain")
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = data.email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender, app_password)
                server.sendmail(sender, data.email, message.as_string())

            return{"trigger" : "mail send"}

        except Exception as e:

            logging.error(f"Error raised during send alert mail {e}")

            return {"issue": str(e)}

    return{"trigger" : "no need"}

if __name__ == "__main__":
        uvicorn.run("emailapi:emailapp", host="0.0.0.0", port=8000)

