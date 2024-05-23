import imageio
from tensorflow_docs.vis import embed



def create_mp4(images, video_dir, video_name):
    """Converts image sequence (4D numpy array) to mp4 video."""
    
    # Define the storage location.
    storage_location = video_dir + 'ANNOTATED_' + video_name

    # Save the video using imageio.
    # Default FPS = 10 (Rechtsklick auf Video > Eigenschaften > Details > Einzelbildrate).
    imageio.mimwrite(uri=storage_location, ims=images)

    return embed.embed_file(storage_location)