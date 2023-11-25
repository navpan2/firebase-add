firebase_config = {
    "apiKey": "AIzaSyBy6tm3udmXYPZ216ggqs6P2Up2owC6U4Q",
    "authDomain": "chalo-5e71c.firebaseapp.com",
    "databaseURL": "https://chalo-5e71c-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "chalo-5e71c",
    "storageBucket": "chalo-5e71c.appspot.com",
    "messagingSenderId": "485358834771",
    "appId": "1:485358834771:web:d4aa0d636433916a87a2a6"
}
from fastapi import FastAPI,BackgroundTasks , Request
import requests
from pyrebase import initialize_app
import httpx
app = FastAPI()

# Firebase configuration
async def keep_alive_request(receiver_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(receiver_url)
        print(f"Keep-alive request sent to {receiver_url}, Status Code: {response.status_code}")


firebase = initialize_app(firebase_config)

@app.get("/fetch_and_store_data")
def fetch_and_store_data(request: Request,url: str = "https://dailymo-api.onrender.com/dailymo/?reqUrl=https://dai.ly/k4Q1uMXJNjgzkHzEO2p&vidFormat=http-1080@60-0"):
    try:
        # Fetch data from the provided URL
        receiver_url = str(request.base_url)
        print(receiver_url)
        res=0
        while res!=200:
            response = requests.get(url)
            res=response.status_code
            background_tasks = BackgroundTasks()
            background_tasks.add_task(keep_alive_request, receiver_url)
            print(response.status_code)
        print(response.json())
        data_to_store = {"a":"a"}  # Assuming the response is in JSON format, adjust accordingly

        # Write data to Firebase Realtime Database
        db = firebase.database()
        db.child('finally').set(response.json())

        return {"status": "success", "message": "Data fetched and stored successfully." , "data_stored":response.json()}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
@app.get("/fetch")
def fetch_and_store_data():
    try:
        # Fetch data from the provided URL
        db = firebase.database()
        response=db.child("finally").child("url").get()
        return {"status": response.val()}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
