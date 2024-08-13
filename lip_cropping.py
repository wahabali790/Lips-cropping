import cv2
import dlib
from moviepy.editor import VideoFileClip, AudioFileClip

# Load pre-trained face detector
face_detector = dlib.get_frontal_face_detector()

# Load facial landmark predictor
predictor_path = "./models/shape_predictor_68_face_landmarks.dat"  # You need to download this file
landmark_predictor = dlib.shape_predictor(predictor_path)

# Load video
video_path = "./Testing_samples/testing.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('./outputs/output_lips_video_without_audio.mp4', fourcc, fps, (100, 100))  # Adjust dimensions as needed

# Initialize a list to store video frames
video_frames = []

# Initialize a list to store audio frames
audio_frames = []

# Initialize a counter for the number of frames processed
frame_count = 0

# Loop through each frame in the input video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray)

    lips_roi = None  # Initialize lips ROI

    for face in faces:
        # Predict facial landmarks
        landmarks = landmark_predictor(gray, face)

        # Extract coordinates of lips
        lips_x = [landmarks.part(n).x for n in range(48, 61)]
        lips_y = [landmarks.part(n).y for n in range(48, 61)]

        # Find the minimum and maximum coordinates of the lips
        min_x = min(lips_x)-50
        min_y = min(lips_y)-50
        max_x = max(lips_x)+50
        max_y = max(lips_y)+50

        # Ensure the ROI stays within the frame boundaries
        min_x = max(0, min_x)
        min_y = max(0, min_y)
        max_x = min(frame.shape[1], max_x)
        max_y = min(frame.shape[0], max_y)

        # Crop the lips region
        lips_roi = frame[min_y:max_y, min_x:max_x]

        # Resize the lips ROI to a fixed size (for consistent output video dimensions)
        lips_roi_resized = cv2.resize(lips_roi, (100, 100))  # Adjust dimensions as needed

    # Write lips ROI to output video
    output_video.write(lips_roi_resized if lips_roi is not None else frame)

    # Store the frame in the list of video frames
    video_frames.append(frame)

    # Increment the frame count
    frame_count += 1

    # Break the loop when all frames have been processed
    if frame_count >= num_frames:
        break

# Release video objects
cap.release()
output_video.release()

# Read audio from the input video
audio_clip = AudioFileClip(video_path)

# Extract the audio corresponding to the number of frames processed
audio_clip = audio_clip.subclip(0, frame_count / fps)

# Write the audio to a temporary file
temp_audio_path = "./outputs/temp_audio.wav"
audio_clip.write_audiofile(temp_audio_path)

# Read the video file with merged audio
video_clip = VideoFileClip("./outputs/output_lips_video_without_audio.mp4")

# Load the audio file
audio_clip = AudioFileClip(temp_audio_path)

# Set the audio of the video clip to the loaded audio
video_clip = video_clip.set_audio(audio_clip)

# Write the final video file with merged audio
video_clip.write_videofile("./outputs/output_with_merged_audio.mp4")

# Close the clips
video_clip.close()
audio_clip.close()
