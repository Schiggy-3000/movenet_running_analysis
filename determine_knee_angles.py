import math



def determine_knee_angles(keypoints_with_scores, KEYPOINT_DICT):

    # Left knee angle.
    left_hip = KEYPOINT_DICT['left_hip']
    left_knee = KEYPOINT_DICT['left_knee']
    left_ankle = KEYPOINT_DICT['left_ankle']

    left_hip_x = keypoints_with_scores[0][0][left_hip][1]
    left_hip_y = keypoints_with_scores[0][0][left_hip][0]

    left_knee_x = keypoints_with_scores[0][0][left_knee][1]
    left_knee_y = keypoints_with_scores[0][0][left_knee][0]

    left_ankle_x = keypoints_with_scores[0][0][left_ankle][1]
    left_ankle_y = keypoints_with_scores[0][0][left_ankle][0]

    left_knee_angle = calculate_knee_angle(
        left_hip_x,
        left_hip_y,
        left_knee_x,
        left_knee_y,
        left_ankle_x,
        left_ankle_y)


    # Right knee angle.
    right_hip = KEYPOINT_DICT['right_hip']
    right_knee = KEYPOINT_DICT['right_knee']
    right_ankle = KEYPOINT_DICT['right_ankle']

    right_hip_x = keypoints_with_scores[0][0][right_hip][1]
    right_hip_y = keypoints_with_scores[0][0][right_hip][0]

    right_knee_x = keypoints_with_scores[0][0][right_knee][1]
    right_knee_y = keypoints_with_scores[0][0][right_knee][0]

    right_ankle_x = keypoints_with_scores[0][0][right_ankle][1]
    right_ankle_y = keypoints_with_scores[0][0][right_ankle][0]

    right_knee_angle = calculate_knee_angle(
        right_hip_x,
        right_hip_y,
        right_knee_x,
        right_knee_y,
        right_ankle_x,
        right_ankle_y)


    return left_knee_angle, right_knee_angle



def calculate_knee_angle(
        hip_x,
        hip_y,
        knee_x,
        knee_y,
        ankle_x,
        ankle_y):
    
    # The following calculations determine the angle between two vectors in clockwise directions.
    # Vector 1: From left knee to left hip.
    # Vector 2: From left knee to left ankle.
    # Note: The "Nullpunkt" of the coordinate system is in the top left.
    vec1_x = hip_x - knee_x
    vec1_y = hip_y - knee_y
    vec2_x = ankle_x - knee_x
    vec2_y = ankle_y - knee_y
    # Calculate dot product and determinant
    dot_product = vec1_x * vec2_x + vec1_y * vec2_y
    determinant = vec1_x * vec2_y - vec1_y * vec2_x
    # Calculate angle in radians using atan2
    angle_radians = math.atan2(determinant, dot_product)
    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)
    # Ensure positive angle. Results are [-180, 180], negative ones are shifted by 360.
    if angle_degrees < 0:
        angle_degrees += 360
    

    # Whenever the angle between vector 1 and vector 2 is larger than 180 degrees, we know that the runner in the image
    # runs towards the right side of the image. Otherwise, the knee joint would bend agains the joint =(
    if angle_degrees >= 180:
        running_direction = "right"
    else:
        running_direction = "left"


    # Since the angle is calculated in clockwise direction, knee angles from runners who face the right side of
    # the image must be inverted.
    if running_direction == "right":
        knee_angle = 360 - angle_degrees
    else:
        knee_angle = angle_degrees

    
    return knee_angle