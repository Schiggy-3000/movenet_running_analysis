import tensorflow as tf
from crop_image import crop_and_resize



def run_inference(model, image, crop_region, crop_size):
  """Runs model inference on the cropped region.

  The function runs the model inference on the cropped region and updates the
  model output to the original image coordinate system.
  """
  
  image_height, image_width, _ = image.shape
  input_image = crop_and_resize(tf.expand_dims(image, axis=0), crop_region, crop_size=crop_size)


  # Model expects tensor type of int32.
  input_image = tf.cast(input_image, dtype=tf.int32)
  

  # Run model inference.
  keypoints_with_scores = model(input_image)
  keypoints_with_scores = keypoints_with_scores["output_0"].numpy() # tf.Tensor elements can't be changed, therefore we convert to numpy array.
  #print("Keypoint with scores: ", keypoints_with_scores[0][0])


  # Update the coordinates.
  for idx in range(17):

    # Update Y coordinate of point.
    tmp_y = (
        crop_region['y_min'] * image_height +
        crop_region['height'] * image_height *
        keypoints_with_scores[0][0][idx][0]) / image_height
    keypoints_with_scores[0][0][idx][0] = tmp_y
    
    # Update X coordinate of point.
    tmp_x = (
        crop_region['x_min'] * image_width +
        crop_region['width'] * image_width *
        keypoints_with_scores[0][0][idx][1]) / image_width
    keypoints_with_scores[0][0][idx][1] = tmp_x
    

  return keypoints_with_scores