import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import os
import time

# --------------------------
# כתובות הדפים לבדיקה
# --------------------------
URLS = [
    "https://ipo.presglobal.store/order/2386",
    "https://ipo.presglobal.store/order/2387",
    "https://ipo.presglobal.store/order/2388"
]

# --------------------------
# משתני סביבה (מהגדרות ב-Railway)
# --------------------------
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
MY_PHONE = os.getenv("MY_PHONE")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(body):
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE,
            to=MY_PHONE
        )
        print(f"✅ SMS נשלח! SID: {message.sid}")
    except Exception as e:
        print(f"❌ שגיאה בשליחת SMS: {e}")

# --------------------------
# פונקציה לבדוק זמינות כרטיסים
# --------------------------
def check_tickets():
    for url in URLS:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            sold_out = soup.find("span", string="Sold out")

            if sold_out:
                print(f"❌ Sold out בעמוד: {url}")
            else:
                print(f"🎉 כרטיסים זמינים בעמוד: {url}")
                send_sms(f"🎉 כרטיסים זמינים! כנסי מהר: {url}")
                return True  # עצור אחרי שמוצאים כרטיסים
        except Exception as e:
            print(f"שגיאה בבדיקה של {url}: {e}")
    return False

# --------------------------
# לולאת בדיקה כל 10 דקות
# --------------------------
if __name__ == "__main__":
    while True:
        found = check_tickets()
        if found:
            break  # עצור אחרי שמצאת כרטיסים
        print("💤 מחכה 10 דקות לבדיקה הבאה...")
        time.sleep(600)  # 600 שניות = 10 דקות
