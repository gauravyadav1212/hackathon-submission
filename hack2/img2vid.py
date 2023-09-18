import cv2
import os

path = 'slides'
out_path = ''
out_video_name = 'final_.mp4'
out_vid_full_path = os.path.join(out_path, out_video_name)

pre_imgs = os.listdir(path)
img = []

for i in pre_imgs:
    i = os.path.join(path, i)
    if os.path.isfile(i):  # Check if it's a file
        img.append(i)
    else:
        print(f"Skipped: {i} is not a file or doesn't exist.")

if not img:
    print("No valid image files found.")
else:
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    frame = cv2.imread(img[0])
    if frame is not None:
        size = (frame.shape[1], frame.shape[0])  # Get frame width and height
    else:
        print(f"Unable to read the first image: {img[0]}")

    # Define a default size in case the frame is not read
    if 'size' not in locals():
        size = (640, 480)  # Default size, you can change this

    # Now you can proceed with creating the video.
    video = cv2.VideoWriter(out_vid_full_path, cv2_fourcc, 30, size)  # 30 frames per second

    # Specify how many times you want to repeat each image (duration)
    repeat_factor = [5, 2.5, 3, 1.7, 1, 3, 2, 1]  # Each image will be shown for 2 seconds (30 frames per second * 2 seconds)
    repeat_factor = [int(x * 30) for x in repeat_factor]

    for i in range(len(img)):
        if i > 0:
            # Add a 300 ms (10 frames) fade transition between images
            fade_duration = 10
            for j in range(fade_duration):
                alpha = j / fade_duration
                beta = 1 - alpha
                blended_frame = cv2.addWeighted(cv2.imread(img[i - 1]), beta, cv2.imread(img[i]), alpha, 0)
                video.write(blended_frame)

        for _ in range(repeat_factor[i]):
            video.write(cv2.imread(img[i]))

    video.release()
