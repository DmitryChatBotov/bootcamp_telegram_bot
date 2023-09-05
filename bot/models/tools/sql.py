from typing import Any, Optional, Callable, Awaitable

from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import BaseTool

from models.config import TABLE_INFO, DIALECT


class SQLTool(BaseTool):
    name: str
    description: str
    func: Optional[Callable[..., str]]
    """The function to run when the tool is called."""
    coroutine: Optional[Callable[..., Awaitable[str]]] = None
    """The asynchronous version of the function."""

    def __init__(
            self, name: str, func: Optional[Callable], description: str, **kwargs: Any
    ) -> None:
        """Initialize tool."""
        super(SQLTool, self).__init__(
            name=name, func=func, description=description, **kwargs
        )

    def _run(
            self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> str:
        """Use the tool."""
        return self.func(
            input=query, table_info=TABLE_INFO, dialect=DIALECT, query=query
        )

    async def _arun(
            self, query: str, run_manager: AsyncCallbackManagerForToolRun | None = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("sql_tool does not support async")
