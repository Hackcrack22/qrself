import random
import os
import sys
from pathlib import Path

# Manually define a list of blacklisted numbers
BLACKLIST = [
    "52680070", "20966973", "51690273","03854069","02488471","80144618"# Add numbers you want to block
]

# Determine the correct storage path for QR codes
if sys.platform.startswith("linux") and "ANDROID_STORAGE" in os.environ:
    # Android (Termux)
    USER_PICTURES_PATH = Path.home() / "storage/shared/Pictures/Generated_QRCodes"
elif sys.platform.startswith("win"):
    # Windows
    USER_PICTURES_PATH = Path.home() / "Pictures" / "Generated_QRCodes"
else:
    # Linux/macOS
    USER_PICTURES_PATH = Path(__file__).parent / "Generated_QRCodes"

# Ensure the directory exists
os.makedirs(USER_PICTURES_PATH, exist_ok=True)

# Define the file to store generated codes
CODE_FILE_PATH = "generated_codes.txt"

def load_existing_codes():
    """Load existing codes from a file into a set."""
    if not os.path.exists(CODE_FILE_PATH):
        return set()

    with open(CODE_FILE_PATH, "r") as file:
        return set(line.strip() for line in file)

def save_code(code):
    """Save the new code to the text file."""
    with open(CODE_FILE_PATH, "a") as file:
        file.write(f"{code}\n")

def generate_qr_code(code):
    """Dynamically import and generate a QR code if requested."""
    try:
        import qrcode  # Import only if needed
        qr = qrcode.make(code)
        qr_path = USER_PICTURES_PATH / f"{code}.png"
        qr.save(qr_path)
        print(f"QR Code saved to: {qr_path}")
    except ImportError:
        print("Error: 'qrcode' module not found. Install it with: pip install qrcode[pil]")

def generate_unique_codes(count, generate_qr=False):
    """Generate multiple unique 8-digit codes."""
    existing_codes = load_existing_codes()
    generated_codes = []

    while len(generated_codes) < count:
        new_code = str(random.randint(10000000, 99999999))  # Generate an 8-digit number
        if new_code not in existing_codes and new_code not in BLACKLIST:
            save_code(new_code)
            generated_codes.append(new_code)
            if generate_qr:
                generate_qr_code(new_code)  # Generate and save QR code only if requested

    return generated_codes

def show_all_codes():
    """Read and print all generated codes."""
    if not os.path.exists(CODE_FILE_PATH) or os.stat(CODE_FILE_PATH).st_size == 0:
        print("\nNo codes have been generated yet.")
    else:
        print("\nPreviously Generated Codes:")
        with open(CODE_FILE_PATH, "r") as file:
            for line in file:
                print(line.strip())

# User menu
print("\n1. Generate unique codes (No QR Code)")
print("2. Generate unique codes with QR Codes")
print("3. Show all previously generated codes")

choice = input("\nChoose an option (1, 2, or 3): ")

if choice in ["1", "2"]:
    while True:
        try:
            count = int(input("How many codes do you want to generate? "))
            if count > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    generate_qr = choice == "2"
    unique_codes = generate_unique_codes(count, generate_qr)

    print("\nGenerated Codes:")
    for code in unique_codes:
        print(code)

elif choice == "3":
    show_all_codes()

else:
    print("\nInvalid choice. Please enter 1, 2, or 3.")

print("\nScript finished. Exiting...")
exit()
