
#include <iostream>
#include <string>
#include <regex>
using namespace std;

class PasswordStrengthChecker {
private:
    //Criteria weights
    const int LENGTH_WEIGHT = 20;
    const int COMPLEXITY_WEIGHT = 20;
    const int UNIQUENESS_WEIGHT = 50;

    // check the length of password
    int checkLength(const string& password)const {
        if (password.length() < 8) return 0;
        if (password.length() < 12) return 0;
        if (password.length() < 16) return 0;
        return 20;
    }

    // check complexity (mix of characters types)
    int checkComplexity(const string& password) const {
        bool hasLower = regex_search(password, regex("[a-z]"));
        bool hasUpper = regex_search(password, regex("[A-Z]"));
        bool hasDigit = regex_search(password, regex("\\d"));
        bool hasSpecial = regex_search(password, std::regex("[!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]"));

        int complexity = 0;
        if (hasLower) complexity += 1;
        if (hasUpper) complexity += 1;
        if (hasDigit) complexity += 1;
        if (hasSpecial) complexity += 1;

        return complexity * 10;
    }

    //check for uniqueness (avoiding common patterns)
    int checkUniqueness(const string& password) const {
        //check against common password patterns

        vector<string> commonPatterns = {
            "123","abc","qwerty","password","admin"
        };

        for (const auto& pattern : commonPatterns) {
            if (password.find(pattern) != string::npos) {
                return 0;
            }
        }

        //penalize sequential or repeated characters
        bool hasSequential = regex_search(password, std::regex("(.)\\1{2,}"));
        bool hasSequence = regex_search(password, std::regex("(012|123|234|345|456|567|678|789|987|876|765|654|543|432|321|210)"));

        return hasSequential || hasSequence ? 10 : 50;
    }

public:
    //main method to assess password strength
    int assessPasswordsStrength(const string& password) const {
        int lengthScore = checkLength(password);
        int complexityScore = checkComplexity(password);
        int uniquessScore = checkUniqueness(password);


        int totalScore = (lengthScore * LENGTH_WEIGHT / 20) +
            (complexityScore * COMPLEXITY_WEIGHT / 40) +
            (uniquessScore * UNIQUENESS_WEIGHT / 50);

        return min(max(totalScore, 0), 100);
    }

    //Provide feedback on password strength
    string getStrengthFeedback(int score) const {
        if (score < 30) return "Weak Password";
        if (score < 60) return "Moderate Password";
        if (score < 80) return "Strong Password";

        return "Very Strong Password";
    }
};

int main()
{
    PasswordStrengthChecker checker;

    //Test different passwords
    vector<string> testPasswords = {
        "123456",
        "password",
        "Password123",
        "Str0ngP@ssw0rd!",
        "ComplexPassword2024!@#"
    };

    for (const auto& password : testPasswords) {
        int strength = checker.assessPasswordsStrength(password);
        cout << "Password: " << password << endl;
        cout << "Strength score: " << strength << endl;
        cout << "Feedback: " << checker.getStrengthFeedback(strength) << endl;
        cout << endl;
    }
    return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
