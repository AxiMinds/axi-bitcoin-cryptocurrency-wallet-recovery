import os
import shutil
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("wallet_recovery.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Constant values
WALLET_EXTENSIONS = ['.dat', '.wallet', '.key', '.priv', '.pub', '.json', '.keystore']
WALLET_NAMES = ['wallet', 'bitcoin', 'ethereum', 'litecoin', 'dogecoin', 'solana']
WALLET_MAGIC_NUMBERS: Dict[str, bytes] = {
    'Bitcoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Ethereum': b'\x19\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    'Litecoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Dogecoin': b'\x30\x82\x01\x0a\x02\x82\x01\x01\x00',
    'Solana': b'\x01\x00\x00\x00\x00\x00\x00\x00'
}
RECOVERY_PHRASE_FORMATS: List[str] = [
    r'\b(?:\w{11}\s){23}\w{11}\b',  # 24-word recovery phrase
    r'\b(?:\w{12}\s){23}\w{12}\b',  # 24-word with 12-word chunks
    r'\b(?:\w{3,}\s){11}\w{3,}\b'   # 12-word recovery phrase
]
EXCLUDED_FILE_EXTENSIONS = ['.exe', '.pyc', '.pem', '.pyd', '.dll', '.so']

def is_potential_wallet_file(file_path: Path) -> Tuple[bool, str]:
    """Check if a file is a potential wallet based on name, extension, and magic numbers."""
    file_name = file_path.name.lower()
    file_ext = file_path.suffix

    if file_ext in EXCLUDED_FILE_EXTENSIONS:
        return False, ""

    if any(ext in file_ext for ext in WALLET_EXTENSIONS) or \
       any(name in file_name for name in WALLET_NAMES):
        return True, "Name/Extension match"

    try:
        with file_path.open('rb') as file:
            file_start = file.read(32)
            for wallet_type, magic_number in WALLET_MAGIC_NUMBERS.items():
                if file_start.startswith(magic_number):
                    return True, f"Magic number match: {wallet_type}"
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return False, ""

def search_for_recovery_phrases(file_path: Path) -> List[str]:
    """Search for potential recovery phrases in a file."""
    if file_path.suffix in EXCLUDED_FILE_EXTENSIONS:
        return []

    try:
        with file_path.open('r', errors='ignore') as file:
            content = file.read()
            phrases = []
            for pattern in RECOVERY_PHRASE_FORMATS:
                matches = re.findall(pattern, content)
                phrases.extend(matches)
            return phrases
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return []

def copy_file(src: Path, dst: Path) -> None:
    """Copy a file from source to destination."""
    try:
        shutil.copy2(src, dst)
        logger.info(f"Copied {src} to {dst}")
    except IOError as e:
        logger.error(f"Error copying {src} to {dst}: {e}")

def search_for_wallets(root_dir: Path, output_dir: Path) -> List[Dict[str, str]]:
    """Search for potential wallet files in the given directory."""
    wallets = []
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and output_dir not in file_path.parents:
            is_wallet, reason = is_potential_wallet_file(file_path)
            if is_wallet:
                wallet_info = {
                    'path': str(file_path),
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'created': datetime.fromtimestamp(file_path.stat().st_ctime),
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                    'reason': reason
                }
                wallets.append(wallet_info)
                logger.info(f"Potential wallet found: {file_path}")
                copy_file(file_path, output_dir / file_path.name)
    return wallets

def search_for_recovery_phrases_in_files(root_dir: Path, output_dir: Path) -> None:
    """Search for potential recovery phrases in files in the given directory."""
    recovery_phrase_files = set()
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and output_dir not in file_path.parents:
            recovery_phrases = search_for_recovery_phrases(file_path)
            if recovery_phrases:
                phrase_file = output_dir / f"recovery_phrases_{file_path.name}.txt"
                recovery_phrase_files.add(str(phrase_file))
                with phrase_file.open('w') as file:
                    for phrase in recovery_phrases:
                        file.write(f"{phrase}\n")
    logger.info(f"Potential recovery phrases found in {len(recovery_phrase_files)} files.")
    logger.info(f"Saved recovery phrase files to {output_dir}")

def main() -> None:
    """Main function to run the wallet recovery suite."""
    print("Cryptocurrency Wallet Recovery Suite")
    print("====================================")
    root_dir = Path(input("Enter the root directory to search for wallets: "))
    output_dir = Path(input("Enter the output directory to copy wallet files: "))
    output_dir.mkdir(parents=True, exist_ok=True)
    print("\nSearching for wallets and recovery phrases. This may take a while...")
    wallets = search_for_wallets(root_dir, output_dir)
    search_for_recovery_phrases_in_files(root_dir, output_dir)
    if wallets:
        print(f"\nFound {len(wallets)} unique potential wallet files:")
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

if __name__ == "__main__":
    main()
