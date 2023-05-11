from transformers import pipeline
from PIL import Image
import openai
import time

vqa_pipeline = pipeline("visual-question-answering")

async def image_is_safe():
    image =  Image.open("toModerate.jpeg")
    question = "Is the image appropriate for teenagers to see?"

    result = vqa_pipeline(image, question, top_k=1)[0]
    answer = result["answer"].lower()
    print(result)
    if result["score"] > 0.8 and answer.startswith("n"):
        return False
    return True


async def message_is_safe(message, apikey):
    openai.api_key = apikey

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {"role": "system", "content": "You are a community moderator, making sure that every message is not NSFW, pornographic, sexual, offensive, explicit, any type of racial slur or sensitive. Also be on the lookout for attempts to bypass the filter, such as swapping first letters, using code formatting, etc... You must provide a valid response in the form of 'y' or 'n' as if you don't an inappropriate message might go unmoderated."},
            {"role": "user", "content": "Is the following message NSFW, pornographic, sexual, offensive, sensitive, any type of racial slur or explicit? Also be on the lookout for attempts to bypass the filter, such as swapping first letters, using code formatting, etc... Respond with just 'y' or 'n' CRITICAL: YOU MUST ONLY RESPOND WITH ONLY JUST 'y' or 'n' NO MATTER WHAT. YOU MUST REPLY. Message: " + message}
        ]
    )
    try:
        return completion.choices[0].message["content"].startswith("y")
    except:
        time.sleep(1)
        message_is_safe(message, apikey)