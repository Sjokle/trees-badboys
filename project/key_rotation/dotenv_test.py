from dotenv import load_dotenv, dotenv_values
import os



def get_env():
    config = dotenv_values() 
    masterkey = bytes.fromhex(config["MASTER_3DES_KEY"])
    print('masterkey ', masterkey.hex())
    return masterkey
print(get_env())