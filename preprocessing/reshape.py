import os
from PIL import Image

# Path to the folder containing images
input_folder = './fill50k/target_raw'  # Replace with the path to your folder
output_folder = './fill50k/target'  # Replace with the desired output folder path

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Resize dimensions
target_size = (512, 512)

# Process each image in the folder
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
        try:
            # Open the image
            with Image.open(input_path) as img:
                # Resize the image
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Save the resized image to the output folder
                output_path = os.path.join(output_folder, filename)
                img_resized.save(output_path)
                print(f"Resized and saved: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("All images resized and saved to the output folder.")