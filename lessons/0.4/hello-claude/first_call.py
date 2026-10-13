import anthropic
from dotenv import load_dotenv

load_dotenv()  # copies ANTHROPIC_API_KEY from .env into the environment

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY by itself

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    thinking={"type": "disabled"},
    messages=[
        {"role": "user", "content": "In one sentence, what is an API key?"}
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print("stop_reason:", response.stop_reason)
print("tokens in:", response.usage.input_tokens, "out:", response.usage.output_tokens)
print("request id:", response._request_id)
