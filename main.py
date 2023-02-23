import requests
import smtplib
from datetime import datetime
import dotenv
import os
import time

dotenv.load_dotenv()
email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]
to = os.environ["TO"]


MY_LAT = 1.352083 # Your latitude
MY_LONG = 103.819839 # Your longitude


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

def check_pos(my_lat, my_long, iss_lat, iss_long):

    if abs(iss_lat-my_lat) <= 5 and abs(iss_long-my_long) <=5:
        return True
    else:
        return False

def is_dark(sunrise, sunset, timenow):
    if timenow <= sunrise:
        return True
    elif timenow >= sunset:
        return True
    else:
        return False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

while True:
    time.sleep(60)
    if check_pos(MY_LAT, MY_LONG, iss_latitude, iss_longitude) and is_dark(sunrise, sunset, time_now):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(to_addrs=to, from_addr= email, msg="Subject:ISS Overhead!\n\nLook up!")

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.







