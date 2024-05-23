
def determine_center_of_mass(keypoints_with_scores, KEYPOINT_DICT):

    # Determine midpoint between shoulders.
    right_shoulder = KEYPOINT_DICT['right_shoulder']
    left_shoulder = KEYPOINT_DICT['left_shoulder']
    right_shoulder_x = keypoints_with_scores[0][0][right_shoulder][1]
    right_shoulder_y = keypoints_with_scores[0][0][right_shoulder][0]
    left_shoulder_x = keypoints_with_scores[0][0][left_shoulder][1]
    left_shoulder_y = keypoints_with_scores[0][0][left_shoulder][0]
    shoulders_x = (right_shoulder_x + left_shoulder_x) / 2
    shoulders_y = (right_shoulder_y + left_shoulder_y) / 2


    # Determine midpoint between hips.
    right_hip = KEYPOINT_DICT['right_hip']
    left_hip = KEYPOINT_DICT['left_hip']
    right_hip_x = keypoints_with_scores[0][0][right_hip][1]
    right_hip_y = keypoints_with_scores[0][0][right_hip][0]
    left_hip_x = keypoints_with_scores[0][0][left_hip][1]
    left_hip_y = keypoints_with_scores[0][0][left_hip][0]
    hips_x = (right_hip_x + left_hip_x) / 2
    hips_y = (right_hip_y + left_hip_y) / 2


    # Determine midpoint between shoulders and hips.
    center_of_mass_x = (shoulders_x + hips_x) / 2
    center_of_mass_y = (shoulders_y + hips_y) / 2


    return center_of_mass_x, center_of_mass_y

