import os
from PIL import Image

def rename_images(input_folder, output_folder, start_number, limit=None):
    """
    Renames and converts images in the input folder to PNG format, 
    storing them in the output folder with ascending order.

    Args:
        input_folder (str): Path to the folder containing original images.
        output_folder (str): Path to the folder where renamed images will be stored.
        start_number (int): Starting number for renaming.
        limit (int, optional): Maximum number of images to process. 
                               If None, all images in the folder are processed.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of image files in the input folder
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])

    # Apply limit if specified
    if limit is not None:
        image_files = image_files[:limit]

    for i, file in enumerate(image_files, start=start_number):
        img_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"{i}.png")
        
        # Open image and save in PNG format with new name
        with Image.open(img_path) as img:
            img.save(output_path, format='PNG')
    
    print(f"Renamed and converted {len(image_files)} images. Output stored in '{output_folder}'.")

# Example usage:
input_folder = "/Users/sameerbharadwaj/Downloads/work/images/casual"
output_folder = "/Users/sameerbharadwaj/Downloads/work/fill50k/source"
start_number = 28  # You can start at 0
limit = None      # Number of images to process, if None, process all

rename_images(input_folder, output_folder, start_number, limit)