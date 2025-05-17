# MPC-Based Ethereum Wallet

This project is a secure Ethereum wallet web application that uses **Shamir's Secret Sharing** (a form of Multi-Party Computation, MPC) to protect your private key. The wallet allows you to check your balance and send ETH on the Sepolia testnet, while ensuring your private key is never stored in a single location.

## Features

- **MPC Key Protection:** Your Ethereum private key is split into 3 shares using Shamir's Secret Sharing. Any 2 shares are required to reconstruct the key, protecting against single-point compromise.
- **USB Share Storage:** Each share is saved to a separate USB drive for physical security.
- **Web Interface:** Simple web UI to check wallet balance and send ETH.
- **Transaction Logging:** All transactions are logged in a local MongoDB database.
- **Sepolia Testnet Support:** Connects to Ethereum Sepolia testnet via Infura.

## Project Structure

```
.env
.gitignore
app.py
generate_share.py
templates/
    index.html
```

- **app.py**: Main Flask application. Handles web routes, wallet logic, and MPC key management.
- **generate_share.py**: Utility script to generate and save key shares to USB drives.
- **templates/index.html**: Web UI template.
- **.env**: Stores sensitive environment variables (API key, wallet address, private key).

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [MongoDB](https://www.mongodb.com/try/download/community) running locally
- 3 USB drives (for storing key shares)

### 2. Install Dependencies

```sh
pip install flask python-dotenv pymongo web3 secretsharing
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```
apikey=YOUR_INFURA_API_KEY
WALLET_ADDRESS=YOUR_ETH_ADDRESS
PRIVATE_KEY=YOUR_PRIVATE_KEY
```

**Never share your private key!**

### 4. Generate Key Shares

Plug in your 3 USB drives. Update the USB paths in `app.py` and `generate_share.py` if needed.

Run:

```sh
python generate_share.py
```

This will split your private key and save each share to a different USB drive.

### 5. Start MongoDB

Make sure MongoDB is running locally on the default port (`27017`).

### 6. Run the Application

```sh
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Usage

- **Check Balance:** The home page displays your wallet address and allows you to check its ETH balance.
- **Send ETH:** Enter the recipient's address, name, and amount. At least 2 USB drives with key shares must be plugged in to sign transactions.

## Security Notes

- **Private Key Protection:** The private key is never stored in full on disk. It is reconstructed in memory only when needed, using at least 2 out of 3 USB shares.
- **Physical Security:** Keep your USB drives in separate, secure locations.
- **Testnet Only:** This wallet is configured for the Sepolia testnet. Do not use with mainnet funds.

## Troubleshooting

- **USB Not Detected:** Ensure the USB paths in the code match your system.
- **MongoDB Connection Error:** Make sure MongoDB is running locally.
- **Infura Connection Error:** Check your API key and internet connection.

## License

This project is for educational purposes. Use at your own risk.

---

**Author: SUBHAM BISWAS (TECHNO INDIA UNIVERSITY 211001001009 BCS 4A)
