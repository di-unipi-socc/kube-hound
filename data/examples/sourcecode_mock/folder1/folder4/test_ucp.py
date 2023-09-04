from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# AES encryption
def encrypt_aes(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def decrypt_aes(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# RSA encryption
def private():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_rsa(plaintext, public_key):
    key = RSA.import_key(public_key)
    cipher = key.encrypt(plaintext, None)[0]
    return cipher

def decrypt_rsa(ciphertext, private_key):
    key = RSA.import_key(private_key)
    plaintext = key.decrypt(ciphertext)
    return plaintext

# Usage example
plaintext = b"Hello, World!"

# AES encryption and decryption
aes_key = get_random_bytes(16)  # 16 bytes key for AES-128
ciphertext_aes = encrypt_aes(plaintext, aes_key)
decrypted_text_aes = decrypt_aes(ciphertext_aes, aes_key)

# RSA encryption and decryption
private_key, public_key = private()
ciphertext_rsa = encrypt_rsa(plaintext, public_key)
decrypted_text_rsa = decrypt_rsa(ciphertext_rsa, private_key)

print("Plaintext:", plaintext)
print("AES Ciphertext:", ciphertext_aes)
print("Decrypted AES Text:", decrypted_text_aes)
print("RSA Ciphertext:", ciphertext_rsa)
print("Decrypted RSA Text:", decrypted_text_rsa)

