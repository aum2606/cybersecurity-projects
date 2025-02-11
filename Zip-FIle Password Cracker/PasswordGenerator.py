from typing import List
class PasswordGenerator:
    """Utility class for generating common password patterns"""
    @staticmethod
    def generate_common_variations(base_word:str)->List[str]:
        """Generate common variations of a given base word
        Args:
            base_word (str): The base word to generate variations from
        Returns:
            List[str]: A list of common variations of the base word
        """
        variations = []
        variations.appeand(base_word)
        
        # common number suffixes
        for i in range(100):
            variations.append(f"{base_word}{i}")
            variations.append(f"{base_word}{i:02d}")
            
        #common special character suffixes
        special_chars = ['!','@','#','$','%','*']
        for char in special_chars:
            variations.append(f"{base_word}{char}")
            variations.append(f"{base_word}{char}!")
            
        # Capitalization variations
        variations.append(base_word.capitalize())
        variations.append(base_word.upper())
        
        return variations