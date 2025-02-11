#include <boost/uuid/detail/md5.hpp>
#include <boost/algorithm/hex.hpp>
#include <iostream>
#include <string>
#include <vector>

class CryptoTool {
private:
    std::string key;

    std::string getMD5(const std::string& input) {
        boost::uuids::detail::md5 hash;
        boost::uuids::detail::md5::digest_type digest;

        hash.process_bytes(input.data(), input.size());
        hash.get_digest(digest);

        const auto charDigest = reinterpret_cast<const char*>(&digest);
        std::string result;
        boost::algorithm::hex(charDigest, charDigest + sizeof(boost::uuids::detail::md5::digest_type), std::back_inserter(result));

        return result;
    }

    std::string xorWithKey(const std::string& input) {
        std::string output = input;
        std::string hashedKey = getMD5(key);

        for (size_t i = 0; i < input.length(); ++i) {
            output[i] = input[i] ^ hashedKey[i % hashedKey.length()];
        }

        return output;
    }

public:
    CryptoTool(const std::string& encryptionKey = "DefaultKey123") : key(encryptionKey) {}

    std::string encrypt(const std::string& plaintext) {
        std::string encrypted = xorWithKey(plaintext);
        std::string hexOutput;
        boost::algorithm::hex(encrypted.begin(), encrypted.end(), std::back_inserter(hexOutput));
        return hexOutput;
    }

    std::string decrypt(const std::string& ciphertext) {
        std::string decoded;
        try {
            boost::algorithm::unhex(ciphertext, std::back_inserter(decoded));
            return xorWithKey(decoded);
        }
        catch (const boost::algorithm::hex_decode_error& e) {
            std::cerr << "Decoding error: " << e.what() << std::endl;
            return "";
        }
    }
};

int main() {
    CryptoTool crypto("MySecretKey123");
    std::string input;
    char choice;

    while (true) {
        std::cout << "\n1. Encrypt\n2. Decrypt\n3. Exit\nChoice: ";
        std::cin >> choice;
        std::cin.ignore();

        if (choice == '3') break;

        std::cout << "Enter text: ";
        std::getline(std::cin, input);

        if (choice == '1') {
            std::cout << "Encrypted: " << crypto.encrypt(input) << std::endl;
        }
        else if (choice == '2') {
            std::cout << "Decrypted: " << crypto.decrypt(input) << std::endl;
        }
    }

    return 0;
}