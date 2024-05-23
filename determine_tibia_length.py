

def determine_tibia_length(keypoints_with_scores, KEYPOINT_DICT):


    # Determine Y position of knees.
    right_knee = KEYPOINT_DICT['right_knee']
    left_knee = KEYPOINT_DICT['left_knee']
    right_knee_y = keypoints_with_scores[0][0][right_knee][0]
    left_knee_y = keypoints_with_scores[0][0][left_knee][0]


    # Determine Y position of ankles.
    right_ankle = KEYPOINT_DICT['right_ankle']
    left_ankle = KEYPOINT_DICT['left_ankle']
    right_ankle_y = keypoints_with_scores[0][0][right_ankle][0]
    left_ankle_y = keypoints_with_scores[0][0][left_ankle][0]


    # Determine distance between knee and ankle.
    # This yields the tibia length. Careful: The actual length of the tibia
    # can only be found when the gif contains at least an entire stride.
    # The actual tibia length is apparent on the image where the tibia is precisely in vertical position.
    # If we measure the distance between knee and ankle in every image,
    # we get the tibia length by finding the max. distance between knee and ankle.
    distance_right_knee_to_ankle = abs(right_knee_y - right_ankle_y)
    distance_left_knee_to_ankle = abs(left_knee_y - left_ankle_y)


    return distance_left_knee_to_ankle, distance_right_knee_to_ankle