import string
import secrets
import os 
import math

def calculate_entropy(pool_size, length):
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)

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
    if not all(required_sets):
        return "ERROR_INSUFFICIENT_CHARS"
        
    if not filtered_chars:
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

def interactive_password_saver():
    password_file = "passwords.txt"
    
    print("✨ Welcome to the Interactive Password Generator (v4.0)! ✨")
    print("➡️  Guarantees: 1 Uppercase, 1 Lowercase, 1 Digit, 1 Symbol.")
    print("-" * 40)
    
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
        
        while True:
            action = input(
                "Options: (s)ave, (r)egenerate, or (e)xit? [s/r/e]: "
            ).lower()
            
            if action in ('s', 'save'):
                login_info = input("Enter the login/website/service this is for: ")
                
                try:
                    with open(password_file, 'a') as f:
                        f.write(f"Service: {login_info}\n")
                        f.write(f"Password: {current_password}\n")
                        f.write(f"Length: {length} / Pool Size (N): {pool_size} / Entropy: {entropy_bits:.2f} bits\n")
                        f.write(f"Exclusions: {exclude_input if exclude_input else 'None'}\n")
                        f.write("-" * 20 + "\n")
                    print(f"\n✅ Password for **{login_info}** saved successfully to {password_file}.")
                except IOError as e:
                    print(f"❌ Error saving file: {e}")
                
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

    print("\n👋 Thank you for using the generator. Goodbye!")

if __name__ == "__main__":
    interactive_password_saver()