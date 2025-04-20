# backend/routes/key_ops.py

import rsa
import os

KEY_DIR = "certs"
os.makedirs(KEY_DIR, exist_ok=True)

def generate_keys():
    public_key, private_key = rsa.newkeys(2048)

    with open(f"{KEY_DIR}/public_key.pem", "wb") as pub_file:
        pub_file.write(public_key.save_pkcs1("PEM"))

    with open(f"{KEY_DIR}/private_key.pem", "wb") as priv_file:
        priv_file.write(private_key.save_pkcs1("PEM"))

    return {
        "message": "Keys generated successfully.",
        "public_key_path": f"{KEY_DIR}/public_key.pem",
        "private_key_path": f"{KEY_DIR}/private_key.pem"
    }

def load_keys():
    with open(f"{KEY_DIR}/public_key.pem", "rb") as pub_file:
        public_key = rsa.PublicKey.load_pkcs1(pub_file.read())

    with open(f"{KEY_DIR}/private_key.pem", "rb") as priv_file:
        private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())

    return public_key, private_key
