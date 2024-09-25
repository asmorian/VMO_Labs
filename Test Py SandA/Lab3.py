import cv2
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def detect_lightning(current_frame, previous_frame, threshold=10):
    # Convert frames to grayscale
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between the current frame and the previous frame
    diff = cv2.absdiff(current_gray, previous_gray)

    # Calculate the mean brightness of the difference
    mean_diff = np.mean(diff)

    # Return True if the mean difference exceeds the threshold
    return mean_diff > threshold


def process_video(input_path, output_dir, buffer_seconds=5, threshold=50):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    lightning_times = []
    buffer_frames = int(buffer_seconds * fps)

    prev_frame = None
    frame_times = []

    for frame_idx in range(frame_count):
        ret, current_frame = cap.read()
        if not ret:
            break

        current_time = frame_idx / fps

        if prev_frame is not None:
            if detect_lightning(current_frame, prev_frame, threshold):
                lightning_times.append(current_time)

        prev_frame = current_frame

    cap.release()

    # Save segments with lightning
    for lightning_time in lightning_times:
        start_time = max(0, int(lightning_time - buffer_seconds))
        end_time = min(duration, lightning_time + buffer_seconds)
        output_path = f"{output_dir}/lightning_{start_time:.2f}_{end_time:.2f}.mp4"
        ffmpeg_extract_subclip(input_path, start_time, end_time, targetname=output_path)


if __name__ == "__main__":
    input_path = "D:/vid/VID_20240609_144337.mp4"
    output_dir = "D:/vid/new_vid"
    process_video(input_path, output_dir)
