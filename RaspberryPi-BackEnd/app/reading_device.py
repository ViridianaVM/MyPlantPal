import requests

api_url = "http://52.233.91.25:5000/device_readings/my-plant-pal-001/all"

def get_device_reading():    
    response = requests.get(api_url)
    new_response = response.json()
    print(new_response)
    ###Get all info from new_response and send it to todo variable/JSON
    # todo = {"userId": 1, "title": "Buy milk", "completed": False}
    # response = requests.post(api_url, json=todo)
    # final_response = response.json()
    # print(final_response)


get_device_reading()


