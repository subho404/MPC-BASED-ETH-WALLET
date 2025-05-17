import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from web3 import Web3
import secretsharing as sss  # Shamir's Secret Sharing

# Load environment variables
load_dotenv()
API_KEY = os.getenv("apikey")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Web3 connection to Sepolia Testnet
NODE_URL = f"https://sepolia.infura.io/v3/{API_KEY}"
web3 = Web3(Web3.HTTPProvider(NODE_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network!")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["crypto_wallet"]
transactions_collection = db["transactions"]

# USB Paths for 3 shares (update if needed)
USB1_PATH = "E:\\pendrive1_share.txt"
USB2_PATH = "F:\\pendrive2_share.txt"
USB3_PATH = "G:\\pendrive3_share.txt"

# Initialize Flask app
app = Flask(__name__)

# Check Ethereum balance
def check_balance(address):
    if not web3.is_address(address):
        return {"error": "Invalid wallet address!"}
    balance = web3.eth.get_balance(address)
    return {"balance": web3.from_wei(balance, 'ether')}

# Split private key into 3 shares (used only if needed)
def split_private_key():
    if not PRIVATE_KEY:
        raise ValueError("Private key is missing! Check your .env file.")
    if not PRIVATE_KEY.startswith("0x"):
        raise ValueError("Private key must start with '0x' and be in hex format.")
    cleaned_key = PRIVATE_KEY[2:]
    shares = sss.SecretSharer.split_secret(cleaned_key, 3, 2)
    return shares

# Save shares to pendrives
def save_shares_to_pendrives():
    shares = split_private_key()
    try:
        with open(USB1_PATH, "w") as f1:
            f1.write(shares[0])
        with open(USB2_PATH, "w") as f2:
            f2.write(shares[1])
        with open(USB3_PATH, "w") as f3:
            f3.write(shares[2])
        print("✅ Shares saved successfully to USBs.")
    except Exception as e:
        print(f"❌ Error saving shares: {e}")

# Read a share from a USB file
def read_share_from_pendrive(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Error reading share from {path}: {e}")

# Reconstruct private key from any 2 of 3 USBs
def reconstruct_private_key():
    shares = []
    for path in [USB1_PATH, USB2_PATH, USB3_PATH]:
        share = read_share_from_pendrive(path)
        if share:
            shares.append(share)

    if len(shares) < 2:
        raise Exception("🔐 Key reconstruction failed: Please insert at least two USB drives.")

    try:
        recovered_key = sss.SecretSharer.recover_secret(shares)
        return "0x" + recovered_key
    except Exception as e:
        raise Exception(f"⚠️ Key reconstruction error: {e}")

# Send Ethereum transaction
def send_eth(sender_address, recipient, amount, name):
    if not web3.is_address(sender_address) or not web3.is_address(recipient):
        return {"error": "Invalid wallet address."}

    try:
        reconstructed_key = reconstruct_private_key()
    except Exception as e:
        return {"error": str(e)}

    try:
        amount_wei = web3.to_wei(amount, 'ether')
        nonce = web3.eth.get_transaction_count(sender_address)

        transaction = {
            "to": Web3.to_checksum_address(recipient),
            "value": amount_wei,
            "gas": 21000,
            "gasPrice": web3.to_wei("50", "gwei"),
            "nonce": nonce,
            "chainId": 11155111  # Sepolia chain ID
        }

        signed_tx = web3.eth.account.sign_transaction(transaction, reconstructed_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        transactions_collection.insert_one({
            "name": name,
            "address": recipient,
            "amount": amount,
            "tx_hash": web3.to_hex(tx_hash),
            "status": "success"
        })

        return {"tx_hash": web3.to_hex(tx_hash)}

    except Exception as e:
        transactions_collection.insert_one({
            "name": name,
            "address": recipient,
            "amount": amount,
            "status": "failed"
        })
        return {"error": f"No Gas to send transaction: {e}"}

# Flask Routes
@app.route("/")
def home():
    return render_template("index.html", wallet_address=WALLET_ADDRESS)

@app.route("/check_balance", methods=["POST"])
def balance():
    address = request.form["wallet_address"]
    return jsonify(check_balance(address))

@app.route("/send_eth", methods=["POST"])
def send():
    sender_address = request.form["wallet_address"]
    recipient = request.form["recipient_address"]
    amount = request.form["amount_ether"]
    name = request.form["recipient_name"]
    return jsonify(send_eth(sender_address, recipient, amount, name))

# Start Flask app
if __name__ == "__main__":
    if not os.path.exists(USB1_PATH):
        save_shares_to_pendrives()
    app.run(debug=True)
