
def determine_leading_and_trailing_ankle(keypoints_with_scores,
                                         KEYPOINT_DICT,
                                         running_direction,
                                         leading_ankle_x_max_value_all_images,
                                         trailing_ankle_x_min_value_all_images):

    left_ankle = KEYPOINT_DICT['left_ankle']
    right_ankle = KEYPOINT_DICT['right_ankle']

    left_ankle_x_value = keypoints_with_scores[0][0][left_ankle][1] # X-axis value of left knee. (Origin: Top left)
    right_ankle_x_value = keypoints_with_scores[0][0][right_ankle][1] # X-axis value of right knee. (Origin: Top left)



    # If runner runs towards the RIGHT SIDE of the image, the leading ankle is determined by max().
    if running_direction == "right":

        # ------------ Leading ankle ------------

        # Determine x value of leading ankle.
        leading_ankle_x_value = max(left_ankle_x_value, right_ankle_x_value)

        # At the start, there is no value assigned to this variable, therefore we set an initial value.
        if leading_ankle_x_max_value_all_images == None:
            leading_ankle_x_max_value_all_images = leading_ankle_x_value

        # If the x value of the current leading ankle reaches a new extreme value, overwrite the previous value.
        if leading_ankle_x_value > leading_ankle_x_max_value_all_images:
            leading_ankle_x_max_value_all_images = leading_ankle_x_value

        # ------------ Trailing ankle ------------

        # Determine x value of trailing ankle.
        trailing_ankle_x_value = min(left_ankle_x_value, right_ankle_x_value)

        # At the start, there is no value assigned to this variable, therefore we set an initial value.
        if trailing_ankle_x_min_value_all_images == None:
            trailing_ankle_x_min_value_all_images = trailing_ankle_x_value

        # If the x value of the current trailing ankle reaches a new extreme value, overwrite the previous value.
        if trailing_ankle_x_value < trailing_ankle_x_min_value_all_images:
            trailing_ankle_x_min_value_all_images = trailing_ankle_x_value


    # If runner runs towards the LEFT SIDE of the image, the leading ankle is determined by min().
    elif running_direction == "left":

        # ------------ Leading ankle ------------

        # Determine x value of leading ankle.
        leading_ankle_x_value = min(left_ankle_x_value, right_ankle_x_value)

        # At the start, there is no value assigned to this variable, therefore we set an initial value.
        if leading_ankle_x_max_value_all_images == None:
            leading_ankle_x_max_value_all_images = leading_ankle_x_value

        # If the x value of the current leading ankle reaches a new extreme value, overwrite the previous value.
        if leading_ankle_x_value < leading_ankle_x_max_value_all_images:
            leading_ankle_x_max_value_all_images = leading_ankle_x_value

        # ------------ Trailing ankle ------------

        # Determine x value of trailing ankle.
        trailing_ankle_x_value = max(left_ankle_x_value, right_ankle_x_value)

        # At the start, there is no value assigned to this variable, therefore we set an initial value.
        if trailing_ankle_x_min_value_all_images == None:
            trailing_ankle_x_min_value_all_images = trailing_ankle_x_value

        # If the x value of the current leading ankle reaches a new extreme value, overwrite the previous value.
        if trailing_ankle_x_value > trailing_ankle_x_min_value_all_images:
            trailing_ankle_x_min_value_all_images = trailing_ankle_x_value

    
    return leading_ankle_x_value, trailing_ankle_x_value, leading_ankle_x_max_value_all_images, trailing_ankle_x_min_value_all_images
    