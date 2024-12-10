"""CI/CD pipeline using Dagger."""

import sys
from typing import Any

import anyio  # type: ignore
import dagger  # type: ignore


async def test() -> bool:
    """Run tests in container."""
    async with dagger.Connection() as client:  # type: ignore
        # Using Any type because dagger does not provide type hints
        python: Any = (
            client.container()  # type: ignore
            .from_("python:3.12-slim")  # type: ignore
            .with_exec(["pip", "install", "poetry"])  # type: ignore
            .with_mounted_directory("/app", client.host().directory("."))  # type: ignore
            .with_workdir("/app")  # type: ignore
            .with_exec(["poetry", "install"])  # type: ignore
        )
        result: int = await python.with_exec(["poetry", "run", "check"]).exit_code()  # type: ignore
        return result == 0


async def main() -> int:
    """Run pipeline."""
    success: bool = await test()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(anyio.run(main))  # type: ignore
