import argparse

from PasswordCracker import PasswordCracker


def main():
    parser = argparse.ArgumentParser(description='ZIP File Password cracker')
    parser.add_argument('zip_file',help='Path to the ZIP file')
    parser.add_argument('wordlist', help='Path to the wordlist file')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads (default: 4)')
    args = parser.parse_args()
    
    try:
        cracker = PasswordCracker(args.zip_file,args.wordlist,args.threads)
        password = cracker.crack()
        if password:
            print(f"Password found: {password}")
        else:
            print("Password not found")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()