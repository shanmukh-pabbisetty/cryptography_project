from flask import Flask, request, jsonify, send_file
from routes.key_ops import generate_keys, load_keys
from routes.encrypt_ops import encrypt_message, decrypt_message
from routes.file_ops import encrypt_file, decrypt_file
from utils.helpers import (
    save_uploaded_file, read_file_bytes, write_file_bytes,
    ENCRYPTED_DIR, DECRYPTED_DIR
)
import os

# Initialize Flask app
app = Flask(name)

# Routes

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the RSA File Encryption API!"})

@app.route("/generate-keys", methods=["GET"])
def handle_generate_keys():
    """Generate RSA keys (public and private)"""
    result = generate_keys()
    return jsonify(result)

@app.route("/encrypt-message", methods=["POST"])
def handle_encrypt_message():
    """Encrypt a plain text message"""
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    encrypted_message = encrypt_message(message)
    return jsonify({"encrypted_message": encrypted_message})

@app.route("/decrypt-message", methods=["POST"])
def handle_decrypt_message():
    """Decrypt an encrypted message"""
    encrypted_message = request.json.get("encrypted_message")
    if not encrypted_message:
        return jsonify({"error": "No encrypted message provided"}), 400

    decrypted_message = decrypt_message(encrypted_message)
    return jsonify({"decrypted_message": decrypted_message})

@app.route("/encrypt-file", methods=["POST"])
def handle_encrypt_file():
    """Encrypt a file"""
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save the uploaded file
    original_path = save_uploaded_file(file)

    # Encrypt the file
    file_data = read_file_bytes(original_path)
    encrypted_data = encrypt_file(file_data)

    # Save the encrypted file
    encrypted_file_path = os.path.join(ENCRYPTED_DIR, f"encrypted_{file.filename}")
    write_file_bytes(encrypted_file_path, encrypted_data)

    # Return the encrypted file as a downloadable response
    return send_file(encrypted_file_path, as_attachment=True)

@app.route("/decrypt-file", methods=["POST"])
def handle_decrypt_file():
    """Decrypt a file"""
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save the encrypted file
    encrypted_file_path = save_uploaded_file(file)

    # Read the encrypted file data
    encrypted_data = read_file_bytes(encrypted_file_path)

    # Decrypt the file
    decrypted_data = decrypt_file(encrypted_data)

    # Save the decrypted file
    decrypted_file_path = os.path.join(DECRYPTED_DIR, f"decrypted_{file.filename}")
    write_file_bytes(decrypted_file_path, decrypted_data)

    # Return the decrypted file as a downloadable response
    return send_file(decrypted_file_path, as_attachment=True)

if name == 'main':
    app.run(debug=True)
