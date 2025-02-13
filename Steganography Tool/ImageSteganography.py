from PIL import Image
import numpy as numpy
import argparse

class ImageSteganography:
    def __init__(self):
        self.delimiter = "$$END$$"

    def text_to_binary(self,text):
        """convert text to binary string"""
        binary = ''.join(format(ord(char),'08b') for char in text)
        return binary + ''.join(format(ord(char),'08b') for char in self.delimiter)

    def binary_to_text(self,binary):
        """convert binary string to text"""
        text = ''
        #convert each 8 bits to a character
        for i in range(0,len(binary),8):
            byte = binary[i:i+8]
            text += chr(int(byte,2))
            #check for delimiter
            if text.endswith(self.delimiter):
                return text[:-len(self.delimiter)]
        return text

    def hide_message(self,image_path:str,message:str,output_path:str)->bool:
        """hide message in image"""
        try:
            #load image
            img = image.open(image_path)

            #conever image to numpy array
            pixels = numpy.array(img)

            #convert message to binary
            binary_message = self.text_to_binary(message)

            if len(binary_message) > pixels.size:
                raise ValueError("Message too long for this image")

            #Flatten the array
            pixels = pixels.flatten()

            #modify the least significant bits
            for i in range(len(binary_message)):
                pixels[i] = (pixels[i] & ~1) | int(binary_message[i])

            #reshape array back to original shape
            pixels = pixels.reshape(img.size[1],img.size[0],-1)

            #save image
            result_img = Image.fromarray(pixels)
            result_img.save(output_path)
            return True
        except Exception as e:
            print(f"Error hiding message: {e}")
            return False

    def reveal_message(self,image_path:str)->str:
        """extract hidden message from an image"""
        try:
            #load the image
            img = Image.open(image_path)
            pixels = np.array(img)

            #extract the LSB of each pixel
            binary_message = ''
            pixels = pixels.flatten()

            for pixel in pixels:
                binary_message += str(pixel & 1)
                #try to convert to text periodically
                if len(binary_message) % 8 ==0:
                    text = self.binary_to_text(binary_message)
                    if self.delimiter in text:
                        return text
            return "No hidden messaeg found"
        except Exception as e:
            return f"Error revealing message: {e}"

def main():
    parser = argparse.ArgumentParser(description='Image Steganography Tool')
    parser.add_argument('--mode', choices=['hide', 'reveal'], required=True,
                      help='Operation mode: hide or reveal')
    parser.add_argument('--image', required=True,
                      help='Path to the image file')
    parser.add_argument('--message', 
                      help='Message to hide (required for hide mode)')
    parser.add_argument('--output',
                      help='Output image path (required for hide mode)')
    
    args = parser.parse_args()
    stego = ImageSteganography()

    if args.mode == 'hide':
        if not args.message or not args.output:
            print("Error: Message and output path are required for hide mode")
            return
        success = stego.hide_message(args.image,args.message,args.output)
        if success:
            print(f"Message hidden successfully in {args.output}")
    else:
        message = stego.reveal_message(args.image)
        print("\nRevealed message: ")
        print(message)

if __name__ == "__main__":
    main()