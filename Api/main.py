import requests
import sys
import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../input"))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OPTIMIZER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../NextFace"))

def get_next_filename(folder, base_name="imageExample", ext=".png"):
    os.makedirs(folder, exist_ok=True)
    number = 1
    while os.path.exists(os.path.join(folder, f"{base_name}{number}{ext}")):
        number += 1
    return os.path.join(folder, f"{base_name}{number}{ext}")

def download_image(image_url, save_path):
    response = requests.get(image_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Download Completed: {save_path}")

def create_image(prompt, width=960, height=720, seed=42, model='flux'):
    image_url = f"https://pollinations.ai/p/{prompt} fullface?width={width}&height={height}&seed={seed}&model={model}"
    save_path = get_next_filename(IMAGES_DIR)
    download_image(image_url, save_path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = input("Write down description for your char: ")

    create_image(prompt)