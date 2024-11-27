import os
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# MediaPipe Pose Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5)

def preprocess_image(image_path, target_size=(256, 256)):
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Failed to load image - {image_path}")
        return None
    return cv2.resize(image, target_size)

def extract_keypoints(image_path):
    image = preprocess_image(image_path)
    if image is None:
        return np.array([])
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_image)
    keypoints = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            keypoints.append((landmark.x * image.shape[1], landmark.y * image.shape[0]))
    return np.array(keypoints)

def calculate_pck(gt_keypoints, pred_keypoints, threshold=0.1, image_size=256):
    if gt_keypoints.shape != pred_keypoints.shape:
        print("Warning: Keypoints shapes do not match.")
        return 0.0
    distances = np.linalg.norm(gt_keypoints - pred_keypoints, axis=1)
    normalized_distances = distances / image_size
    correct_keypoints = np.sum(normalized_distances < threshold)
    return correct_keypoints / len(gt_keypoints)

def evaluate_multiple_ground_truths(ground_truth_dir, generated_dir, threshold=0.1, image_size=256):
    # Allow multiple formats for ground truth images
    ground_truth_images = sorted([img for img in os.listdir(ground_truth_dir) if img.endswith((".jpg", ".png", ".jpeg"))])
    print("Ground Truth Images Found:", ground_truth_images)

    overall_results = []

    for gt_image in ground_truth_images:
        gt_path = os.path.join(ground_truth_dir, gt_image)
        gt_name = os.path.splitext(gt_image)[0]  # Extract base name without extension
        gen_image_dir = os.path.join(generated_dir, gt_name)
        
        print(f"Looking for folder: {gen_image_dir}")

        if not os.path.exists(gen_image_dir):
            print(f"Warning: Folder '{gen_image_dir}' for ground truth '{gt_name}' does not exist. Skipping.")
            continue

        gen_image_paths = [os.path.join(gen_image_dir, img) for img in os.listdir(gen_image_dir) if img.endswith((".jpg", ".png", ".jpeg"))]
        gt_keypoints = extract_keypoints(gt_path)

        if len(gt_keypoints) == 0:
            print(f"Warning: No keypoints detected in ground truth image {gt_image}. Skipping.")
            continue

        gt_pck_scores = []
        for gen_image_path in gen_image_paths:
            gen_keypoints = extract_keypoints(gen_image_path)
            if len(gen_keypoints) == 0:
                print(f"Warning: No keypoints detected in generated image {gen_image_path}. Skipping.")
                continue

            pck = calculate_pck(gt_keypoints, gen_keypoints, threshold, image_size)
            gt_pck_scores.append(pck * 100)

        if gt_pck_scores:
            avg_pck = np.mean(gt_pck_scores)
            overall_results.append({"Ground Truth Image": gt_image, "Average PCK (%)": round(avg_pck, 2)})
            print(f"Processed {len(gt_pck_scores)} images for ground truth {gt_name}. Average PCK: {avg_pck:.2f}%")

    # Calculate the overall average PCK
    if overall_results:
        total_avg_pck = np.mean([result["Average PCK (%)"] for result in overall_results])
        overall_results.append({"Ground Truth Image": "Overall Average", "Average PCK (%)": round(total_avg_pck, 2)})
        save_summary_table(overall_results, "pck_summary_table.png")
        plot_average_pck(overall_results)
        print(f"Total Average PCK: {total_avg_pck:.2f}%")

    return overall_results

def save_summary_table(results, filename):
    df = pd.DataFrame(results)
    
    # Save as styled HTML table
    styled_table = df.style.set_table_styles(
        [{'selector': 'thead th',
          'props': [('background-color', '#3498db'), ('color', 'white'), ('font-weight', 'bold')]},
         {'selector': 'tbody td',
          'props': [('border', '1px solid #dddddd'), ('text-align', 'center')]}]
    ).set_properties(**{'text-align': 'center', 'font-size': '12px'})
    styled_table.to_html("styled_table.html")
    print("Saved styled table as styled_table.html")

    # Save as PNG table using matplotlib
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.5))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(filename, dpi=300)
    print(f"Saved PCK summary table as {filename}")

def plot_average_pck(results):
    df = pd.DataFrame(results)
    df = df[df["Ground Truth Image"] != "Overall Average"]  # Exclude overall average for the bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Ground Truth Image", y="Average PCK (%)", palette="Blues_d", edgecolor="black")
    plt.axhline(y=df["Average PCK (%)"].mean(), color='red', linestyle='--', label='Overall Average')
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel("Average PCK (%)", fontsize=14)
    plt.xlabel("Ground Truth Image", fontsize=14)
    plt.title("Average PCK for Each Ground Truth", fontsize=16, fontweight="bold")
    plt.legend(fontsize=12, loc="upper right")
    plt.tight_layout()
    plt.savefig("pck_summary_chart.png", dpi=300)
    print("Saved PCK summary chart as pck_summary_chart.png")
    plt.show()

# Example Usage
ground_truth_dir = "./data/ground_truth"  # Path to ground truth directory
generated_dir = "./data/generated"       # Path to generated images directory

# Evaluate PCK for all ground truths and save a summary table and chart
results = evaluate_multiple_ground_truths(ground_truth_dir, generated_dir, threshold=0.05, image_size=256)
