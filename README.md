# AxiMinds Bitcoin and Cryptocurrency Wallet Recovery Suite

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Version](https://img.shields.io/badge/version-1.2-green)

A powerful Python-based tool designed to recover long-lost cryptocurrency wallets from old hard drives. Originally created to help recover a brother's lost Bitcoin, this suite now supports multiple cryptocurrencies and advanced recovery techniques.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Wallets](#supported-wallets)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Donations](#donations)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Ethical Considerations](#ethical-considerations)

## Features
- Advanced search algorithms for wallet files using filenames, extensions, and magic numbers
- Multi-cryptocurrency support with wallet type and version identification
- Recovery phrase scanning in text files
- Automated copying of discovered wallets and phrases to a specified output directory
- Detailed metadata logging for found wallets (creation/modification dates, size, etc.)
- User-friendly command-line interface
- Extensible architecture for easy addition of new wallet types

## Installation
1. Ensure Python 3.6+ is installed on your system.
2. Clone the repository:
   ```
   git clone https://github.com/aximinds/axi-bitcoin-cryptocurrency-wallet-recovery.git
   ```
3. Navigate to the project directory:
   ```
   cd axi-bitcoin-cryptocurrency-wallet-recovery
   ```

## Usage
1. Run the `run.sh` script:
   ```
   bash run.sh
   ```
2. Choose an option from the menu:
   - `Check and Install Dependencies`: This option checks if Python and virtualenv are installed, creates a virtual environment if it doesn't exist, activates it, and installs missing requirements.
   - `Run Wallet Recovery`: This option runs the wallet recovery tool.
   - `Display README`: This option displays the README file.
   - `Quit`: This option exits the script.

3. Follow the prompts to enter the root directory to search and the output directory for recovered files.
4. Review console output and check the output directory for results.

### Quick Start Example
```bash
bash run.sh
# Choose "Check and Install Dependencies" from the menu
# Choose "Run Wallet Recovery" from the menu
Enter the root directory to search for wallets: /path/to/search
Enter the output directory to copy wallet files: /path/to/output
```

## Supported Wallets
- Bitcoin (BTC)
- Ethereum (ETH)
- Litecoin (LTC)
- Dogecoin (DOGE)
- Solana (SOL)

Each wallet type is identified using tailored detection methods, including file extensions, naming conventions, and unique binary signatures.

## Roadmap
1. Expand wallet support (e.g., Ripple, Cardano, Polkadot)
2. Enhance recovery phrase detection with AI-assisted algorithms
3. Develop a user-friendly GUI
4. Implement multi-threading for improved performance 
5. Add customizable search options (file types, size limits, date ranges)

## Contributing
We welcome contributions! Here's how you can help:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

## Donations
If this tool has helped you recover lost funds or you'd like to support its development, consider a donation:

- Bitcoin (BTC): `bc1qpx6afau939qyq75gqj9rd563hycqq9p49sm8cz`
- Ethereum (ETH): `0xdB279940091d6358eFE9aFFc99500984B8B2F88E`
- Solana (SOL): `AFwuzo3E8zJd2dg362QuqyL18j5GZgpgVvHzoiY7hSsF`
- Polygon (MATIC): `0xdB279940091d6358eFE9aFFc99500984B8B2F88E`

To share your success story or for additional recovery assistance, please contact us at emergency@aximinds.com.

## License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is provided for educational and recovery purposes only. Exercise extreme caution when dealing with cryptocurrency wallets and private keys. Ensure you have the legal right to access and search the drives you're analyzing. AxiMinds is not responsible for any loss of funds or legal issues arising from the use of this tool.

## Ethical Considerations
Please be aware that searching hard drives for cryptocurrency wallets without the clear consent of the owner raises serious ethical concerns around privacy and ownership rights. This tool should only be used for legitimate data recovery purposes with proper authorization from the data owner. 

We strongly caution against using or promoting this tool for any unethical or illegal activities. If your goal is authorized data recovery, we recommend working with reputable data recovery professionals who adhere to strict ethical guidelines.

As developers, our role is to create technology responsibly and promote its ethical use. We cannot condone or assist in any misuse of this tool. Please use this software only for its intended purpose and with full respect for individual privacy and property rights.

---

Developed by AxiMinds using advanced AI techniques, combining multiple models for optimal performance:

- Groq.com Llama-3.1 70B  
- Anthropic Claude-3.5-Sonnet & Claude-3-Opus
- Huggingface HuggingChat Llama-3.1 405B
- OpenAI GPT-4

For custom AI solutions or advanced recovery services, contact us at emergency@aximinds.com.
