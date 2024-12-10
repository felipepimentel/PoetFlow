import os
import sys

import anyio
import dagger


async def build_and_test(client: dagger.Client) -> bool:
    """Build and test the package inside a container."""
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


async def publish_package(client: dagger.Client) -> bool:
    """Publish the package to PyPI using an API token."""
    pypi_token = os.getenv("PYPI_TOKEN")
    if not pypi_token:
        print("No PyPI token provided, skipping publish...")
        return True

    python = (
        client.container()
        .from_("python:3.12-slim")
        .with_exec(["pip", "install", "poetry"])
        .with_mounted_directory("/app", client.host().directory("."))
        .with_workdir("/app")
        .with_exec(["poetry", "install"])
    )

    # Publish to PyPI using the token
    publish_result = (
        await python.with_env_variable("POETRY_PYPI_TOKEN_PYPI", pypi_token)
        .with_exec(["poetry", "publish", "--no-interaction"])
        .exit_code()
    )

    return publish_result == 0


async def main() -> int:
    async with dagger.Connection() as client:
        # Run build and tests
        if not await build_and_test(client):
            return 1

        # If tests pass, attempt to publish
        if not await publish_package(client):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(anyio.run(main))
