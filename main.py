import asyncio

from browser_use import Agent, ChatBrowserUse
from dotenv import load_dotenv


async def main() -> None:
    load_dotenv()
    llm = ChatBrowserUse()
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
