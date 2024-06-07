import pyrebase
import os
import environ


# AN FCS CLOUD UTIL TO HELP ME PURPOSELY FOR UPLOADING LARGER MIDEA FILES
class Uploader:
    def __init__(self):
        env = environ.Env()
        firebase = pyrebase.initialize_app({
        "apiKey": env('API_KEY'),
        "authDomain": env('AUTH_DOMAIN'),
        "projectId": env('PROJECT_ID'),
        "storageBucket": env('STORAGE_BUCKET'),
        "messagingSenderId": env('MESSAGING_SENDER_ID'),
        "appId": env('APP_ID'),
        "measurementId": env('MEASUREMENT_ID'),
        "databaseURL": ""
    })
        self.storage = firebase.storage()
    
    def upload(self, file_path):
        # get file name from media_file path
        file_name = file_path.name
        
        #store the file in firebase 
        self.storage.child(file_name).put(file_path) 
        
        # get the url or return none
        return self.storage.child(file_name).get_url(None)