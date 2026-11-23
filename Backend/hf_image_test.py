from dotenv import dotenv_values
from huggingface_hub import InferenceClient
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
env_vars = dotenv_values(PROJECT_DIR / ".env")
token = env_vars.get("HuggingFaceAPIKey")

client = InferenceClient(
    provider="auto",
    api_key=token
)

def main():
    print("Generating image...")
    image = client.text_to_image(
        "a futuristic robotic AI assistant sitting in a high-tech laboratory",
        model="black-forest-labs/FLUX.1-schnell"
    )
    image.save(PROJECT_DIR / "hf_test.jpg")
    print("Image generated successfully!")
    print("Saved as hf_test.jpg")


if __name__ == "__main__":
    main()