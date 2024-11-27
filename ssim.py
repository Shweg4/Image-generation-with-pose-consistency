from skimage.metrics import structural_similarity as compare_ssim
import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_ssim(gt_image_path, gen_image_path):
    """
    Calculate SSIM (Structural Similarity Index) between a ground truth image and a generated image.
    """
    # Load images in grayscale
    gt_image = cv2.imread(gt_image_path, cv2.IMREAD_GRAYSCALE)
    gen_image = cv2.imread(gen_image_path, cv2.IMREAD_GRAYSCALE)

    # Ensure images have the same dimensions
    if gt_image.shape != gen_image.shape:
        gen_image = cv2.resize(gen_image, (gt_image.shape[1], gt_image.shape[0]))

    # Calculate SSIM
    ssim_score, _ = compare_ssim(gt_image, gen_image, full=True)
    return ssim_score

def evaluate_ssim_across_ground_truths(ground_truth_dir, generated_dir):
    """
    Evaluate SSIM for multiple ground truth images and their corresponding generated images.
    """
    ground_truth_images = sorted([img for img in os.listdir(ground_truth_dir) if img.endswith((".jpg", ".png", ".jpeg"))])
    print("Ground Truth Images Found:", ground_truth_images)

    overall_results = []
    all_ssim_scores = []

    for gt_image in ground_truth_images:
        gt_path = os.path.join(ground_truth_dir, gt_image)
        gt_name = os.path.splitext(gt_image)[0]
        gen_image_dir = os.path.join(generated_dir, gt_name)

        print(f"\nProcessing Ground Truth: {gt_image}")
        if not os.path.exists(gen_image_dir):
            print(f"Warning: Folder '{gen_image_dir}' for ground truth '{gt_name}' does not exist. Skipping.")
            continue

        gen_image_paths = [os.path.join(gen_image_dir, img) for img in os.listdir(gen_image_dir) if img.endswith((".jpg", ".png", ".jpeg"))]
        gt_ssim_scores = []
        for gen_image_path in gen_image_paths:
            ssim_score = calculate_ssim(gt_path, gen_image_path)
            gt_ssim_scores.append(ssim_score)

        if gt_ssim_scores:
            avg_ssim = np.mean(gt_ssim_scores)
            overall_results.append({
                "Ground Truth Image": gt_image,
                "Average SSIM": round(avg_ssim, 4)
            })
            all_ssim_scores.extend(gt_ssim_scores)

            print(f"Processed {len(gt_ssim_scores)} images for ground truth {gt_image}. Average SSIM: {avg_ssim:.4f}")

    # Calculate overall average SSIM
    if overall_results:
        overall_avg_ssim = np.mean(all_ssim_scores)
        overall_results.append({
            "Ground Truth Image": "Overall Average",
            "Average SSIM": round(overall_avg_ssim, 4)
        })
        save_summary_table(overall_results, "ssim_comparison_table.png")
        plot_average_ssim(overall_results)
        print(f"\nOverall Average SSIM: {overall_avg_ssim:.4f}")
    else:
        print("No valid SSIM data available.")

    return overall_results

def save_summary_table(results, filename):
    df = pd.DataFrame(results)
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.5))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(filename, dpi=300)
    print(f"Saved SSIM comparison table as {filename}")

def plot_average_ssim(results):
    df = pd.DataFrame(results)
    df = df[df["Ground Truth Image"] != "Overall Average"]  # Exclude the "Overall Average" row

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Ground Truth Image", y="Average SSIM", palette="Blues_d", edgecolor="black")
    plt.axhline(y=df["Average SSIM"].mean(), color='red', linestyle='--', label='Overall Average SSIM')
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel("Average SSIM", fontsize=14)
    plt.xlabel("Ground Truth Image", fontsize=14)
    plt.title("Average SSIM for Each Ground Truth", fontsize=16, fontweight="bold")
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig("ssim_comparison_chart.png", dpi=300)
    print("Saved SSIM comparison chart as ssim_comparison_chart.png")
    plt.show()

# Example Usage
ground_truth_dir = "./data/ground_truth"  # Path to ground truth directory
generated_dir = "./data/generated"       # Path to generated images directory

# Evaluate SSIM across ground truths and their generated images
results = evaluate_ssim_across_ground_truths(ground_truth_dir, generated_dir)
