import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv, set_key
from datetime import datetime
from db_connection import client
from logger import logger


dotenv_path = r"C:\Users\Mehme\Masaüstü\Projects\BadBoysProject\key_rotation\.env"
load_dotenv(dotenv_path)
MASTER_3DES_KEY = os.getenv("MASTER_3DES_KEY")
#MASTER_3DES_KEY = '420ef55580b71d9e7668df1aa77765f1345d743663f9822c'

db = client["BadBoys"]
dek_key_collection = db["3DES_DEKS"]
oldest_dek_doc = dek_key_collection.find_one(sort=[("_id", -1)])
oldest_dek_doc = oldest_dek_doc["dek"]




password_text = 'deneme'

print('MASTER_3DES_KEY', MASTER_3DES_KEY)
print('DEK_KEY', oldest_dek_doc)

def des3_algorithm_encrypt(text, master_key, dek_key) -> bytes:
    
    master_key = des3_algorithm_decrypt(master_key, dek_key) 
    print(master_key.hex())
    cipher = DES3.new(master_key, DES3.MODE_ECB)
    encrypted = cipher.encrypt(pad(text.encode(), DES3.block_size))
    return encrypted.hex()

def des3_algorithm_decrypt(encrypted_hex, key_hex) -> bytes:
    cipher = DES3.new(bytes.fromhex(key_hex), DES3.MODE_ECB)
    decrypted = cipher.decrypt(bytes.fromhex(encrypted_hex))
    return decrypted


def des3_encrypt_master_key(master_key_hex: str, dek_key_hex: str) -> str:
    master_bytes = bytes.fromhex(master_key_hex)
    dek_bytes = bytes.fromhex(dek_key_hex)
    cipher = DES3.new(dek_bytes, DES3.MODE_ECB)
    encrypted = cipher.encrypt(master_bytes)
    return encrypted.hex()

#decrpt doğru olamyabilir
#MODE_CBC, MODE_ECB arasında bir tercih yap
#print(des3_algorithm_encrypt(password_text, MASTER_3DES_KEY, '0a025049d48ae660b118f4fcef934fd8f424bdb5ad059859'))
#print(des3_algorithm_encrypt(password_text, MASTER_3DES_KEY, DEK_KEY))


#print(des3_encrypt_master_key(MASTER_3DES_KEY, DEK_KEY))

print(des3_algorithm_encrypt(password_text, MASTER_3DES_KEY, oldest_dek_doc))