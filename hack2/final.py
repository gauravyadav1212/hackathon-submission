import requests
from flask import Flask, render_template, request, send_from_directory
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
import requests

key_points = []
key_points_file = "keypoints.txt"
image_folder = "images"
output_folder = "slides"
path = 'slides'
out_path = ''
out_video_name = 'final_.mp4'
out_vid_full_path = os.path.join(out_path, out_video_name)


ai_content_api_url = "https://api.worqhat.com/api/ai/content/v2"
ai_content_api_key = "sk-aacd63f9197149de8940312a29cabb2f"  
video_generation_api_url = "https://api.worqhat.com/api/ai/images/generate/v3"
video_generation_api_key = "sk-aacd63f9197149de8940312a29cabb2f"

pre_imgs = os.listdir(path)
img = []

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_slides', methods=['POST'])
def generate_slides():
    num_slides = int(request.form['num_slides'])
    
    #This is the part where we use API
    '''
    def generate_slides_internal(num_slides):
        for i in range(1, num_slides + 1):
            image_path = os.path.join(image_folder, f"image{i}.png")
            SlideGen(key_points[i - 1], image_path, i)

        print(f"{num_slides} slides generated and saved successfully in the 'slides' folder.")
    headers = {
        "Authorization": f"Bearer {ai_content_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(ai_content_api_url, headers=headers)

    if response.status_code == 200:
        api_data = response.json()
        text = api_data['text']
        images = api_data['images']

        # Save text to keypoints.txt
        with open(key_points_file, 'w') as file:
            file.write(text)

        # Save images to the images folder
        for i, image_url in enumerate(images):
            image = requests.get(image_url)
            with open(os.path.join(image_folder, f"image{i + 1}.png"), 'wb') as img_file:
                img_file.write(image.content)

        # Generate slides using the received data
        generate_slides_internal(num_slides)

        # Generate video using the Video Generation API
        video_url = generate_video_with_api()
        if video_url:
            return render_template('result.html', video_url=video_url)
        else:
            return "Error generating video."
    else:
        return f"API request failed with status code: {response.status_code}"
    
    


    def generate_video_with_api():
    # Make a request to the Video Generation API
        headers = {
            "Authorization": f"Bearer {video_generation_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": "Your video generation text here",
            "images": ["image1.png", "image2.png"]  # Provide the image filenames you want to include in the video
        }
        response = requests.post(video_generation_api_url, headers=headers, json=payload)

        if response.status_code == 200:
            # Save the generated video to a file
            video_data = response.content
            with open(out_vid_full_path, 'wb') as video_file:
                video_file.write(video_data)
            return out_video_name
        else:
            return None

    '''

    if not os.path.exists(key_points_file):
        print(f"Error: The key points file '{key_points_file}' does not exist.")
        return False

    with open(key_points_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key_point_list = line.split(';')
                key_points.append(key_point_list)

    os.makedirs(output_folder, exist_ok=True)

    num_images = len([name for name in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, name))])

    if num_slides > num_images:
        print(f"Error: There are only {num_images} images in the '{image_folder}' folder, but you requested {num_slides} slides.")
        return False

    if num_slides > len(key_points):
        print(f"Error: The number of slides requested exceeds the number of available key points in 'keypoints.txt'.")
        return False

    def wrap_text(text, width=35):
        lines = []
        for line in text.splitlines():
            lines.extend([line[i:i+width] for i in range(0, len(line), width)])
        return "\n".join(lines)

    def SlideGen(key_points, image_path, i):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.26, 4.651))

        wrapped_text = wrap_text("\n".join(key_points))
        ax1.text(0.05, 0.5, wrapped_text, fontsize=12, verticalalignment='center')
        ax1.axis('off')

        img = Image.open(image_path)
        ax2.imshow(img)
        ax2.axis('off')
        output_file = os.path.join(output_folder, f"output_slide{i:02}.jpg")
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=300)

        plt.close()

    def generate_slides_internal(key_points, image_folder, output_folder, num_slides):
        for i in range(1, num_slides + 1):
            image_path = os.path.join(image_folder, f"image{i}.png")
            SlideGen(key_points[i - 1], image_path, i)

        print(f"{num_slides} slides generated and saved successfully in the 'slides' folder.")

        return True
    
    def generate_vid():
        success_ = generate_slides_internal(key_points, image_folder, output_folder, num_slides)

        if success_== False:
            return False

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

            return True

    generate_slides_internal(key_points, image_folder, output_folder, num_slides)
    success = generate_vid()
    if success:
        return render_template('result.html')
    else:
        return "Error generating slides."

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
    app.run(debug=True)

#The code below requires Application Default Credentials (ADC) to authenticate.
#But, it worked for us.

'''
"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="I just had a dream that we are gonna go to NY for hackathon and I put the Eiffel tower in front of the empire state building")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    # language_code="en-AU-Polyglot-1", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"'
'''