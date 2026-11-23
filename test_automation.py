import asyncio
from Backend.Automation import TranslateAndExecute

async def test():
    commands = [
        "open lion circuits"
    ]

    async for result in TranslateAndExecute(commands):
        print("RESULT:", result)

asyncio.run(test())