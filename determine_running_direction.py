import math


# Notes:
# This function can be streamlined.

# 1. Consider using determine_knee_angles.py to get the knee angle instead of calculating it here separately.
# This would prevent code duplication but adds convolution.


def determine_running_direction(keypoints_with_scores, KEYPOINT_DICT):

    # The angle in the left knee is used to determine running direction.
    # Better would be to use both knees. For now we use only one leg.

    left_hip = KEYPOINT_DICT['left_hip']
    left_knee = KEYPOINT_DICT['left_knee']
    left_ankle = KEYPOINT_DICT['left_ankle']

    left_hip_x = keypoints_with_scores[0][0][left_hip][1]
    left_hip_y = keypoints_with_scores[0][0][left_hip][0]

    left_knee_x = keypoints_with_scores[0][0][left_knee][1]
    left_knee_y = keypoints_with_scores[0][0][left_knee][0]

    left_ankle_x = keypoints_with_scores[0][0][left_ankle][1]
    left_ankle_y = keypoints_with_scores[0][0][left_ankle][0]

    #print("left hip x: ", left_hip_x, ", left hip y: ", left_hip_y)
    #print("left knee x: ", left_knee_x, ", left knee y: ", left_knee_y)
    #print("left ankle x: ", left_ankle_x, ", left ankle y: ", left_ankle_y)


    # The following calculations determine the angle between two vectors in clockwise directions.
    # Vector 1: From left knee to left hip.
    # Vector 2: From left knee to left ankle.
    # Whenever the angle between those vectors is larger than 180 degrees, we know that the runner in the image
    # runs towards the right side of the image. Otherwise, the knee joint would bend agains the joint =(
    # Calculate vectors between points.
    vec1_x = left_hip_x - left_knee_x
    vec1_y = left_hip_y - left_knee_y
    vec2_x = left_ankle_x - left_knee_x
    vec2_y = left_ankle_y - left_knee_y
    # Calculate dot product and determinant.
    dot_product = vec1_x * vec2_x + vec1_y * vec2_y
    determinant = vec1_x * vec2_y - vec1_y * vec2_x
    # Calculate angle in radians using atan2.
    angle_radians = math.atan2(determinant, dot_product)
    # Convert radians to degrees.
    angle_degrees = math.degrees(angle_radians)
    # Ensure positive angle. Results are [-180, 180], negative ones are shifted by 360.
    if angle_degrees < 0:
        angle_degrees += 360
    
    if angle_degrees >= 180:
        running_direction = "right"
    else:
        running_direction = "left"

    #print("Angle between the two vectors in clockwise direction:", angle_degrees)
    #print("Running direction: ", running_direction)
    

    return running_direction, angle_degrees