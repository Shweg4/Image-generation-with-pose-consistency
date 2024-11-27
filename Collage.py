import os
import cv2
import matplotlib.pyplot as plt

def create_collage(ground_truth_path, generated_folder, output_path="collage.png", max_images=12):
    """
    Create a collage of a ground truth image and generated images.

    Parameters:
        ground_truth_path: Path to the ground truth image.
        generated_folder: Path to the folder containing generated images.
        output_path: Path to save the collage image.
        max_images: Maximum number of generated images to include in the collage.
    """
    # Load ground truth image
    gt_image = cv2.imread(ground_truth_path)
    gt_image = cv2.cvtColor(gt_image, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Extract the ground truth file name (for the heading)
    gt_file_name = os.path.basename(ground_truth_path)

    # Load generated images
    generated_images = [img for img in os.listdir(generated_folder) if img.endswith((".jpg", ".png", ".jpeg"))]
    generated_images = generated_images[:max_images]  # Limit to max_images

    # Prepare a grid for the collage (3x4 for 12 images)
    cols = 4
    rows = 4 if len(generated_images) > 3 else 2  # Dynamically set rows
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    axes = axes.flatten()

    # Add title to the collage
    fig.suptitle(f"Ground Truth: {gt_file_name}", fontsize=16, fontweight="bold")

    # Add ground truth image to the first position
    axes[0].imshow(gt_image)
    axes[0].set_title("Ground Truth", fontsize=12)
    axes[0].axis("off")

    # Add generated images
    for idx, gen_image_name in enumerate(generated_images, start=1):
        gen_image_path = os.path.join(generated_folder, gen_image_name)
        gen_image = cv2.imread(gen_image_path)
        gen_image = cv2.cvtColor(gen_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        axes[idx].imshow(gen_image)
        axes[idx].set_title(gen_image_name, fontsize=10)
        axes[idx].axis("off")

    # Hide remaining axes
    for i in range(len(generated_images) + 1, len(axes)):
        axes[i].axis("off")

    # Save the collage
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to accommodate the title
    plt.savefig(output_path, dpi=300)
    print(f"Collage saved to {output_path}")
    plt.show()

# Example Usage
ground_truth_path = "./basketball_player_collage/ground_truth/basketball_player.jpg"  # Path to ground truth image
generated_folder = "./basketball_player_collage/generated/basketball_player"         # Path to folder with generated images
output_path = "collage_example.png"                   # Output path for collage

create_collage(ground_truth_path, generated_folder, output_path)
