import asyncio

from browseruse import run_task_in_cloud
from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.services.llm_service import FunctionCallParams


def get_tools_functions(append_message=None):
    async def start_browser_task(params: FunctionCallParams, task: str):
        """Execute a task in the browser.

        Args:
            task: Detailed description of the browser task to execute.
        """
        asyncio.create_task(run_task_in_cloud(task, on_log=append_message))
        await params.result_callback("Browser task started.")

    return [start_browser_task]


def get_tools_schema() -> ToolsSchema:
    return ToolsSchema(standard_tools=get_tools_functions())
