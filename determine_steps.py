# This function NEEDS TO BE STREAMLINED.
# Somethimes movenet_thunder is not that accurate and
# the positions for joints wiggle around significantly from frame to frame.
# This messes up the step count.
# I reckon the solution is to only increase the step counter if two consecutive frames agree, that the leading ankle has changed.


def determine_steps(keypoints_with_scores, KEYPOINT_DICT, total_steps, running_direction, leading_ankle):

    steps = total_steps

    # Retrieve x-values for both ankles.
    left_ankle = KEYPOINT_DICT['left_ankle']
    right_ankle = KEYPOINT_DICT['right_ankle']
    left_ankle_x_value = keypoints_with_scores[0][0][left_ankle][1] # X-axis value of left knee. (Origin: Top left)
    right_ankle_x_value = keypoints_with_scores[0][0][right_ankle][1] # X-axis value of right knee. (Origin: Top left)


    # If the runner faces to the RIGHT side of the image, then the leading ankle is determined by the LARGER x-value.
    if running_direction == "right":
        if left_ankle_x_value > right_ankle_x_value:
            leading_ankle_this_frame = "left ankle"
        else:
            leading_ankle_this_frame = "right ankle"


    # If the runner faces to the LEFT side of the image, then the leading ankle is determined by the SMALLERü x-value.
    if running_direction == "left":
        if left_ankle_x_value < right_ankle_x_value:
            leading_ankle_this_frame = "left ankle"
        else:
            leading_ankle_this_frame = "right ankle"


    # The first time the leading ankle is determined, we simply assign it.
    if leading_ankle == "unknown":
        leading_ankle = leading_ankle_this_frame
    # If the leading ankle changes (from left to right or vice versa),
    # this means that a runner has taken one whole step. Visualize it, then you recognize that this is correct.
    elif leading_ankle != leading_ankle_this_frame:
        steps = total_steps + 1
        leading_ankle = leading_ankle_this_frame


    return steps, leading_ankle