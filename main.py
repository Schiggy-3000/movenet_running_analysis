import numpy as np
import tensorflow as tf
from crop_image import init_crop_region
from crop_image import determine_crop_region
from model import run_inference
from draw_metrics_on_image import draw_prediction_on_image
from determine_running_direction import determine_running_direction
from determine_leading_and_trailing_ankle import determine_leading_and_trailing_ankle
from determine_center_of_mass import determine_center_of_mass
from determine_distance_from_com_to_ankles import determine_distance_from_com_to_ankles
from determine_femur_length import determine_femur_length
from determine_tibia_length import determine_tibia_length
from create_gif import create_gif
from create_mp4 import create_mp4
from determine_knee_angles import determine_knee_angles
from determine_steps import determine_steps
from determine_cadence import determine_cadence



# Notes:
# The "Nullpunkt" of the coordinate system is in the top left.
# The leg length is calculated from femur + tibia. femur = max(hip - knee) & tibia = max(knee - ankle). If the frame rate of the gif is low, those max() values won't capture the actual maximal length of the femur and tibia.
# The number of steps is based on ankles. Whenever the leading ankle changes -> steps + 1. The issue is, that movenet_thunder is not that accurate and ankle keypoints can jump around significantly. The leading ankle can therefore change more often than it is actually the case.



# To Do's:
# Vertical distance (VD_stance, VD_flight)  --> Benötigt Erkennung für Bodenkontakt.
# T_stance, T_flight                        --> Benötigt Erkennung für Bodenkontakt.
# Schrittlänge                              --> ...
# Winkel Ellbogen                           --> Bereits jetzt machbar.
# Abstosswinkel                             --> Benötigt Erkennung für Bodenkontakt.
# Auftrittswinkel                           --> Benötigt Erkennung für Bodenkontakt.
# Kadenz                                    --> Video muss in Echtzeit abspielen.



# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}



print("------------------------------------------------------------------------")
print("Read configurations ...")
dict_params = {}
dict_params["fps"] = 15                               # Duration each frame of gif will be shown. Careful, determine_cadence.py is influenced by this.
dict_params["points"] = 1                             # Show points where joints are.
dict_params["lines"] = 0                              # Show lines between points (joints).
dict_params["leading_ankle"] = 1                      # Show line at leading ankle.
dict_params["trailing_ankle"] = 1                     # Show line at trailing ankle.
dict_params["leading_ankle_max"] = 0                  # Show line at max. value the leading ankle has reached so far. --> Can be misleading when runner is not always at the center of the video (the max. value is an absolute x-value).
dict_params["trailing_ankle_max"] = 0                 # Show line at max. value the trailing ankle has reached so far. --> Can be misleading when runner is not always at the center of the video (the max. value is an absolute x-value).
dict_params["leading_ankle_to_com_txt"] = 0           # Show max. distance between the leading ankle and the center of mass (com) relative to leg length.
dict_params["trailing_ankle_to_com_txt"] = 0          # Show max. distance between the trailing ankle and the center of mass (com) relative to leg length.
dict_params["leading_ankle_to_com_max_txt"] = 1       # Show max. distance between the leading ankle and the center of mass (com) relative to leg length.
dict_params["trailing_ankle_to_com_max_txt"] = 1      # Show max. distance between the trailing ankle and the center of mass (com) relative to leg length.
dict_params["center_of_mass"] = 1                     # Show center of mass.
dict_params["leading_ankle_to_com"] = 1               # Show colored area between leading ankle and center of mass.
dict_params["vertical_distance"] = 1                  # Show lines at min. and max. vertical position of center of mass.
dict_params["vertical_distance_txt"] = 0              # Show vertical distance as text (relative to image height).
dict_params["vertical_distance_rel_txt"] = 1          # Show vertical distance as text (relative to leg length).
dict_params["femur_length_txt"] = 0                   # Show femur length as text.
dict_params["tibia_length_txt"] = 0                   # Show tibia length as text.
dict_params["leg_length_txt"] = 0                     # Show leg length as text.
dict_params["left_knee_angle_txt"] = 1                # Show left knee angle (Femur/Tibia) as text.
dict_params["right_knee_angle_txt"] = 1               # Show right knee angle (Femur/Tibia) as text.
dict_params["knee_angle_min_txt"] = 1                 # Show minimum knee angle (Femur/Tibia) as text.
dict_params["left_knee_angle_min_txt"] = 0            # Show minimum left knee angle (Femur/Tibia) as text.
dict_params["right_knee_angle_min_txt"] = 0           # Show minimum right knee angle (Femur/Tibia) as text.
dict_params["left_knee_angle_area"] = 1               # Show colored area for knee angle.
dict_params["right_knee_angle_area"] = 1              # Show colored area for knee angle.
dict_params["total_steps"] = 1                        # Show colored area for knee angle.
dict_params["cadence"] = 1                            # Show colored area for knee angle.



print("------------------------------------------------------------------------")
print("Load input ...")
raw_data_dir = './Raw_data/Gifs/'                     # Raw data (GIFs) that running analysis will be applied to.
video_dir = './Processed_data/Videos/'                # Running analysis is stored as MP4 in this folder.
gif_dir = './Processed_data/Gifs/'                    # Running analysis is stored as GIF in this folder.
gif_name = 'eliud_kipchoge_sub2_marathon.gif'
gif_name = 'jes_woods_nike_coach_1.gif'
#gif_name = 'jes_woods_nike_coach_2.gif'
#gif_name = 'haile_gebrselassie_olympion_gold.gif'
#gif_name = 'random_man.gif'
image = tf.io.read_file(raw_data_dir + gif_name)
image = tf.image.decode_gif(image)
num_frames, image_height, image_width, _ = image.shape
crop_region = init_crop_region(image_height, image_width)



