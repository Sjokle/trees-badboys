from db_connection import client
from datetime import datetime


def logger(ID=None, stepcode= None, stepname=None, message=None):

    try:
        db = client["BadBoys"]
        db["DES3_DEKS_LOGS"].insert_one({
            "3DES_DEKS_ID": ID,
            "stepcode": stepcode,
            "stepname": stepname,
            "message": message
        })
    except Exception as e:
        print("Logger hatası:", e)




        