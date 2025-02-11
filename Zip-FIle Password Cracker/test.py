# test_setup.py
import zipfile
import os

# Create test file
with open('test.txt', 'w') as f:
    f.write('This is a test file')

# Create password-protected ZIP
with zipfile.ZipFile('test.zip', 'w') as zf:
    zf.setpassword(b'secret123')
    zf.write('test.txt')

# Create wordlist
wordlist = """
password123
admin123
secret123
test123
mypass123
secure123
"""

with open('wordlist.txt', 'w') as f:
    f.write(wordlist)

print("Test environment setup complete!")
print("You can now run: python zip_cracker.py test.zip wordlist.txt")