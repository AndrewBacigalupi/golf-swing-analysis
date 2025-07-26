import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
image_path = '/Users/andrew/WideStance.jpg'  # Replace with the path to your image file

# Load the image
image = cv2.imread(image_path)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:  # Infinite loop for displaying the image
        # Process the image
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            # Calculate angles
            angle_elbow = np.abs(np.degrees(np.arctan2(wrist[1] - elbow[1], wrist[0] - elbow[0]) -
                                            np.arctan2(shoulder[1] - elbow[1], shoulder[0] - elbow[0])))
            angle_elbow = angle_elbow if angle_elbow <= 180.0 else 360 - angle_elbow

            # Display angle measurements
            cv2.putText(image, f"Left Elbow Angle: {angle_elbow:.2f} degrees", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

            # Draw landmarks
            for lm in landmarks:
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Draw a circle at the landmark position
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

        except Exception as e:
            print(f"Error: {e}")

        cv2.imshow('Mediapipe Feed', image)

        key = cv2.waitKey(10)
        if key == ord('q'):
            break  # Break the loop when 'q' is pressed

cv2.destroyAllWindows()