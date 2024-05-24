# This function NEEDS TO BE STREAMLINED.
# The step counter is still messed up whenever movenet_thunder keypoints wiggle around too much.


def determine_steps(keypoints_with_scores, KEYPOINT_DICT, total_steps, running_direction, leading_ankle_all_images):

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


    # If the runner faces to the LEFT side of the image, then the leading ankle is determined by the SMALLER x-value.
    if running_direction == "left":
        if left_ankle_x_value < right_ankle_x_value:
            leading_ankle_this_frame = "left ankle"
        else:
            leading_ankle_this_frame = "right ankle"
    

    # Store leading ankle.
    leading_ankle_all_images.append(leading_ankle_this_frame)


    # Step counter logic:
    # If the leading ankle changes (from left to right or vice versa),
    # this means that a runner has taken one whole step. Visualize it, then you recognize that this is correct.
    # Somethimes movenet_thunder is not that accurate and
    # the positions for (ankle) joints wiggle around significantly from frame to frame.
    # This can mess with the step count. In light of this, the step count is only increased whenever
    # the leading ankle has changed for several consecutive frames.
    same_ankle_in_x_frames = 3
    different_ankle_before_that = same_ankle_in_x_frames + 1

    # Check if array contains enough elements.
    if len(leading_ankle_all_images) >= different_ankle_before_that:

        # Check if the X newest elements are equal.
        if leading_ankle_all_images[-same_ankle_in_x_frames:] == [leading_ankle_all_images[-1]] * same_ankle_in_x_frames:
            
            # Check if the element before the X newest elements is different.
            if leading_ankle_all_images[-1] != leading_ankle_all_images[-different_ankle_before_that]:
                
                steps = total_steps + 1


    return steps, leading_ankle_all_images