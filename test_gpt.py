import asyncio
from utils.gpt import ask_gpt

async def main():
    messages = [{"role": "user", "content": "How can I reset my password?"}]
    response = await ask_gpt(messages)
    print("BOT:", response)

asyncio.run(main())
