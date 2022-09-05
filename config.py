import os

FLASK_ENV = 'development'
SECRET_KEY = "jsdkjskdjskdjskdjksjdskjd" or os.urandom(24)
DB_USER = "postgres"
DB_PASSWORD = "master"
GOOGLE_CLIENT_ID = "716315622451-lctgplmftgu6rpe8rt38d2t3r08ftaja.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
GOOGLE_BUCKET_JSON = "crypto-arcade-361520-afa8796cac9d.json"
GOOGLE_BUCKET_NAME = "crypto-arcade-361520.appspot.com"
GOOGLE_BUCKET_PATH = "https://storage.cloud.google.com/crypto-arcade-361520.appspot.com/"
GITHUB_CLIENT_ID = "947abf350821249b4f50"
GITHUB_CLIENT_SECRET = "ce1f8ca39fdab9cc5117f45de82c4e09e684716b"
