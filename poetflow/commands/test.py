"""Copyright (C) 2024 Felipe Pimentel <fpimentel88@gmail.com>

This module provides the test command for PoetFlow.
"""

from typing import Set

from poetflow.commands.base import MonorepoCommand


class TestCommand(MonorepoCommand):
    """Runs tests for packages in the monorepo"""

    name = "monorepo-test"
    description = "Run tests for packages in the monorepo"

    def configure(self) -> None:
        self.add_option("--all", description="Test all packages")
        self.add_option("--package", multiple=True, description="Test specific package(s)")

    def handle(self) -> int:
        packages = self._get_target_packages()

        results = await self.executor.run_command(
            ["poetry", "run", "pytest"], packages=list(packages)
        )

        success = all(r.success for r in results)

        for result in results:
            if not result.success:
                self.line_error(f"Tests failed for {result.package}:")
                self.line_error(result.error)

        return 0 if success else 1

    def _get_target_packages(self) -> Set[str]:
        if self.option("all"):
            return set(self.manager.get_all_packages())

        if packages := self.option("package"):
            return set(packages)

        return self.get_affected_packages()
