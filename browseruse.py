import asyncio
import builtins
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


def schedule_callback(callback, message):
	try:
		loop = asyncio.get_running_loop()
		loop.create_task(callback(message))
	except:
		pass


async def run_task_in_cloud(task, on_log=None):
	@sandbox(**get_sandbox_kwargs())
	async def run_task(browser: Browser) -> None:
		llm = ChatBrowserUse()
		agent = Agent(task=task, browser=browser, llm=llm)
		await agent.run()

	original_print = builtins.print

	def intercept_print(*args, **kwargs):
		message = " ".join(str(a) for a in args).strip()
		if on_log and message:
			schedule_callback(on_log, message)
		original_print(*args, **kwargs)

	builtins.print = intercept_print
	await run_task()
	builtins.print = original_print
