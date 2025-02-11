from PIL import Image
import os

# first, let's create a test image
def create_test_image():
    img = Image.new('RGB',(100,100),color='red')
    if not os.path.exists('test_images'):
        os.mkdir('test_images')
    img.save('test_images/test_image.jpg')
    print("Created test image: test_images/test_image.jpg")

# Import our metadata extractor
from image_metadata import ImageMetadataExtractor

# run demonstrations
def run_demo():
    #create test image
    create_test_image()
    
    # initialize metadata extractor
    extractor = ImageMetadataExtractor()

    print("\n===single image demo===")
    #process single image
    metadata = extractor.get_exif_data('test_images/test_image.jpg')
    print("\n metadata for single image: ")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("\n ===directory demo===")
    metadata_collection = extractor.process_directory('test_images')

    # generate and display report
    print("\n ===report demo===")
    report = extractor.generate_report(metadata_collection)
    print(report)

    #save report to file
    output_file = 'metadata_report.txt'
    extractor.generate_report(metadata_collection,output_file)
    print(f"\nReport saved to {output_file}")


if __name__ == "__main__":
    run_demo()