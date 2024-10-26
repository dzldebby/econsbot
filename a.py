import requests

input_json = {
    "model": "gpt-4o-prd-gcc2-lb",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "hello"}
    ],
}

try:
    print("Sending request...")
    response = requests.post(
        url="https://litellm.govtext.gov.sg/chat/completions",
        json=input_json,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer sk-9yferRaarrs_xmdJKA3uMg",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
        })
    
    print(f"Status code: {response.status_code}")
    
    # Print the response
    if response.status_code == 200:
        print("Response content:", response.json()['choices'][0]['message']['content'])
    else:
        print("Error response:", response.text)

except Exception as e:
    print(f"An error occurred: {str(e)}")
