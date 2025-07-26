
import cv2
import mediapipe as mp
import numpy as np
import math
from scipy.stats import pearsonr
# My Class
from peakfinder import PeakFinder

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Example: video_path = 'path/to/your/swing_video.mov'

def angle_between_points(A, B, C):
  AB = (B[0] - A[0], B[1] - A[1])
  BC = (C[0] - B[0], C[1] - B[1])

  dot_product = AB[0] * BC[0] + AB[1] * BC[1]
  magnitude_AB = math.sqrt(AB[0]**2 + AB[1]**2)
  magnitude_BC = math.sqrt(BC[0]**2 + BC[1]**2)

  cos_theta = dot_product / (magnitude_AB * magnitude_BC)

  # Ensure the value is within the valid range for arccosine
  cos_theta = max(-1, min(1, cos_theta))

  theta = math.acos(cos_theta)
  return 180 - math.degrees(theta)

def swing_analysis(video_path, right_handed):
    user_video = cv2.VideoCapture(video_path)

    width = int(user_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(user_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(width, height)



    frame_count = 0
    # sum and angle variables for initial/final stance angles
    sum_kneebend_angle = 0
    angle_kneebend_initial = 0

    sum_back_angle = 0
    angle_back_initial = 0

    sum_ballPosition_angle = 0
    angle_ballPosition_initial = 0

    sum_backArm_angle = 0
    angle_backArm_initial = 0

    angle_backLeg_final = 0

    # Previous Point for Total Head Traveled Distance
    previous_head_point = None
    total_head_traveled = 0

    # counter for finding arm difference once
    arms_rotation_first_time = True
    peak = PeakFinder(30)

    final_stance_values = []

    total_frames = int(user_video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)

    with (mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose):
        paused = False
        while user_video.isOpened():
            if not paused:
                ret, frame = user_video.read()

                if frame is None:
                    print("No frame detected")
                    break
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    # Get coordinates for Body Key Points and set them as tuples in variables (x, y)
                    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x * width,
                            landmarks[mp_pose.PoseLandmark.NOSE.value].y * height]
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * height]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]
                    left_elbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * height)
                    right_elbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height)
                    right_ankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * width,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * height)
                    left_ankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * height)
                    right_hip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * height)
                    left_hip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * width,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * height)
                    right_knee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * width,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * height)
                    left_knee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * width,
                                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * height)
                    abdominal_center = ((right_hip[0] + left_hip[0]) // 2, (right_hip[1] + left_hip[1]) // 2)

                    # Calculate Live Setup Angles Every Frame
                    if right_handed:
                        angle_kneebend = angle_between_points(right_ankle, right_knee, right_hip)
                        angle_back = angle_between_points(right_knee, right_hip, right_shoulder)
                        angle_ballPosition = angle_between_points(right_hip, right_shoulder, right_wrist)
                        angle_backArm = angle_between_points(right_shoulder, right_elbow, right_wrist)

                    else:
                        angle_kneebend = angle_between_points(left_ankle, left_knee, left_hip)
                        angle_back = angle_between_points(left_knee, left_hip, left_shoulder)
                        angle_ballPosition = angle_between_points(left_hip, left_shoulder, left_wrist)
                        angle_backArm = angle_between_points(left_shoulder, left_elbow, left_wrist)

                    # Calculate Average Setup Stance Angles
                    if frame_count < 20:
                        sum_kneebend_angle += angle_kneebend
                        sum_back_angle += angle_back
                        sum_ballPosition_angle += angle_ballPosition
                        sum_backArm_angle += angle_backArm

                    elif frame_count == 20:
                        angle_kneebend_initial = round(sum_kneebend_angle / 20, 2)
                        angle_back_initial = round(sum_back_angle / 20, 2)
                        angle_ballPosition_initial = round(sum_ballPosition_angle // 20, 2)
                        angle_backArm_initial = round(sum_backArm_angle / 20, 2)
                        print(angle_backArm_initial)


                    # Send values to PeakFinder to find Top Arm Angle
                    if frame_count < 1 and right_handed:
                        init_y = left_wrist[1]
                        init_x = left_wrist[0]

                    elif frame_count < 1 and not right_handed:
                        init_y = right_wrist[1]
                        init_x = right_wrist[0]

                    if frame_count >= 1 and not right_handed:
                        peak.find_peak(right_wrist[0], right_wrist[1], right_shoulder[0],
                           right_shoulder[1], right_hip[0], right_hip[1], init_x, init_y)
                    elif frame_count >= 1 and right_handed:
                        peak.find_peak(left_wrist[0], left_wrist[1], left_shoulder[0],
                           left_shoulder[1], left_hip[0], left_hip[1], init_x, init_y)


                    # Send values to peakFinder find_range so head movement until contact is made can be found
                    if right_handed:
                        peak.find_range(nose[1], right_wrist[1], right_hip[1])
                    if not right_handed:
                        peak.find_range(nose[1], left_wrist[1], left_hip[1])



                    #This is finding how far the arms are back when they reach the hip from their starting point
                    if right_handed:
                        if right_hip[1] - 5 < right_wrist[1] < right_hip[1] + 5 and arms_rotation_first_time == True:
                            arm_rotation_hands = round(right_wrist[0] - init_x, 1)
                            arms_rotation_first_time = False
                    else:
                        if left_hip[1] - 5 < left_wrist[1] < left_hip[1] + 5 and arms_rotation_first_time == True:
                            arm_rotation_hands = round(left_wrist[0] - init_x, 1)
                            arms_rotation_first_time = False

                    # QUEUE for Final Stance
                    current = angle_between_points(left_ankle, left_knee, left_hip)

                    if right_handed:
                        if frame_count < 20:
                            final_stance_values.append(current)
                        final_stance_values = final_stance_values[1:]
                        final_stance_values.append(current)
                        sum_finalBackLeg_angle = 0
                        for i in final_stance_values:
                            sum_finalBackLeg_angle += i
                        angle_backLeg_final = round(sum_finalBackLeg_angle / 20, 1)
                    else:
                        if frame_count < 20:
                            final_stance_values.append(current)
                        final_stance_values = final_stance_values[1:]
                        final_stance_values.append(current)
                        sum_finalBackLeg_angle = 0
                        for i in final_stance_values:
                            sum_finalBackLeg_angle += i
                        angle_backLeg_final = round(sum_finalBackLeg_angle / 20, 1)

                    #Narrow the giant list of landmarks to a better list for golf
                    golf_landmarks = [
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value]]

                    # Draw landmarks
                    for lm in golf_landmarks:
                        cx, cy = int(lm.x * width), int(lm.y * height)
                        # Draw a circle at the landmark position
                        cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

                    frame_count += 1


                except Exception as e:
                    traceback.print_exc()
                    print(f"Error: {e}")

                cv2.imshow('Mediapipe Feed', image)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == ord('p'):  # Press 'p' to toggle pause/resume
                paused = not paused

        #CalculateT Top Arm Angle
        top_arm_angle = round(angle_between_points
                              ((peak.first_point_x, peak.first_point_y),
                               (peak.second_point_x, peak.second_point_y),
                               (peak.third_point_x, peak.third_point_y)), 1)
        #Calculate Head Y Range
        head_y_range = round(peak.max_head_y - peak.min_head_y, 1)

        final_user_data = [angle_kneebend_initial, angle_back_initial, angle_ballPosition_initial,
                           angle_backArm_initial, arm_rotation_hands, top_arm_angle, angle_backLeg_final,
                           head_y_range]
        rory_data = [156.8, 129.75, 47, 170.67, 9.9, 93.8, 157.4, 26.1]
        similarity_score = round((np.square(pearsonr(rory_data, final_user_data)[0])) * 100, 0)




        print("R-squared: ", similarity_score)
        print("Kneebend Initial Angle: ", angle_kneebend_initial)
        print("Initial Back Posture Angle: ", angle_back_initial)
        print("Initial Ball Position Angle: ", angle_ballPosition_initial)
        print("Initial Back Arm Angle: ", angle_backArm_initial + 180)
        print("Arm Takeback Distance from Initial X-Value: ", arm_rotation_hands)
        print("Top Arm Angle: ", top_arm_angle)
        print("Final Back Leg Angle: ", angle_backLeg_final)
        print("Head Vertical Change", head_y_range)
        user_video.release()
        cv2.destroyAllWindows()
        return angle_kneebend_initial, angle_back_initial, angle_ballPosition_initial, angle_backArm_initial, arm_rotation_hands, top_arm_angle, angle_backLeg_final, head_y_range, similarity_score



