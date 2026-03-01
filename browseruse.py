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


async def run_task_in_cloud(task, append_message=None):
	@sandbox(**get_sandbox_kwargs())
	async def run_task(browser: Browser):
		llm = ChatBrowserUse()
		agent = Agent(task=task, browser=browser, llm=llm)
		await agent.run()

	def browserbase_update(message: str, run_llm: bool):
		if append_message:
			loop = asyncio.get_running_loop()
			loop.create_task(append_message(message, run_llm=run_llm))

	expect_final_result = False
	original_print = builtins.print

	def intercept_print(*args, **kwargs):
		nonlocal expect_final_result
		message = " ".join(str(a) for a in args).strip()
		if "🧠 Memory: " in message:
			cleaned = message.split("🧠 Memory: ", 1)[1]
			browserbase_update(cleaned, run_llm=True)
		elif expect_final_result:
			browserbase_update(message, run_llm=True)
			expect_final_result = False
		elif "Final Result:" in message:
			expect_final_result = True
		original_print(*args, **kwargs)

	builtins.print = intercept_print
	await run_task()
	builtins.print = original_print
