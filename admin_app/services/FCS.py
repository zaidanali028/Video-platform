import pyrebase
import os
import constants

# AN FCS CLOUD UTIL TO HELP ME PURPOSELY FOR UPLOADING LARGER MIDEA FILES
class Uploader:
    def __init__(self):
        firebase = pyrebase.initialize_app({
        "apiKey": constants.API_KEY,
        "authDomain":constants.AUTH_DOMAIN,
        "projectId": constants.PROJECT_ID,
        "storageBucket":constants.STORAGE_BUCKET,
        "messagingSenderId": constants.MESSAGING_SENDER_ID,
        "appId": constants.APP_ID,
        "measurementId": constants.MEASUREMENT_ID,
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