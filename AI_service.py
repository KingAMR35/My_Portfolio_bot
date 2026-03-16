import requests
import time
import io
import os
from dotenv import load_dotenv
 
def generate_leonardo_image(prompt):
    load_dotenv()
    api_key = os.getenv('api_key')
    authorization = f"Bearer {api_key}"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authorization
    }
    
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    
    payload = {
        "height": 512,
        "width": 512,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", 
        "prompt": prompt
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        return None, "❌ Ошибка API: " + str(response.status_code)
    
    generation_id = response.json()['sdGenerationJob']['generationId']

    for i in range(20):
        time.sleep(3)
        result_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        response = requests.get(result_url, headers=headers)
        data = response.json()
        
        if data["generations_by_pk"]["generated_images"]:
            image_url = data["generations_by_pk"]["generated_images"][0]["url"]
            image_data = requests.get(image_url).content
            
            img_buffer = io.BytesIO(image_data)
            return img_buffer, "✅ Изображение сгенерировано!"
    
    return None, "⏰ Таймаут генерации (60 сек)"
