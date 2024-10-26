from openai import OpenAI

try:
    client = OpenAI(
        api_key="sk-9yferRaarrs_xmdJKA3uMg",
        base_url="https://litellm.govtext.gov.sg/",
        default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"},
    )
    
    print("Client created successfully")  # Debug print
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "hello",
            }
        ],
        model="gpt-4o-prd-gcc2-lb",
    )
    
    print("Response received:")  # Debug print
    print(chat_completion.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {str(e)}")
