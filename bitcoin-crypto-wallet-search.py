import os
import hashlib
import datetime
import shutil
import re
import logging
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constant values
WALLET_EXTENSIONS = ['.dat', '.wallet', '.key', '.priv', '.pub', '.json', '.keystore']
WALLET_NAMES = ['wallet', 'bitcoin', 'ethereum', 'litecoin', 'dogecoin','solana']
WALLET_MAGIC_NUMBERS: Dict[str, bytes] = {
    'Bitcoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Ethereum': b'\x19\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    'Litecoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Dogecoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Solana': b'\x01\x00\x00\x00\x00\x00\x00\x00'
}
RECOVERY_PHRASE_FORMATS: List[str] = [
    r'\b(?:\w{11}\s){23}\w{11}\b',  # 24-word recovery phrase
    r'\b(?:\w{12}\s){23}\w{12}\b',  # 24-word recovery phrase with 12-word chunks
    r'\b(?:\w{3,}\s){11}\w{3,}\b'   # 12-word recovery phrase
]

def is_potential_wallet(file_path: str) -> Tuple[bool, str]:
    """
    Check if a file is a potential wallet based on name, extension, and magic numbers.
    """
    file_name = os.path.basename(file_path).lower()
    file_ext = os.path.splitext(file_name)[1]

    if any(ext in file_ext for ext in WALLET_EXTENSIONS) or any(name in file_name for name in WALLET_NAMES):
        return True, "Name/Extension match"

    try:
        with open(file_path, 'rb') as f:
            file_start = f.read(32)
            for wallet_type, magic_number in WALLET_MAGIC_NUMBERS.items():
                if file_start.startswith(magic_number):
                    return True, f"Magic number match: {wallet_type}"
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")

    return False, ""

def search_for_recovery_phrases(file_path: str) -> List[str]:
    """
    Search for potential recovery phrases in a file.
    """
    try:
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            phrases = []
            for pattern in RECOVERY_PHRASE_FORMATS:
                matches = re.findall(pattern, content)
                phrases.extend(matches)
            return phrases
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

def copy_file(src: str, dst: str) -> None:
    """
    Copy a file from source to destination.
    """
    try:
        shutil.copy2(src, dst)
        logging.info(f"Copied {src} to {dst}")
    except Exception as e:
        logging.error(f"Error copying {src} to {dst}: {e}")

def search_for_wallets(root_dir: str, output_dir: str) -> List[Dict[str, str]]:
    """
    Search for potential wallet files in the given directory.
    """
    wallets = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            is_wallet, reason = is_potential_wallet(file_path)
            
            if is_wallet:
                wallet_info = {
                    'path': file_path,
                    'name': file,
                   'size': os.path.getsize(file_path),
                    'created': datetime.datetime.fromtimestamp(os.path.getctime(file_path)),
                   'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)),
                   'reason': reason
                }
                wallets.append(wallet_info)
                logging.info(f"Potential wallet found: {file_path}")
                
                # Copy the wallet file to the output directory
                copy_file(file_path, output_dir)

    return wallets

def search_for_recovery_phrases_in_files(root_dir: str, output_dir: str) -> None:
    """
    Search for potential recovery phrases in files in the given directory.
    """
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            recovery_phrases = search_for_recovery_phrases(file_path)
            if recovery_phrases:
                phrase_file = os.path.join(output_dir, f"recovery_phrases_{os.path.basename(file_path)}.txt")
                with open(phrase_file, 'w') as f:
                    for phrase in recovery_phrases:
                        f.write(f"{phrase}\n")
                logging.info(f"Potential recovery phrases found in {file_path}. Saved to {phrase_file}")

def main() -> None:
    print("Cryptocurrency Wallet Recovery Suite")
    print("====================================")
    
    root_dir = input("Enter the root directory to search for wallets: ")
    output_dir = input("Enter the output directory to copy wallet files: ")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\nSearching for wallets and recovery phrases. This may take a while...")
    wallets = search_for_wallets(root_dir, output_dir)
    search_for_recovery_phrases_in_files(root_dir, output_dir)

    if wallets:
        print(f"\nFound {len(wallets)} potential wallet files:")
        for wallet in wallets:
            print(f"File: {wallet['name']}")
            print(f"Path: {wallet['path']}")
            print(f"Size: {wallet['size']} bytes")
            print(f"Created: {wallet['created']}")
            print(f"Modified: {wallet['modified']}")
            print(f"Reason: {wallet['reason']}")
            print("------------------------")
    else:
        print("\nNo potential wallet files found.")

    print(f"\nSearch complete. Check {output_dir} for copied wallet files and potential recovery phrases.")
    print("\nDonation addresses:")
    print("Bitcoin (BTC): bc1qpx6afau939qyq75gqj9rd563hycqq9p49sm8cz")
    print("Ethereum (ETH): 0xdB279940091d6358eFE9aFFc99500984B8B2F88E")
    print("Solana (SOL): AFwuzo3E8zJd2dg362QuqyL18j5GZgpgVvHzoiY7hSsF")
    print("Polygon (MATIC): 0xdB279940091d6358eFE9aFFc99500984B8B2F88E")
    print("\nFor advanced recovery assistance, contact: emergency@aximinds.com")

if __name__ == "__main__":
    main()