print("------------------------------------------------------------------------")
print("Load model ...")
module = tf.saved_model.load("./Models/singlepose_thunder")
model = module.signatures['serving_default']



print("------------------------------------------------------------------------")
print("Start inference ...")
input_size = 256
total_steps = 0                     # This is a counter for the steps taken by a given runner.
leading_ankle_all_images = []       # The leading ankle in each frame is stored in this array.
cadence = 0                         # Initial cadence is set to 0. Is updated every 10 frames (= every second).
output_images = []
center_of_mass_y_all_images = []
distance_com_to_leading_ankle_all_images = []   # Contains the horizontal distance from the center of mass (com) to the leading ankle in all images.
distance_com_to_trailing_ankle_all_images = []  # Contains the horizontal distance from the center of mass (com) to the trailing ankle in all images.
leading_ankle_x_max_value_all_images = None
trailing_ankle_x_min_value_all_images = None
femur_length_all_images = []
tibia_length_all_images = []
left_knee_angle_all_images = []
right_knee_angle_all_images = []

for frame_idx in range(num_frames):
  
  
  # Print status update to the console.
  print(f'\rFrame {frame_idx + 1} of {num_frames} total frames in process', end='', flush=True)


  # Find points (= make inference).
  keypoints_with_scores = run_inference(
    model,
    image[frame_idx, :, :, :],
    crop_region, crop_size=[input_size, input_size])
  

  # Determine running direction.
  # angle_degrees: Angle between femur/tibia clockwise
  (running_direction, angle_degrees) = determine_running_direction(keypoints_with_scores, KEYPOINT_DICT)


  # Determine leading and trailing ankle.
  (leading_ankle_x_value,
   trailing_ankle_x_value,
   leading_ankle_x_max_value_all_images,
   trailing_ankle_x_min_value_all_images) = determine_leading_and_trailing_ankle(keypoints_with_scores,
                                                                                 KEYPOINT_DICT,
                                                                                 running_direction,
                                                                                 leading_ankle_x_max_value_all_images,
                                                                                 trailing_ankle_x_min_value_all_images)


  # Determine center of mass.
  (center_of_mass_x, center_of_mass_y) = determine_center_of_mass(keypoints_with_scores, KEYPOINT_DICT)


  # Determine distance between center of mass and leading/trailing ankle.
  (distance_com_to_leading_ankle,
   distance_com_to_trailing_ankle,
   distance_com_to_leading_ankle_all_images,
   distance_com_to_trailing_ankle_all_images) = determine_distance_from_com_to_ankles(leading_ankle_x_value,
                                                                                      trailing_ankle_x_value,
                                                                                      distance_com_to_leading_ankle_all_images,
                                                                                      distance_com_to_trailing_ankle_all_images,
                                                                                      center_of_mass_x)


  # Determine vertical distance.
  # This is done by collecting all center_of_mass_x and then finding min. and max. values.
  center_of_mass_y_all_images.append(center_of_mass_y)


  # Determine femur length.
  (femur_length_left, femur_length_right) = determine_femur_length(keypoints_with_scores, KEYPOINT_DICT)
  femur_length_all_images.append(femur_length_left)
  femur_length_all_images.append(femur_length_right)


  # Determine tibia length.
  (tibia_length_left, tibia_length_right) = determine_tibia_length(keypoints_with_scores, KEYPOINT_DICT)
  tibia_length_all_images.append(tibia_length_left)
  tibia_length_all_images.append(tibia_length_right)


  # Determine knee angles.
  (left_knee_angle, right_knee_angle) = determine_knee_angles(keypoints_with_scores, KEYPOINT_DICT)
  left_knee_angle_all_images.append(left_knee_angle)
  right_knee_angle_all_images.append(right_knee_angle)


  # Determine_steps (= step counter).
  (total_steps, leading_ankle_all_images) = determine_steps(keypoints_with_scores, KEYPOINT_DICT, total_steps, running_direction, leading_ankle_all_images)
  

  # Determine cadence.
  cadence = determine_cadence(cadence, frame_idx, total_steps)

  
  # Draw assets on image.
  output_images.append(draw_prediction_on_image(
      image[frame_idx, :, :, :].numpy().astype(np.int32),
      keypoints_with_scores,
      leading_ankle_x_value,
      trailing_ankle_x_value,
      leading_ankle_x_max_value_all_images,
      trailing_ankle_x_min_value_all_images,
      center_of_mass_x,
      center_of_mass_y,
      center_of_mass_y_all_images,
      distance_com_to_leading_ankle,
      distance_com_to_trailing_ankle,
      distance_com_to_leading_ankle_all_images,
      distance_com_to_trailing_ankle_all_images,
      femur_length_all_images,
      tibia_length_all_images,
      left_knee_angle,
      right_knee_angle,
      left_knee_angle_all_images,
      right_knee_angle_all_images,
      total_steps,
      cadence,
      dict_params,
      crop_region=None,
      close_figure=True,
      output_image_height=600)) # Creating an mp4 might require you to adjust this value (e.g. multiple of 16). 
  
  crop_region = determine_crop_region(keypoints_with_scores, KEYPOINT_DICT, image_height, image_width)



print("\n")
print("------------------------------------------------------------------------")
print("Create Gif ...")
output = np.stack(output_images, axis=0)
gif_duration = int(1000 * 1/ dict_params["fps"])
create_gif(output, gif_duration, gif_dir, gif_name)



print("------------------------------------------------------------------------")
print("Create MP4 ...")
output = np.stack(output_images, axis=0)
video_name = gif_name.replace('.gif', '.mp4')
create_mp4(output, video_dir, video_name)



print("------------------------------------------------------------------------")
print("Program finished")