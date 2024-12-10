import os
import sys

import anyio
import dagger


async def build_and_test(client: dagger.Client) -> bool:
    """
    Build and test the package inside a container.

    Args:
        client (dagger.Client): The Dagger client instance.

    Returns:
        bool: True if tests pass, False otherwise.
    """
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
    if result != 0:
        print("Tests failed.")
    return result == 0


async def publish_package(client: dagger.Client) -> bool:
    """
    Build and publish the package to PyPI using an API token.

    Args:
        client (dagger.Client): The Dagger client instance.

    Returns:
        bool: True if the package is published successfully, False otherwise.
    """
    pypi_token = os.getenv("PYPI_TOKEN")
    if not pypi_token:
        print("No PyPI token provided, skipping publish...")
        return True

    # Define the directory to store build artifacts
    python = (
        client.container()
        .from_("python:3.12-slim")
        .with_exec(["pip", "install", "poetry"])
        .with_mounted_directory("/app", client.host().directory("."))
        .with_workdir("/app")
        .with_exec(["poetry", "install"])
    )

    # Build the package
    build_result = await python.with_exec(["poetry", "build"]).exit_code()
    if build_result != 0:
        print("Failed to build the package.")
        return False

    print("Package built successfully.")

    # Publish to PyPI using the token
    publish_result = (
        await python.with_env_variable("POETRY_PYPI_TOKEN_PYPI", pypi_token)
        .with_exec(["poetry", "publish", "--no-interaction"])
        .exit_code()
    )

    if publish_result != 0:
        print("Failed to publish the package.")
        return False

    print("Package published successfully.")
    return True


async def main() -> int:
    """
    Main function to orchestrate the pipeline.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    async with dagger.Connection() as client:
        # Run build and tests
        print("Starting build and test process...")
        if not await build_and_test(client):
            print("Build or tests failed. Exiting.")
            return 1

        # If tests pass, attempt to publish
        print("Build and tests passed. Starting publish process...")
        if not await publish_package(client):
            print("Publish process failed. Exiting.")
            return 1

    print("Pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(anyio.run(main))
