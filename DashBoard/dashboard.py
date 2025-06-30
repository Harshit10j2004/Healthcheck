import requests
import mysql.connector
import random
from dotenv import load_dotenv
import os
import logging


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

load_dotenv(os.getenv("DOTENV_PATH", "healthcheck.env"))




class Dashborad:

    def __init__(self):
        self.con = mysql.connector.connect(
                host=os.getenv("db_host"),
                user=os.getenv("db_user"),
                password=os.getenv("db_password"),
                database=os.getenv("db_database"),
                port=int(os.getenv("db_port"))
            )


        self.cursor = self.con.cursor()

    def adduser(self):

        try:

            print("Welcome to healthcheck for signup fill details")

            id = random.randint(1000,9999)
            name = input("Enter your name: ")
            email = input("Enter your email: ")



            mail_response = requests.post("http://emailapi:8000/signup_mail",data={"email": email})

            if mail_response.status_code != 200:
                print("Failed to send OTP:", mail_response.json())
                logging.error("During signup dashboard is not getting response from signup email api")
                return

            print("OTP sent to your email.")



            otp_sent = mail_response.json().get("otp")

            getotp = int(input("enter the otp: "))



            if(otp_sent == getotp):



                url = input("Enter the url: ")

                payload = {
                    "id": id,
                    "name": name,
                    "email": email,
                    "url": url
                }

                final_response = requests.post("http://loginandsignupapi:8001/signup", data=payload)
                if final_response.status_code == 200:
                    print("response", final_response.json().get("response"))
                else:
                    print("Failed to save user:", final_response.json())
                    logging.error("During signup dashboard is not getting response from signupapi")

        except Exception as e:

            logging.error(f"Error occur during signup {e}")

            print(e)



    def login(self):

        try:


                print("Welcome to healthcheck ")


                email = input("Enter your email: ")

                self.cursor.execute(f"select email from user where email = %s",(email,))
                isitavi = self.cursor.fetchone()

                if isitavi is not None:


                    mail_response = requests.post("http://emailapi:8000/login_mail", data={"email": email})

                    if mail_response.status_code != 200:
                        print("Failed to send OTP:", mail_response.json())
                        logging.error("During login dashboard is not getting response from login email api")
                        return

                    print("OTP sent to your email.")

                    response_json = mail_response.json()


                    otp_sent = int(response_json.get("otp"))

                    getotp = int(input("enter the otp: "))

                    if (otp_sent == getotp):
                        payload = {

                                "email": email
                            }

                        final_response = requests.post("http://loginandsignupapi:8001/login", data=payload)
                        if final_response.status_code == 200:
                            print(final_response.json())
                        else:
                            logging.error("During login dashboard is not getting response from login api")
                            print("Login failed")

                    else:
                        print("wrong otp")

                else:
                    print("user not found")
                    logging.info("unregistered user tried to enter!")


        except Exception as e:
            logging.error(f"Error occur in dashboard during login {e}")
            print(e)

d = Dashborad()
while True:

    ope = input("Login/Signup/Exit: ")

    if ope == 'Login':
        d.login()

    elif ope == 'Signup':

        d.adduser()

    elif ope == 'Exit':
        break
