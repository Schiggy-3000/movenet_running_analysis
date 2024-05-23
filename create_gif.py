
import imageio
from tensorflow_docs.vis import embed


def create_gif(images, duration, gif_dir, gif_name):
  """Converts image sequence (4D numpy array) to gif."""

  storage_location = gif_dir + 'ANNOTATED_' + gif_name
  imageio.mimsave(storage_location, images, duration=duration)
  
  return embed.embed_file(storage_location)