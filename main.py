import asyncio

from browseruse import run_task_in_cloud

task = "Go to https://glovoapp.com/ and tell me what are the top 10 pizza restaurants in Barcelona"


if __name__ == "__main__":
    asyncio.run(run_task_in_cloud(task))
