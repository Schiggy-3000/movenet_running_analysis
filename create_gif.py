import imageio
from tensorflow_docs.vis import embed



def create_gif(images, duration, gif_dir, gif_name):
  """Converts image sequence (4D numpy array) to gif."""

  # Define the storage location.
  storage_location = gif_dir + 'ANNOTATED_' + gif_name

  # Save GIF.
  imageio.mimsave(storage_location,
                  images,
                  duration=duration,
                  loop=0 # Makes gif run infinitely
                  )
  
  return embed.embed_file(storage_location)