import json
import requests
import urllib.request
from PIL import Image
from keys import API_KEY
from keys import SYNONYM_KEY

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
OD_URL ="https://api.edenai.run/v2/image/object_detection"
T2S_URL ="https://api.edenai.run/v2/audio/text_to_speech"
TR_URL ="https://api.edenai.run/v2/translation/automatic_translation"


def get_object_details(items):
    detailed_items = {}
    for i in range(0,len(items)):
        item = items[i]
        text = item["label"]
        payload1={"providers": "google", "language": "en-US", "option":"MALE", "text": text}
        response1 = requests.post(T2S_URL, json=payload1, headers=HEADERS)
        result1 = json.loads(response1.text)
        item["audio_resource_url"] = result1['google']['audio_resource_url']
        
        payload2={"providers": "phedone", 'source_language':"en", 'target_language':"uz", 'text': text}
        response2 = requests.post(TR_URL, json=payload2, headers=HEADERS)
        result2 = json.loads(response2.text)
        item["translation"]= result2['phedone']['text']
        
        payload3={"providers": "microsoft", "language": "uz-UZ", "option":"MALE", "text": result2['phedone']['text']}
        response3 = requests.post(T2S_URL, json=payload3, headers=HEADERS)
        result3 = json.loads(response3.text)
        item["audio_resource_url2"] = result3['microsoft']['audio_resource_url']
        detailed_items[i] = item
    return detailed_items

def get_objects_list(image_address):
    
  json_payload={"providers": "api4ai", "file_url": image_address}
  response = requests.post(OD_URL, json=json_payload, headers=HEADERS)
  result = json.loads(response.text)
  results = result["api4ai"]["items"]
  return results


def crop_image(url,item):
    # Download the image from the URL
    urllib.request.urlretrieve(url, "image.jpg")
    img_path = f"media/{item['label']}_cropped_image.jpg"

    # Open the downloaded image
    image = Image.open("image.jpg")

    # Specify the crop coordinates
    x_min = item['x_min']  # Replace with the actual x_min value
    x_max = item['x_max']  # Replace with the actual x_max value
    y_min = item['y_min']  # Replace with the actual y_min value
    y_max = item['y_max']  # Replace with the actual y_max value

    # Crop the image using the specified coordinates
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    cropped_image.save(img_path)
    return img_path


# def summurize(text):
#     url ="https://api.edenai.run/v2/text/summarize"
#     payload={"providers": "openai", "language": "en", "text": text}
#     response = requests.post(url, json=payload, headers=HEADERS)
#     result = json.loads(response.text)['openai']['result']
#     payload1={"providers": "google", "language": "en-US", "option":"MALE", "text": result}
#     response1 = requests.post(T2S_URL, json=payload1, headers=HEADERS)
#     result1 = json.loads(response1.text)
#     return result1['google']['audio_resource_url']


def get_synonyms_and_antonyms(word):
    url = "https://api.api-ninjas.com/v1/thesaurus?word="
    response = requests.get(url+word, headers={"X-Api-Key": SYNONYM_KEY})