import environ

env = environ.Env()




# cloudinary keys
CLOUDINARY_API_KEY=env('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET=env('CLOUDINARY_API_SECRET')
CLOUDINARY_CLOUD_NAME=env('CLOUDINARY_CLOUD_NAME')


# Firebase cloud storage keys
API_KEY=env('API_KEY')
AUTH_DOMAIN=env('AUTH_DOMAIN')
PROJECT_ID=env('PROJECT_ID')
STORAGE_BUCKET=env('STORAGE_BUCKET')
MESSAGING_SENDER_ID=env('MESSAGING_SENDER_ID')
APP_ID=env('APP_ID')
MEASUREMENT_ID=env('MEASUREMENT_ID')