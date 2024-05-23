def determine_femur_length(keypoints_with_scores, KEYPOINT_DICT):


    # Determine Y position of hips.
    right_hip = KEYPOINT_DICT['right_hip']
    left_hip = KEYPOINT_DICT['left_hip']
    right_hip_y = keypoints_with_scores[0][0][right_hip][0]
    left_hip_y = keypoints_with_scores[0][0][left_hip][0]


    # Determine Y position of knees.
    right_knee = KEYPOINT_DICT['right_knee']
    left_knee = KEYPOINT_DICT['left_knee']
    right_knee_y = keypoints_with_scores[0][0][right_knee][0]
    left_knee_y = keypoints_with_scores[0][0][left_knee][0]


    # Determine distance between hib and knee.
    # This yields the femur length. Careful: The actual length of the femur
    # can only be found when the gif contains at least an entire stride.
    # The actual femur length is apparent on the image where the femur is precisely in vertical position.
    # If we measure the distance between hip and knee in every image,
    # we get the femur length by finding the max. distance between hip and knee.
    distance_right_hip_to_knee = abs(right_hip_y - right_knee_y)
    distance_left_hip_to_knee = abs(left_hip_y - left_knee_y)


    return distance_left_hip_to_knee, distance_right_hip_to_knee