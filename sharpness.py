import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_sharpness(image_path):
    """
    Calculate the sharpness of an image using the Laplacian variance.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return None
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpness_score = laplacian.var()
    return sharpness_score

def evaluate_sharpness_with_comparison(ground_truth_dir, generated_dir):
    """
    Evaluate sharpness for ground truth images and compare with their generated counterparts.
    """
    ground_truth_images = sorted([img for img in os.listdir(ground_truth_dir) if img.endswith((".jpg", ".png", ".jpeg"))])
    print("Ground Truth Images Found:", ground_truth_images)

    comparison_results = []
    overall_generated_sharpness = []

    for gt_image in ground_truth_images:
        gt_path = os.path.join(ground_truth_dir, gt_image)
        gt_name = os.path.splitext(gt_image)[0]
        gen_image_dir = os.path.join(generated_dir, gt_name)

        print(f"\nProcessing Ground Truth: {gt_image}")
        if not os.path.exists(gen_image_dir):
            print(f"Warning: Folder '{gen_image_dir}' for ground truth '{gt_name}' does not exist. Skipping.")
            continue

        # Calculate sharpness for the ground truth image
        gt_sharpness = calculate_sharpness(gt_path)
        if gt_sharpness is None:
            print(f"Error: Unable to calculate sharpness for ground truth image {gt_image}. Skipping.")
            continue

        # Calculate sharpness for generated images
        gen_image_paths = [os.path.join(gen_image_dir, img) for img in os.listdir(gen_image_dir) if img.endswith((".jpg", ".png", ".jpeg"))]
        gen_sharpness_scores = []
        for gen_image_path in gen_image_paths:
            gen_sharpness = calculate_sharpness(gen_image_path)
            if gen_sharpness is not None:
                gen_sharpness_scores.append(gen_sharpness)

        if gen_sharpness_scores:
            avg_gen_sharpness = np.mean(gen_sharpness_scores)
            overall_generated_sharpness.extend(gen_sharpness_scores)

            # Add results to the comparison table
            comparison_results.append({
                "Ground Truth Image": gt_image,
                "Ground Truth Sharpness": round(gt_sharpness, 2),
                "Average Generated Sharpness": round(avg_gen_sharpness, 2),
                "Difference": round(avg_gen_sharpness - gt_sharpness, 2)
            })
            print(f"Processed {len(gen_sharpness_scores)} images for ground truth {gt_image}.")
            print(f"Ground Truth Sharpness: {gt_sharpness:.2f}, Average Generated Sharpness: {avg_gen_sharpness:.2f}")

    # Calculate the overall average sharpness
    if comparison_results:
        overall_avg_sharpness = np.mean(overall_generated_sharpness)
        comparison_results.append({
            "Ground Truth Image": "Overall Average",
            "Ground Truth Sharpness": "",
            "Average Generated Sharpness": round(overall_avg_sharpness, 2),
            "Difference": ""
        })

        save_summary_table(comparison_results, "sharpness_comparison_table.png")
        plot_comparison_graph(comparison_results)
    else:
        print("No valid sharpness data available.")

    return comparison_results

def save_summary_table(results, filename):
    df = pd.DataFrame(results)
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(filename, dpi=300)
    print(f"Saved sharpness comparison table as {filename}")

def plot_comparison_graph(results):
    df = pd.DataFrame(results)
    df = df[df["Ground Truth Image"] != "Overall Average"]  # Exclude the "Overall Average" row

    # Plotting comparison graph
    plt.figure(figsize=(12, 6))
    x = np.arange(len(df))  # X positions for the bars
    width = 0.35  # Width of the bars

    plt.bar(x - width/2, df["Ground Truth Sharpness"], width, label="Ground Truth Sharpness", color="skyblue", edgecolor="black")
    plt.bar(x + width/2, df["Average Generated Sharpness"], width, label="Generated Average Sharpness", color="steelblue", edgecolor="black")

    plt.axhline(y=df["Average Generated Sharpness"].mean(), color='red', linestyle='--', label='Overall Average Generated Sharpness')

    plt.xticks(x, df["Ground Truth Image"], rotation=45, ha="right", fontsize=12)
    plt.ylabel("Sharpness Score", fontsize=14)
    plt.xlabel("Ground Truth Image", fontsize=14)
    plt.title("Comparison of Ground Truth and Generated Image Sharpness", fontsize=16, fontweight="bold")
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig("sharpness_comparison_chart.png", dpi=300)
    print("Saved sharpness comparison chart as sharpness_comparison_chart.png")
    plt.show()

# Example Usage
ground_truth_dir = "./data/ground_truth"  # Path to ground truth directory
generated_dir = "./data/generated"       # Path to generated images directory

# Evaluate sharpness across ground truths and their generated images
comparison_results = evaluate_sharpness_with_comparison(ground_truth_dir, generated_dir)
