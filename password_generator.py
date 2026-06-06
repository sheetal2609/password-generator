import random
import string
import json
import os
from datetime import datetime

SAVED_FILE = "saved_passwords.json"

def load_saved():
    if os.path.exists(SAVED_FILE):
        with open(SAVED_FILE, "r") as f:
            return json.load(f)
    return []

def save_password(saved, password, label):
    saved.append({
        "label": label,
        "password": password,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(SAVED_FILE, "w") as f:
        json.dump(saved, f, indent=4)
    print("✅ Password saved!")

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        print("❌ Please select at least one character type!")
        return None

    password = ''.join(random.choices(characters, k=length))
    return password

def check_strength(password):
    strength = 0
    feedback = []

    if len(password) >= 12:
        strength += 1
    else:
        feedback.append("Use at least 12 characters")

    if any(c.isupper() for c in password):
        strength += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c.islower() for c in password):
        strength += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        strength += 1
    else:
        feedback.append("Add numbers")

    if any(c in string.punctuation for c in password):
        strength += 1
    else:
        feedback.append("Add special characters")

    if strength == 5:
        level = "💪 VERY STRONG"
    elif strength == 4:
        level = "✅ STRONG"
    elif strength == 3:
        level = "🟡 MEDIUM"
    elif strength == 2:
        level = "🟠 WEAK"
    else:
        level = "❌ VERY WEAK"

    return level, feedback

def generate_menu():
    saved = load_saved()

    print("\n--- GENERATE PASSWORD ---")

    try:
        length = int(input("Enter password length (8-50): ").strip())
        if length < 8 or length > 50:
            print("❌ Length must be between 8 and 50!")
            return
    except ValueError:
        print("❌ Invalid length!")
        return

    print("\nSelect character types:")
    use_upper = input("Include UPPERCASE letters? (yes/no): ").strip().lower() == "yes"
    use_lower = input("Include lowercase letters? (yes/no): ").strip().lower() == "yes"
    use_digits = input("Include numbers (0-9)? (yes/no): ").strip().lower() == "yes"
    use_symbols = input("Include symbols (!@#$)? (yes/no): ").strip().lower() == "yes"

    password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)

    if password:
        print(f"\n  🔐 Generated Password: {password}")

        strength, tips = check_strength(password)
        print(f"  💡 Strength: {strength}")

        if tips:
            print("  📝 Tips to improve:")
            for tip in tips:
                print(f"     - {tip}")

        save = input("\nSave this password? (yes/no): ").strip().lower()
        if save == "yes":
            label = input("Enter a label (e.g. Gmail, Facebook): ").strip()
            save_password(saved, password, label)

def generate_multiple():
    print("\n--- GENERATE MULTIPLE PASSWORDS ---")
    try:
        count = int(input("How many passwords to generate? (1-10): ").strip())
        length = int(input("Password length (8-50): ").strip())
    except ValueError:
        print("❌ Invalid input!")
        return

    print("\n🔐 Generated Passwords:")
    print("-" * 40)
    for i in range(count):
        pwd = generate_password(length, True, True, True, True)
        if pwd:
            print(f"  {i+1}. {pwd}")
    print("-" * 40)

def view_saved():
    saved = load_saved()
    print("\n--- SAVED PASSWORDS ---")

    if not saved:
        print("❌ No saved passwords!")
        return

    for i, item in enumerate(saved, 1):
        print(f"\n  [{i}] Label    : {item['label']}")
        print(f"      Password : {item['password']}")
        print(f"      Saved on : {item['created_on']}")

def check_my_password():
    print("\n--- CHECK PASSWORD STRENGTH ---")
    password = input("Enter your password: ").strip()
    strength, tips = check_strength(password)
    print(f"\n  Password : {password}")
    print(f"  Strength : {strength}")
    if tips:
        print("  Tips:")
        for tip in tips:
            print(f"    - {tip}")

def main():
    print("=" * 45)
    print("       PASSWORD GENERATOR")
    print("       Created by: sheetal2609")
    print("=" * 45)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Generate Password")
        print("2. Generate Multiple Passwords")
        print("3. View Saved Passwords")
        print("4. Check Password Strength")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            generate_menu()
        elif choice == "2":
            generate_multiple()
        elif choice == "3":
            view_saved()
        elif choice == "4":
            check_my_password()
        elif choice == "5":
            print("\n✅ Goodbye!")
            break
        else:
            print("❌ Invalid choice! Enter 1-5.")

if __name__ == "__main__":
    main()
