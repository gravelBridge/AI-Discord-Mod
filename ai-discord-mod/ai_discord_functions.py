from transformers import pipeline
from PIL import Image, ImageFile
import openai

ImageFile.LOAD_TRUNCATED_IMAGES = True

vqa_pipeline = pipeline("visual-question-answering")

async def image_is_safe():
    image =  Image.open("toModerate.jpeg")
    question = "Is the image safe for a public online community?"

    result = vqa_pipeline(image, question, top_k=1)[0]
    answer = result["answer"].lower()
    
    print(result)

    if result["score"] > 0.8 and answer.startswith("n"):
        return False
    return True


async def message_is_safe(message, apikey):
    openai.api_key = apikey

    response = openai.Moderation.create(
        input = message
    )
    try:
        if response["results"][0]["flagged"]:
            return False
        return True
    except:
        message_is_safe(message, apikey)