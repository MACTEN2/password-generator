import string
import secrets
import os 
import math
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- File Names ---
ENCRYPTED_FILE = "passwords.encrypted"
KEY_FILE = "master_key.key" # Stores the securely derived encryption key

# --- Helper Function: Key Derivation (KDF) ---
def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

# --- Helper Function: Master Key Management ---
def get_master_key():
    if os.path.exists(KEY_FILE):
        # Key file exists: Ask for master password to load and decrypt
        print("\n🔒 Accessing Encrypted Vault...")
        try:
            with open(KEY_FILE, 'rb') as f:
                salt = f.read(16)
                stored_key = f.read()
        except IOError:
            print("❌ Error reading key file. Vault may be corrupted.")
            return None

        for attempt in range(1, 4): # Give the user 3 tries
            master_password = input(f"Enter Master Password to unlock vault (Attempt {attempt}/3, type 'e' to exit): ")
            
            # NEW FEATURE: Check for exit command
            if master_password.lower() in ('e', 'exit'):
                print("🛑 Vault access canceled by user. Exiting.")
                return None

            derived_key = derive_key(master_password, salt)
            
            if derived_key == stored_key:
                print("✅ Vault unlocked successfully.")
                return Fernet(derived_key)
            else:
                print(f"❌ Invalid Master Password. {3 - attempt} attempts remaining.")
        
        print("🛑 Too many failed attempts. Exiting.")
        return None

    else:
        # Key file does not exist: First run setup
        print("\n🔑 First-Time Setup: Create Master Password")
        while True:
            master_password = input("Create a strong Master Password (will be used to encrypt all data): ")
            confirm_password = input("Confirm Master Password: ")
            if master_password == confirm_password and master_password:
                break
            print("Passwords do not match or are empty. Please try again.")

        salt = os.urandom(16)
        derived_key = derive_key(master_password, salt)
        
        try:
            with open(KEY_FILE, 'wb') as f:
                f.write(salt)
                f.write(derived_key)
            print(f"✅ Master key saved to {KEY_FILE}. Keep this file secret!")
            return Fernet(derived_key)
        except IOError:
            print("❌ Error writing key file. Cannot proceed.")
            return None

# --- Helper Function: Entropy Calculation ---
def calculate_entropy(pool_size, length):
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)

# --- Core Password Generation Function ---
def generate_strong_password(length=12, exclude_chars=""):
    all_characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    filtered_chars = "".join(c for c in all_characters if c not in exclude_chars)
    
    allowed_upper = "".join(c for c in string.ascii_uppercase if c not in exclude_chars)
    allowed_lower = "".join(c for c in string.ascii_lowercase if c not in exclude_chars)
    allowed_digits = "".join(c for c in string.digits if c not in exclude_chars)
    allowed_punctuation = "".join(c for c in string.punctuation if c not in exclude_chars)
    
    required_sets = [allowed_upper, allowed_lower, allowed_digits, allowed_punctuation]
    if not all(required_sets) or not filtered_chars:
        return "ERROR_INSUFFICIENT_CHARS"

    MIN_REQUIRED_LENGTH = 5 
    if length < MIN_REQUIRED_LENGTH:
        print(f"(Adjusted length from {length} to minimum required {MIN_REQUIRED_LENGTH})")
        length = MIN_REQUIRED_LENGTH
    
    password_list = [
        secrets.choice(allowed_upper),
        secrets.choice(allowed_lower),
        secrets.choice(allowed_digits),
        secrets.choice(allowed_punctuation),
        *(secrets.choice(filtered_chars) for _ in range(length - 4))
    ]

    secrets.SystemRandom().shuffle(password_list)
    
    pool_size = len(filtered_chars)

    return "".join(password_list), pool_size

# --- Interactive CLI Function ---
def interactive_password_saver():
    
    print("✨ Welcome to the Interactive Password Generator (v5.1 - Secure)! ✨")
    print("➡️  Guarantees: 1 Uppercase, 1 Lowercase, 1 Digit, 1 Symbol.")
    print("-" * 40)
    
    # 1. AUTHENTICATION AND KEY SETUP
    f = get_master_key()
    if f is None:
        return # Exit if authentication failed

    # 2. Get Customization Settings 
    while True:
        try:
            length = int(input("Enter desired password length (minimum 5, default 16): ") or 16)
            if length < 5:
                print("Length must be at least 5 to ensure complexity. Setting to 5.")
                length = 5
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    print("\n--- Character Exclusion ---")
    print("Some systems reject symbols like ' \" \\ < >")
    exclude_input = input("Enter any characters to EXCLUDE (or press Enter for none): ")
            
    # 3. Main Generation Loop
    running = True
    while running:
        
        result = generate_strong_password(length, exclude_input)
        
        if result == "ERROR_INSUFFICIENT_CHARS":
            print("\n🚨 Cannot generate password due to too many character exclusions. You must allow at least one of each: Uppercase, Lowercase, Digit, and Symbol.")
            running = False
            break

        current_password, pool_size = result
        entropy_bits = calculate_entropy(pool_size, length)

        print("\n" + "=" * 50)
        print(f"Generated Password ({length} chars)")
        print(f"Pool Size (N): {pool_size} characters | Entropy: {entropy_bits:.2f} bits")
        if entropy_bits < 128:
            print("❗ Recommendation: For maximum security, aim for 128 bits of entropy. (Try using a longer password)")
        print("-" * 50)
        print(f"**{current_password}**")
        print("=" * 50)
        
        # 4. Ask the user for action (Save, Regenerate, or Exit)
        while True:
            action = input(
                "Options: (s)ave, (r)egenerate, or (e)xit? [s/r/e]: "
            ).lower()
            
            if action in ('s', 'save'):
                login_info = input("Enter the login/website/service this is for: ")
                
                # Format the data for saving
                data_to_save = (
                    f"Service: {login_info}\n"
                    f"Password: {current_password}\n"
                    f"Length: {length} / Pool Size (N): {pool_size} / Entropy: {entropy_bits:.2f} bits\n"
                    f"Exclusions: {exclude_input if exclude_input else 'None'}\n"
                    f"-" * 20 + "\n"
                )
                
                # ENCRYPT AND SAVE
                try:
                    encrypted_data = f.encrypt(data_to_save.encode())
                    with open(ENCRYPTED_FILE, 'ab') as enc_file:
                        enc_file.write(encrypted_data + b'\n') # Use \n to separate encrypted lines
                    print(f"\n✅ Password for **{login_info}** ENCRYPTED and saved successfully to {ENCRYPTED_FILE}.")
                except Exception as e:
                    print(f"❌ Error during encryption and saving: {e}")
                
                if input("Generate another password? [y/n]: ").lower() == 'n':
                    running = False
                break
                
            elif action in ('r', 'regenerate'):
                print("🔄 Generating a new password with the same settings...")
                break
                
            elif action in ('e', 'exit'):
                running = False
                break
                
            else:
                print("Invalid choice. Please enter 's', 'r', or 'e'.")

    print("\n👋 Thank you for using the secure generator. Goodbye!")

if __name__ == "__main__":
    interactive_password_saver()