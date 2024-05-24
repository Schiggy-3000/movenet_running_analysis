# Imports
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches

import numpy as np
import cv2
from IPython.display import HTML, display
from PIL import Image

import tensorflow as tf
import tensorflow_hub as hub



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



# Maps bones to a matplotlib color name.
KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}



def _keypoints_and_edges_for_display(keypoints_with_scores,
                                     height,
                                     width,
                                     keypoint_threshold=0.11):
  """Returns high confidence keypoints and edges for visualization.

  Args:
    keypoints_with_scores: A numpy array with shape [1, 1, 17, 3] representing
      the keypoint coordinates and scores returned from the MoveNet model.
    height: height of the image in pixels.
    width: width of the image in pixels.
    keypoint_threshold: minimum confidence score for a keypoint to be
      visualized.

  Returns:
    A (keypoints_xy, edges_xy, edge_colors) containing:
      * the coordinates of all keypoints of all detected entities;
      * the coordinates of all skeleton edges of all detected entities;
      * the colors in which the edges should be plotted.
  """

  keypoints_all = []
  keypoint_edges_all = []
  edge_colors = []
  num_instances, _, _, _ = keypoints_with_scores.shape

  # Calcualte X and Y koordinates of all points
  for idx in range(num_instances):
    kpts_x = keypoints_with_scores[0, idx, :, 1]
    kpts_y = keypoints_with_scores[0, idx, :, 0]
    kpts_scores = keypoints_with_scores[0, idx, :, 2]
    kpts_absolute_xy = np.stack(
        [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
    kpts_above_thresh_absolute = kpts_absolute_xy[
        kpts_scores > keypoint_threshold, :]
    keypoints_all.append(kpts_above_thresh_absolute)

    # Construct lines between points
    for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
      if (kpts_scores[edge_pair[0]] > keypoint_threshold and
          kpts_scores[edge_pair[1]] > keypoint_threshold):
        x_start = kpts_absolute_xy[edge_pair[0], 0]
        y_start = kpts_absolute_xy[edge_pair[0], 1]
        x_end = kpts_absolute_xy[edge_pair[1], 0]
        y_end = kpts_absolute_xy[edge_pair[1], 1]
        line_seg = np.array([[x_start, y_start], [x_end, y_end]])
        keypoint_edges_all.append(line_seg)
        edge_colors.append(color)

  if keypoints_all:
    keypoints_xy = np.concatenate(keypoints_all, axis=0)
  else:
    keypoints_xy = np.zeros((0, 17, 2))

  if keypoint_edges_all:
    edges_xy = np.stack(keypoint_edges_all, axis=0)
  else:
    edges_xy = np.zeros((0, 2, 2))

  # keypoints_xy: All points that were determinet (with enough certainty 0.11)
  # edges_x_y: Lines between points
  # edge_colors: Color of lines
  return keypoints_xy, edges_xy, edge_colors



def draw_prediction_on_image(
    image,
    keypoints_with_scores,
    leading_ankle_x_value,
    center_of_mass_x,
    center_of_mass_y,
    center_of_mass_y_all_images,
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
    close_figure=False,
    output_image_height=None):
  """Draws the keypoint predictions on image.

  Args:
    image: A numpy array with shape [height, width, channel] representing the
      pixel values of the input image.
    keypoints_with_scores: A numpy array with shape [1, 1, 17, 3] representing
      the keypoint coordinates and scores returned from the MoveNet model.
    crop_region: A dictionary that defines the coordinates of the bounding box
      of the crop region in normalized coordinates (see the init_crop_region
      function below for more detail). If provided, this function will also
      draw the bounding box on the image.
    output_image_height: An integer indicating the height of the output image.
      Note that the image aspect ratio will be the same as the input image.

  Returns:
    A numpy array with shape [out_height, out_width, channel] representing the
    image overlaid with keypoint predictions.
  """
  
  height, width, channel = image.shape
  aspect_ratio = float(width) / height
  fig, ax = plt.subplots(figsize=(12 * aspect_ratio, 12))
  # To remove the huge white borders
  fig.tight_layout(pad=0)
  ax.margins(0)
  ax.set_yticklabels([])
  ax.set_xticklabels([])
  plt.axis('off')

  im = ax.imshow(image)
  line_segments = LineCollection([], linewidths=(4), linestyle='solid')
  ax.add_collection(line_segments)
  # Turn off tick labels 0
  scat = ax.scatter([], [], s=60, color='#FF1493', zorder=3)


  # Call other helper function (_keypoints_and_edges_for_display) to determine points (keypoint_locs) and lines (keypoint_edges) between points.
  (keypoint_locs, keypoint_edges, edge_colors) = _keypoints_and_edges_for_display(
       keypoints_with_scores, height, width)


  # Draw lines.
  if dict_params["lines"] == 1:
    line_segments.set_segments(keypoint_edges)
    line_segments.set_color(edge_colors)
    if keypoint_edges.shape[0]:
      line_segments.set_segments(keypoint_edges)
      line_segments.set_color(edge_colors)
  

  # Draw points.
  if dict_params["points"] == 1:
    if keypoint_locs.shape[0]:
      scat.set_offsets(keypoint_locs)


  # Draw a vertical line at the leading ankle.
  # This shall help to identify whether the center of mass is in the correct spot,
  # once the front foot makes contact with the ground.
  if dict_params["leading_ankle"] == 1:
    line_x_pixel = leading_ankle_x_value * width
    ax.axvline(x=line_x_pixel, color='red')


  # Draw center of mass.
  if dict_params["center_of_mass"] == 1:
    ax.scatter(center_of_mass_x * width, center_of_mass_y * height, color='red', s=700)


  # Draw colored rectangle between center of mass and leading ankle.
  if dict_params["leading_ankle_to_com"] == 1:
    rectangle_height = 20
    rectangle_corner = (center_of_mass_x * width, center_of_mass_y * height - (rectangle_height / 2))
    rectangle_width = leading_ankle_x_value * width - center_of_mass_x * width
    rectangle = patches.Rectangle(rectangle_corner, rectangle_width, rectangle_height, edgecolor='none', facecolor='yellow', alpha=0.3)
    ax.add_patch(rectangle)


  # Draw colored area for left knee angle.
  if dict_params["left_knee_angle_area"] == 1:
    hip = KEYPOINT_DICT['left_hip']
    knee = KEYPOINT_DICT['left_knee']
    ankle = KEYPOINT_DICT['left_ankle']

    hip_x = keypoints_with_scores[0][0][hip][1] * width
    hip_y = keypoints_with_scores[0][0][hip][0] * height
    knee_x = keypoints_with_scores[0][0][knee][1] * width
    knee_y = keypoints_with_scores[0][0][knee][0] * height
    ankle_x = keypoints_with_scores[0][0][ankle][1] * width
    ankle_y = keypoints_with_scores[0][0][ankle][0] * height

    triangle_coords = np.array([(hip_x, hip_y), (knee_x, knee_y), (ankle_x, ankle_y)])
    triangle = patches.Polygon(triangle_coords, closed=True, edgecolor='none', facecolor='yellow', alpha=0.3)
    ax.add_patch(triangle)


  # Draw colored area for right knee angle.
  if dict_params["right_knee_angle_area"] == 1:
    hip = KEYPOINT_DICT['right_hip']
    knee = KEYPOINT_DICT['right_knee']
    ankle = KEYPOINT_DICT['right_ankle']

    hip_x = keypoints_with_scores[0][0][hip][1] * width
    hip_y = keypoints_with_scores[0][0][hip][0] * height
    knee_x = keypoints_with_scores[0][0][knee][1] * width
    knee_y = keypoints_with_scores[0][0][knee][0] * height
    ankle_x = keypoints_with_scores[0][0][ankle][1] * width
    ankle_y = keypoints_with_scores[0][0][ankle][0] * height

    triangle_coords = np.array([(hip_x, hip_y), (knee_x, knee_y), (ankle_x, ankle_y)])
    triangle = patches.Polygon(triangle_coords, closed=True, edgecolor='none', facecolor='yellow', alpha=0.3)
    ax.add_patch(triangle)
  

  # Draw line at vertical distance min. and vertical distance max.
  if dict_params["vertical_distance"] == 1:
      center_of_mass_y_max = min(center_of_mass_y_all_images) # ATTENTION: The center of mass is measured from the top of the image. Therefore, min(...) yields the point where the center of mass was highest.
      center_of_mass_y_min = max(center_of_mass_y_all_images) # See one line above.
      y_max = center_of_mass_y_max * height
      y_min = center_of_mass_y_min * height
      ax.axhline(y=y_max, color='orange', linestyle='--')
      ax.axhline(y=y_min, color='orange', linestyle='--')
  

  # Add femur length as text.
  if dict_params["femur_length_txt"] == 1:
      pos_x = width * 0.35 # 2nd column
      pos_y = height * 0.9 # 2nd last pos.
      femur_length = round(max(femur_length_all_images), 2)
      text = "Femur length (relative to img): " + str(femur_length)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))
    

  # Add tibia length as text.
  if dict_params["tibia_length_txt"] == 1:
      pos_x = width * 0.35 # 2nd column
      pos_y = height * 0.95 # last pos.
      tibia_length = round(max(tibia_length_all_images), 2)
      text = "Tibia length (relative to img): " + str(tibia_length)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))
      

  # Add leg length as text.
  if dict_params["leg_length_txt"] == 1:
      pos_x = width * 0.35 # 2nd column
      pos_y = height * 0.85 # 3th last pos.
      leg_length = round(tibia_length + femur_length, 2)
      text = "Leg length (relative to img): " + str(leg_length)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))
  

  # Add vertical distance (relative to img) as text.
  if dict_params["vertical_distance_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.95 # last pos.
      vertical_distance =  round(abs(center_of_mass_y_max - center_of_mass_y_min), 2)
      text = "VD (relative to img): " + str(vertical_distance)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))


  # Add vertical distance (relative to leg length) as text.
  if dict_params["vertical_distance_rel_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.1 # 1st pos.
      vertical_distance_rel = round(vertical_distance / leg_length, 2)
      text = "VD (relative to leg length): " + str(vertical_distance_rel)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))


  # Add left knee angle (Femur/Tibia) as text.
  if dict_params["left_knee_angle_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.2 # 3th pos.
      knee_angle = int(round(left_knee_angle, 0))
      text = "Left knee angle: " + str(knee_angle)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))


  # Add right knee angle (Femur/Tibia) as text.
  if dict_params["right_knee_angle_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.25 # 4th pos.
      knee_angle = int(round(right_knee_angle, 0))
      text = "Right knee angle: " + str(knee_angle)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))


  # Add minimum knee angle (Femur/Tibia) as text.
  if dict_params["knee_angle_min_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.3 # 5th pos.
      left_knee_angle_min = min(left_knee_angle_all_images)
      right_knee_angle_min = min(right_knee_angle_all_images)
      knee_angle_min = int(round(min(left_knee_angle_min, right_knee_angle_min), 0))
      text = "Knee angle min.: " + str(knee_angle_min)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))

  
  # Add minimum left knee angle (Femur/Tibia) as text.
  if dict_params["left_knee_angle_min_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.85 # 3th last pos.
      knee_angle_min = int(round(min(left_knee_angle_all_images), 0))
      text = "Min. left knee angle: " + str(knee_angle_min)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))


  # Add minimum right knee angle (Femur/Tibia) as text.
  if dict_params["right_knee_angle_min_txt"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.9 # 2nd last pos.
      knee_angle_min = int(round(min(right_knee_angle_all_images), 0))
      text = "Min. right knee angle: " + str(knee_angle_min)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 0.3,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=0.3, pad=5))


  # Add total steps as text.
  if dict_params["total_steps"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.4 # 7th pos.
      text = "Total steps: " + str(total_steps)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))


  # Add cadence as text.
  if dict_params["cadence"] == 1:    
      pos_x = width * 0.02
      pos_y = height * 0.45 # 8th pos.
      text = "Cadence: " + str(cadence)
      ax.text(x=pos_x,
              y=pos_y,
              s=text,
              alpha = 1,
              fontsize=24,
              ha="left",
              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad=5))


  # ... for now this does nothing.
  if crop_region is not None:
    xmin = max(crop_region['x_min'] * width, 0.0)
    ymin = max(crop_region['y_min'] * height, 0.0)
    rec_width = min(crop_region['x_max'], 0.99) * width - xmin
    rec_height = min(crop_region['y_max'], 0.99) * height - ymin
    rect = patches.Rectangle(
        (xmin,ymin),rec_width,rec_height,
        linewidth=1,edgecolor='b',facecolor='none')
    ax.add_patch(rect)
  

  # Render entire image and convert it to numpy array.
  fig.canvas.draw()
  image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
  image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
  plt.close(fig)


  # Resize image to output_image_height.
  # Careful, this can lead to color changes in the image due to interpolation method.
  if output_image_height is not None:
    output_image_width = int(output_image_height / height * width)
    image_from_plot = cv2.resize(image_from_plot, dsize=(output_image_width, output_image_height), interpolation=cv2.INTER_CUBIC)


  return image_from_plot