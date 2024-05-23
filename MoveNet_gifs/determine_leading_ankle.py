
def determine_leading_ankle(keypoints_with_scores, KEYPOINT_DICT, running_direction):

    left_ankle = KEYPOINT_DICT['left_ankle']
    right_ankle = KEYPOINT_DICT['right_ankle']

    left_ankle_x_value = keypoints_with_scores[0][0][left_ankle][1] # X-axis value of left knee. (Origin: Top left)
    right_ankle_x_value = keypoints_with_scores[0][0][right_ankle][1] # X-axis value of right knee. (Origin: Top left)


    # If runner runs towards the right side of the image, max(), otherwise min().
    if running_direction == "right":
        leading_ankle_x_value = max(left_ankle_x_value, right_ankle_x_value)
    elif running_direction == "left":
        leading_ankle_x_value = min(left_ankle_x_value, right_ankle_x_value)
    else:
        leading_ankle_x_value = 0

    
    return leading_ankle_x_value
    