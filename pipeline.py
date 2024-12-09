"""CI/CD pipeline using Dagger."""

import sys

import anyio
import dagger


async def test() -> bool:
    """Run tests in container."""
    async with dagger.Connection() as client:
        # Get python image
        python = (
            client.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "poetry"])
            .with_mounted_directory("/app", client.host().directory("."))
            .with_workdir("/app")
            .with_exec(["poetry", "install"])
        )

        # Run tests
        result = await python.with_exec(["poetry", "run", "check"]).exit_code()
        return result == 0


async def main() -> int:
    """Run pipeline."""
    success = await test()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(anyio.run(main))
