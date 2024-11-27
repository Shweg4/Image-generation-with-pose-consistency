import os
import cv2
import mediapipe as mp
import numpy as np

# Paths to input and output folders
input_folder = '/Users/sameerbharadwaj/Downloads/TakeHome_GenSim'  # Replace with your input folder path
output_folder = "./fill50k/pose_report"  # Replace with your output folder path

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Mediapipe Pose Detection setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize Mediapipe pose detector
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# OpenPose color scheme for body parts
colors = {
    "HEAD": (255, 20, 147),  # Pink
    "LEFT_ARM": (255, 0, 0),  # Red
    "RIGHT_ARM": (255, 165, 0),  # Orange
    "TORSO": (0, 255, 0),  # Green
    "LEFT_LEG": (0, 255, 255),  # Cyan
    "RIGHT_LEG": (0, 0, 255),  # Blue
}

# Pose landmark connections with color-matched circles
connections = [
    # Head
    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.LEFT_EYE_INNER, colors["HEAD"]),
    (mp_pose.PoseLandmark.LEFT_EYE_INNER, mp_pose.PoseLandmark.LEFT_EYE, colors["HEAD"]),
    (mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.LEFT_EYE_OUTER, colors["HEAD"]),
    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.RIGHT_EYE_INNER, colors["HEAD"]),
    (mp_pose.PoseLandmark.RIGHT_EYE_INNER, mp_pose.PoseLandmark.RIGHT_EYE, colors["HEAD"]),
    (mp_pose.PoseLandmark.RIGHT_EYE, mp_pose.PoseLandmark.RIGHT_EYE_OUTER, colors["HEAD"]),
    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.MOUTH_LEFT, colors["HEAD"]),
    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.MOUTH_RIGHT, colors["HEAD"]),

    # Torso
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER, colors["TORSO"]),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP, colors["TORSO"]),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP, colors["TORSO"]),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP, colors["TORSO"]),

    # Arms
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, colors["LEFT_ARM"]),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST, colors["LEFT_ARM"]),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, colors["RIGHT_ARM"]),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST, colors["RIGHT_ARM"]),

    # Legs
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, colors["LEFT_LEG"]),
    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE, colors["LEFT_LEG"]),
    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, colors["RIGHT_LEG"]),
    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE, colors["RIGHT_LEG"]),
]

# Process images
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            # Read the image
            image = cv2.imread(input_path)
            if image is None:
                print(f"Unable to read {filename}, skipping...")
                continue

            # Convert to RGB for Mediapipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Perform pose detection
            results = pose.process(image_rgb)

            # Create a blank image for the stick figure
            height, width, _ = image.shape
            blank_image = np.zeros((height, width, 3), dtype=np.uint8)

            # Draw pose landmarks as a stick figure
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Draw connections and joints
                for start, end, color in connections:
                    start_landmark = landmarks[start.value]
                    end_landmark = landmarks[end.value]

                    # Convert normalized coordinates to pixel values
                    start_x, start_y = int(start_landmark.x * width), int(start_landmark.y * height)
                    end_x, end_y = int(end_landmark.x * width), int(end_landmark.y * height)

                    # Draw line between the landmarks
                    cv2.line(blank_image, (start_x, start_y), (end_x, end_y), color, 2)

                    # Draw circles at joints
                    cv2.circle(blank_image, (start_x, start_y), 8, color, -1)  # Circle for the starting joint
                    cv2.circle(blank_image, (end_x, end_y), 8, color, -1)  # Circle for the ending joint

            # Resize the blank image to 512x512
            resized_image = cv2.resize(blank_image, (512, 512), interpolation=cv2.INTER_AREA)

            # Save the resized stick figure image to the output folder
            cv2.imwrite(output_path, resized_image)
            print(f"Processed and saved: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Release resources
pose.close()

print("Pose stick figures resized to 512x512 and saved in the output folder.")