import asyncio
from random import randint
from PIL import Image
from huggingface_hub import InferenceClient
from dotenv import dotenv_values
import os
from time import sleep
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "Data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
REQUEST_PATH = PROJECT_DIR / "Frontend" / "Files" / "ImageGeneration.data"

# Function to open and display images based on a given prompt
def open_images(prompt):
    prompt = prompt.replace(" ", "_")  # Replace spaces in the prompt with underscores

    # Generate the filenames for the images
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    for jpg_file in files:
        image_path = DATA_DIR / f"generated_{jpg_file}"
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


# API details for the Hugging Face Text-to-Image model
env_vars = dotenv_values(PROJECT_DIR / ".env")
HuggingFaceAPIKey = env_vars.get("HuggingFaceAPIKey")

client = InferenceClient(
    provider="auto",
    api_key=HuggingFaceAPIKey
)

# Async function to send a query to the Hugging Face API
async def query(prompt):
    image = await asyncio.to_thread(
        client.text_to_image,
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )
    return image


# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        image_prompt = (
            f"{prompt}, quality=4K, sharpness-maximum, "
            f"Ultra High details, high resolution, "
            f"seed {randint(0, 1000000)}"
        )

        task = asyncio.create_task(query(image_prompt))
        tasks.append(task)

    images = await asyncio.gather(*tasks)

    for i, image in enumerate(images):
        image_path = DATA_DIR / f"generated_{prompt.replace(' ', '_')}{i + 1}.jpg"
        image.save(image_path)


# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


def wait_for_generation_request():
    while True:
        try:
            with REQUEST_PATH.open("r", encoding="utf-8") as file:
                data = file.read().strip()

            if "," not in data or not data:
                print("Invalid data format in ImageGeneration.data. Skipping...")
                sleep(1)
                continue

            prompt, status = data.split(",", 1)

            if status.strip() == "True":
                print("Generating Images...")
                GenerateImages(prompt=prompt.strip())
                REQUEST_PATH.write_text("False, False", encoding="utf-8")
                break
            sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sleep(1)


if __name__ == "__main__":
    wait_for_generation_request()
