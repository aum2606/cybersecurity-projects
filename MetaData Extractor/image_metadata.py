from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import argparse

class ImageMetadataExtractor:
    """A class to extract and analyze image metadata"""

    def __init__(self):
        self.supported_formats = [".jpg",".jpeg", ".png", ".tiff", ".bmp"]

    def get_exif_data(self, image_path):
        """Extract EXIF data from an image file"""
        try:
            image = Image.open(image_path)
            exif_data = {}

            #get basic image info
            exif_data["filename"] = os.path.basename(image_path)
            exif_data["format"] = image.format
            exif_data["mode"] = image.mode 
            exif_data["size"] = image.size

            #extract EXIF metadata if available
            if hasattr(image,"_getexif") and image._getexif():
                exif = image.getexif()
                for tag_id in exif():
                    tag = TAGS.get(tag_id,tag_id)
                    data = exif.get(tag_id)

                    # Convert bytes to string if necessary
                    if isinstance(data, bytes):
                        try:
                            data = data.decode()
                        except UnicodeDecodeError:
                            data = str(data)
                            
                    exif_data[tag] = data
            
            return exif_data
        except Exception as e:
            print(f"Error extracting EXIF data from {image_path}: {str(e)}")
            return None

    def process_directory(self,directory_path):
        """Process all images in a directory
            Args: directory_path (str) : Path to directory containing images
            Returns:
                list : List of dictionaries, one per image, with EXIF data
        """

        metadata_collection = []

        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if os.path.splitext(filename)[1].lower() in self.supported_formats:
                    image_path = os.path.join(root, filename)
                    exif_data = self.get_exif_data(image_path)
                    if exif_data:
                        metadata_collection.append(exif_data)
        return metadata_collection

    def generate_report(self,metadata_collection,output_file=None):
        """Generate a report from the metadata collection
            Args:
                metadata_collection (list) : Collection of metadata dictionaries
                output_file (str, optional) : File to save report to
            Returns:
                str : Report text
        """
        report = "Image Metadata Analysis Report\n"
        report += "=" * 30 + "\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total images processed: {len(metadata_collection)}\n"
        report += "\n"

        for idx,metadata in enumerate(metadata_collection,1):
            report += f"Image {idx} : {metadata.get('filename','Unknown')}\n"
            report += f"-" * 20 + "\n"
            for key, value in metadata.items():
                report += f"{key}: {value}\n"
            report += "\n"

        if output_file:
            with open(output_file,"w") as f:
                f.write(report)

        return report


def main():
    parser = argparse.ArgumentParser(description="Image Metadata Extractor")
    parser.add_argument('path',help='Path to image file or directory')
    parser.add_argument('--output',help='Output file',default=None)
    
    args = parser.parse_args()
    if os.path.isfile(args.path):
        metadata = extractor.get_exif_data(args.path)
        if metadata:
            metadata_collection = [metadata]
        else:
            print("No metadata could be extracted from the image")
            return 
    else:
        metadata_collection = extractor.process_directory(args.path)
        
    report = extractor.generate_report(metadata_collection,args.output)
    if not args.output:
        print(report)

if __name__ == "__main__":
    main()