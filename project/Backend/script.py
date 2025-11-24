from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

def verify_master_key(master_key_hex, dek_key_hex, current_key_hex):

    master_key_bytes = bytes.fromhex(master_key_hex)
    dek_key_bytes = bytes.fromhex(dek_key_hex)
    current_key_bytes = bytes.fromhex(current_key_hex)
    
    cipher = DES3.new(dek_key_bytes, DES3.MODE_ECB)
    
    try:
        # decrypt ederken unpad kullanabiliriz, ancak key genelde tam block boyu olduğundan gerek yok
        decrypted = cipher.decrypt(current_key_bytes)
        if decrypted == master_key_bytes:
            return True
        else:
            return False
    except ValueError as e:
        print("Decrypt hatası:", e)
        return False


MASTER_3DES_KEY = 'a667f63c57ebbfaf55116ade1278c495ef6cd0f32081d40f'
DEK_KEY = '25cb0c3b6a016082489c7e3788c17a9c7c0780466df2833c'
MEVCUT_KEY = 'dae5f1213863fdf5689cb230c83ed2717944c5ca8e7ff122'

result = verify_master_key(MASTER_3DES_KEY, DEK_KEY, MEVCUT_KEY)
print("MASTER key doğru mu?", result)















from Crypto.Cipher import DES3

def encrypt_master_key(master_key_hex, dek_key_hex):
    master_bytes = bytes.fromhex(master_key_hex)
    dek_bytes = bytes.fromhex(dek_key_hex)

    cipher = DES3.new(dek_bytes, DES3.MODE_ECB)
    
    from Crypto.Util.Padding import pad
    master_bytes_padded = master_bytes
    
    encrypted = cipher.encrypt(master_bytes_padded)
    return encrypted.hex()


MASTER_3DES_KEY = 'a667f63c57ebbfaf55116ade1278c495ef6cd0f32081d40f'
DEK_KEY = '25cb0c3b6a016082489c7e3788c17a9c7c0780466df2833c'

MEVCUT_KEY = encrypt_master_key(MASTER_3DES_KEY, DEK_KEY)
print("MEVCUT_KEY (şifrelenmiş):", MEVCUT_KEY)
