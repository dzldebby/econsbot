from langchain_openai import ChatOpenAI  # Make sure this exact import is used
from langchain.schema import HumanMessage, SystemMessage

chat = ChatOpenAI(
    api_key="sk-9yferRaarrs_xmdJKA3uMg",
    openai_api_base="https://litellm.govtext.gov.sg/",
    model = "gpt-4o-prd-gcc2-lb",
    temperature=0.1,
    default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"},
)

messages = [
    SystemMessage(
        content="You are a helpful assistant"
    ),
    HumanMessage(
        content="hello"
    ),
]
response = chat.invoke(messages)  # Make sure to use .invoke() not chat()
print(response.content)
