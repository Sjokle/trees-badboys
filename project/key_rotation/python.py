import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv, set_key
from datetime import datetime
from db_connection import client
from logger import logger


dotenv_path = r"C:\Users\Mehme\Masaüstü\Projects\BadBoysProject\key_rotation\.env"
load_dotenv(dotenv_path)

MASTER_3DES_KEY = 'bcf179e34f90b36d92fb7ac16ca9b285cce9509783ad9886'

DEK_KEY  = '03857a845be30cdce678e78eb5a2304394d1d7472cb1a76c'

password_text = 'deneme'



def des3_algorithm_encrypt(text, master_key, dek_key) -> bytes:
    
    master_key = des3_algorithm_decrypt(master_key, dek_key) 
    print(master_key)
    cipher = DES3.new(master_key, DES3.MODE_ECB)
    encrypted = cipher.encrypt(pad(text.encode(), DES3.block_size))
    return encrypted.hex()

def des3_algorithm_decrypt(encrypted_hex, key_hex) -> bytes:
    cipher = DES3.new(bytes.fromhex(key_hex), DES3.MODE_ECB)
    decrypted = cipher.decrypt(bytes.fromhex(encrypted_hex))
    return decrypted

#decrpt doğru olamyabilir
#MODE_CBC, MODE_ECB arasında bir tercih yap

print(des3_algorithm_decrypt(MASTER_3DES_KEY, DEK_KEY).hex())