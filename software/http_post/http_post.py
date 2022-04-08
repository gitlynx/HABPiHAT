import requests

def post_results(endpoints: list, data: dict):
    """
        Construct HTTP POST from given data and send it to each item of the given list
        ref: https://www.geeksforgeeks.org/get-post-requests-using-python/

        @param endpoints: list of dictionaries with the following elements:
            endpoint: str --> http URL of the endpoint
            apikey: str --> API Key to use for that endpoint
        @param data: dictionary with variable name (key) and value (value)

        // Prepare your HTTP POST request data
        String httpRequestData = 
                "api_key=" + apiKeyValue + 
                "&pressure=" + String(random(300)) +
                "&temperature=" + String(random(300)) + 
                "&lightsensor=" + String(random(300)) + 
                "&UVsensor=" + String(random(300))+ 
                "&GeigerCounter=" + String(random(300))+ 
                "&value6=" + String(random(300))+ 
                "&value7=" + String(random(300))+ 
                "&value8=" + String(random(300))+ "";

        http://www.habheiliggraf.be/

    """
    postdata = {
        'pressure': data['pressure'],
        'temperature': data.get('temperature', None),
        'lightsensor': data.get('lightsensor', None),
        'UVsensor': data.get('uvsensor', None),
        'GeigerCounter': data.get('geigercounter', None),
        'value6': data.get('battery', None),
        'value7': data.get('percentage', None),
        'value8': data.get('status', 'undefined') 
    }    
    for endpoint in endpoints:
        postdata['apikey'] = endpoint['apikey']
        r = requests.post(url=endpoint['url'], data = postdata)
        print(f"Post response: {r.text}")




if __name__ == "__main__":
    endpoints = [ 
        # http://highaltitudeballoon.be/balloonlk/post-data.php
        # https://www.habheiliggraf.be/balloonlk/post-data.php
        { 'url': "https://www.habheiliggraf.be/post-data.php", 'apikey':"tPmAT5Ab3j7F9"},
        { 'url': "http://127.0.0.1:8080", 'apikey':"23456"},                
    ]

    values = {
        'pressure': 100,
        'temperature': "25",
        'lightsensor': 100,
        'uvsensor': 123,
        'geigercounter': 0,
        'battery': 80,
        'percentage': 90,
        'status': "online"
    }

    post_results(endpoints, values)