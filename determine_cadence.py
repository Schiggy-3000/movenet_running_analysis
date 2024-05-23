def determine_cadence(current_cadence, frame_idx, total_steps):

    cadence = current_cadence
    frame = frame_idx + 1

    # Cadence is only updated every 10th frame.
    # By default, an MP4 video has 10 FPS. That is why this approach was chosen.
    if frame % 10 == 0:
        
        # By default, an MP4 video has 10 frames per second.
        # We get the amounts of seconds by dividing frames by 10.
        video_play_time_in_seconds = frame / 10
        
        # Cadence (steps/min)
        steps_per_second = total_steps / video_play_time_in_seconds
        steps_per_minute = steps_per_second * 60
        cadence = int(round(steps_per_minute, 0))

    return cadence