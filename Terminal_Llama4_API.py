import base64
from openai import OpenAI
from easygui import fileopenbox
from PIL import Image
import io
from datetime import datetime
from rich.prompt import Prompt # https://rich.readthedocs.io/en/latest/

#Ask for your openrouter API key
APIKey = Prompt.ask("Enter your Openrouter API key: ", password=True)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
print('Pick one image from your local PC...')
image_path = fileopenbox(msg='Pick your image', default='*.jpg')
#Display the image side by side in oS window
selectedImage = Image.open(image_path)
print('Opening the image in your Operating System...')
selectedImage.show('Your uploaded Image')

print('Encoding the image...')
# Getting the Base64 string
base64_image = encode_image(image_path)

print('Connecting to Openrouter Llama4 Scout...')
client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=APIKey,
                )
start = datetime.now()
print('Reply:')
stream = client.chat.completions.create(
    extra_headers={},
    extra_body={},
    model="meta-llama/llama-4-scout:free",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What is in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            }
            }
        ]
        }
    ],
    max_tokens=1024,
    stream=True,
    temperature=0.4)
# Print the straming from the API call
for chunk in stream:
    print(chunk.choices[0].delta.content, end='',flush=True)
end = datetime.now() - start
print('\n---\n')
print(f'Completed in {end.total_seconds():.1f} seconds')