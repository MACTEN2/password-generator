🔐 Strong Password Generator & Manager

Overview

This Python application provides a command-line interface (CLI) tool for generating cryptographically strong, random passwords. It uses the secure secrets module to ensure high-quality randomness, helping users create unique passwords to enhance digital security and limit the risk of password guessing.

The tool includes an interactive loop that allows users to view a generated password, save it with a corresponding login service, or regenerate a new one until they are satisfied.

✨ Features
- Cryptographically Secure Generation: Utilizes Python's secrets module for generating high-entropy, unpredictable passwords.
- Guaranteed Complexity: Ensures every generated password includes a mix of uppercase letters, lowercase letters, digits, and special characters.
- Interactive Control: Users can accept, save, or reject a generated password in real-time.
- Custom Length: Allows the user to specify the desired length for the password (default is 16 characters).
- Simple Storage: Saves accepted passwords along with the service name to a local file (passwords.txt).

⚠️ Important Security Warning

'DO NOT use this tool for long-term, production-level storage of sensitive passwords'.

The application saves passwords to a plain text file (passwords.txt) on your local machine. This is done for demonstration and ease of use, but it is not secure against unauthorized access.

For real-world password management, please use dedicated, encrypted software like LastPass, 1Password, Bitwarden, or your browser's built-in manager.

🚀 How to Run the Script

Prerequisites

You only need a working installation of Python 3.

Running the Program

Execute: Open your terminal or command prompt, navigate to the directory where you saved the file, and run the following command:
- python3 main.py


🛠️ Usage Guide (Interactive Mode)

The script will launch the interactive tool:

Set Length: When prompted, enter the desired password length (e.g., 12, 16, or press Enter to use the default of 16).

View and Choose: The script will immediately generate and display a new password:

========================================
Generated Password (16 chars): **A$sD9fG!hJ2kL3mP**
========================================


Select an Action: You will be prompted with three options:

(s) Save: The program will ask for the service (e.g., "Netflix Login"). It will then save the password and the service name to passwords.txt and ask if you wish to generate another.

(r) Regenerate: The program will discard the current password and instantly generate a new one.

(e) Exit: The program will terminate.

Example Interaction

Enter desired password length (default 16): 18

... Password Generated ...

Options: (s)ave, (r)egenerate, or (e)xit? [s/r/e]: s
Enter the login/website/service this is for (e.g., Google, Bank): Personal Email

✅ Password for **Personal Email** saved successfully to passwords.txt.

Generate another password? [y/n]: n

👋 Thank you for using the generator. Goodbye!