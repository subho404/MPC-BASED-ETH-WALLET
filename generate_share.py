import os
from dotenv import load_dotenv
from secretsharing import SecretSharer
import secretsharing as sss

# Load private key from .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# USB Paths (Update if needed)
USB1_PATH = "E:\\pendrive1_share.txt"
USB2_PATH = "F:\\pendrive2_share.txt"
USB3_PATH = "G:\\pendrive3_share.txt"  # NEW third share

def split_private_key():
    if not PRIVATE_KEY:
        raise ValueError("Private key is missing! Ensure it's set in the .env file.")

    if not PRIVATE_KEY.startswith("0x"):
        raise ValueError("Private key must start with '0x' and be in hex format.")

    # Remove the "0x" prefix before splitting
    private_key_cleaned = PRIVATE_KEY[2:]

    # Split the key into 3 shares, any 2 required to reconstruct
    shares = SecretSharer.split_secret(private_key_cleaned, 2, 3)

    print("🔹 Generated Share 1:", shares[0])
    print("🔹 Generated Share 2:", shares[1])
    print("🔹 Generated Share 3:", shares[2])

    return shares

def save_shares_to_pendrives():
    shares = split_private_key()
    try:
        with open(USB1_PATH, "w") as f1:
            f1.write(shares[0])
        with open(USB2_PATH, "w") as f2:
            f2.write(shares[1])
        with open(USB3_PATH, "w") as f3:
            f3.write(shares[2])

        print("✅ Shares saved successfully to all 3 USB drives.")

    except Exception as e:
        print(f"❌ Error saving shares to USB: {e}")

if __name__ == "__main__":
    save_shares_to_pendrives()
