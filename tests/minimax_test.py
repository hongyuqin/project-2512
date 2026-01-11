import anthropic

client = anthropic.Anthropic(
    api_key="sk-cp-O9pxeWFOgMup86FTpmgukzxOmDdMsX6CqR_60OPkaHyc1scZ8aRHDOsRkxYNGW3HqKj4sx-_sQMxzfoJiKleFGvyI3DAC2OKfOLwbCKMslA4d5ENPVXgA28",
    base_url="https://api.minimaxi.com/anthropic",
)

message = client.messages.create(
    model="MiniMax-M2.1",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi, how are you?"
                }
            ]
        }
    ]
)

for block in message.content:
    if block.type == "thinking":
        print(f"Thinking:\n{block.thinking}\n")
    elif block.type == "text":
        print(f"Text:\n{block.text}\n")