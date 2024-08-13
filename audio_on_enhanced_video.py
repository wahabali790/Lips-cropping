from moviepy.editor import VideoFileClip, AudioFileClip

# Load the video file
video_clip = VideoFileClip("./enhanced_video.mp4")

# Load the audio file
audio_clip = AudioFileClip("./temp_audio.wav")

# Set the audio of the video clip to the loaded audio
video_clip = video_clip.set_audio(audio_clip)

# Write the video file with the merged audio
video_clip.write_videofile("output_with_merged_audio.mp4")

# Close the clips
video_clip.close()
audio_clip.close()
