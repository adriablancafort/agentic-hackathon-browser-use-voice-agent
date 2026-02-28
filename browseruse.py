import os

from browser_use import Agent, Browser, ChatBrowserUse, sandbox
from dotenv import load_dotenv


load_dotenv()


def get_sandbox_kwargs():
	cloud_profile_id = os.getenv("BROWSER_USE_PROFILE_ID")
	if not cloud_profile_id:
		raise ValueError("BROWSER_USE_PROFILE_ID not set")

	return {
		"cloud_proxy_country_code": "es",
		"cloud_profile_id": cloud_profile_id,
	}


async def run_task_in_cloud(task: str) -> None:
	@sandbox(**get_sandbox_kwargs())
	async def run_task(browser: Browser) -> None:
		llm = ChatBrowserUse()
		agent = Agent(task=task, browser=browser, llm=llm)
		await agent.run()

	await run_task()
