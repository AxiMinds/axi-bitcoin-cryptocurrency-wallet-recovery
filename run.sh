#!/bin/bash

# Function to check and install dependencies
check_and_install_dependencies() {
    echo "Checking dependencies..."

    # Check if Python is installed
    if ! command -v python3 &> /dev/null
    then
        echo "Python 3 is not installed. Please install Python 3.6 or higher and try again."
        exit 1
    fi

    # Check if virtualenv is installed
    if ! python3 -c "import virtualenv" &> /dev/null
    then
        echo "Installing virtualenv..."
        pip3 install virtualenv
    fi

    # Create a virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating a virtual environment..."
        python3 -m venv venv
    fi

    # Activate the virtual environment
    echo "Activating the virtual environment..."
    source venv/bin/activate

    # Install missing requirements
    echo "Installing missing requirements..."
    pip3 install -r requirements.txt
}

# Function to run the wallet recovery tool
run_wallet_recovery() {
    echo "Running the wallet recovery tool..."
    python3 wallet_recovery_suite.py
}

# Function to display the README
display_readme() {
    echo "Displaying the README..."
    cat README.md | less
}

# Function to display the menu
display_menu() {
    echo "
========================================
Wallet Recovery Suite
========================================
1. Check and Install Dependencies
2. Run Wallet Recovery
3. Display README
4. Quit
========================================
"
    read -p "Enter your choice [1-4]: " choice
    case $choice in
        1)
            check_and_install_dependencies
            press_enter_to_continue
            ;;
        2)
            run_wallet_recovery
            press_enter_to_continue
            ;;
        3)  
            display_readme
            press_enter_to_continue
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            press_enter_to_continue
            ;;
    esac
}

# Function to wait for user input before continuing
press_enter_to_continue() {
    read -p "Press Enter to continue..."
    clear
}

# Main script
while true
do
    display_menu
done
