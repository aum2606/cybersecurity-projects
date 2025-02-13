import argparse
from typing import Tuple

class TextSteganography:
    """zero width characters for encoding"""
    ZERO_WIDTH_CHARS = {
        '0': '\u200b',
        '1': '\u200c',
    }

    @staticmethod
    def text_to_binary(text: str)->str:
        """convert text to binary string"""
        return ''.join(format(ord(char),'08b') for char in text)

    @staticmethod
    def binary_to_text(binary: str)->str:
        """convert binary string to text"""
        return ''.join(chr(int(binary[i:i+8],2)) for i in range(0,len(binary),8))

    def hide_message(self,secret_message:str,cover_text:str)->str:
        """hide secret message within cover text using zero-width characters"""
        binary_secret = self.text_to_binary(secret_message)

        #convert binary to zero-width characters
        hidden_text = ''.join(self.ZERO_WIDTH_CHARS[bit] for bit in binary_secret)

        #insert the hidden text after the first character of the cover text
        return cover_text[0] + hidden_text + cover_text[1:]

    def reveal_message(self,steganographic_text:str)->str:
        """Extract hidden message from steganographic text"""
        #create reverse mapping of zero-width characters
        reverse_map = {v: k for k,v in self.ZERO_WIDTH_CHARS.items()}

        #extract the hidden binary message
        binary_message = ''
        for char in steganographic_text:
            if char in reverse_map:
                binary_message += reverse_map[char]


        #convert binary back to text
        try:
            return self.binary_to_text(binary_message)
        except:
            return "No hidden message found"

def main():
    parser = argparse.ArgumentParser(description='Text Steganography Tool')
    parser.add_argument('--mode',choices=['hide','reveal'],required=True,help='Operation mode: hide or reveal')
    parser.add_argument('--message', help='Secret message to hide (required for hide mode)')
    parser.add_argument('--cover', help='Cover text (required for hide mode)')
    parser.add_argument('--stego-text', help='Steganographic text (required for reveal mode)')
    
    args = parser.parse_args()
    stego = TextSteganography()

    if args.mode == 'hide':
        if not args.message or not args.cover:
            print("Error: Both message and cover text are required for hide mode")
            return
        result = stego.hide_message(args.message,args.cover)
        print("\nSteganographic text: ")
        print(result)
    else:
        if not args.stego_text:
            print("Error: Steganographic text is required for reveal mode")
            return
        result = stego.reveal_message(args.stego_text)
        print("\nRevealed message: ")
        print(result)



if __name__ == '__main__':
    main()