def determine_distance_from_com_to_ankles(leading_ankle_x_value,
                                          trailing_ankle_x_value,
                                          distance_com_to_leading_ankle_all_images,
                                          distance_com_to_trailing_ankle_all_images,
                                          center_of_mass_x):


    # Calculate the distance between the center of mass (com) and the leading ankle.
    distance_com_to_leading_ankle = abs(center_of_mass_x - leading_ankle_x_value)
    distance_com_to_leading_ankle_all_images.append(distance_com_to_leading_ankle)

    # Calculate the distance between the center of mass (com) and the trailing ankle.
    distance_com_to_trailing_ankle = abs(center_of_mass_x - trailing_ankle_x_value)
    distance_com_to_trailing_ankle_all_images.append(distance_com_to_trailing_ankle)


    return distance_com_to_leading_ankle, distance_com_to_trailing_ankle, distance_com_to_leading_ankle_all_images, distance_com_to_trailing_ankle_all_images