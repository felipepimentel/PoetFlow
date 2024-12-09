# PoetFlow: Monorepo Management Tool for Poetry-based Python Projects

## Overview

**PoetFlow** is a CLI tool (with potential plugin architecture) designed to streamline the management of Python monorepos that rely on Poetry for dependency management. Its primary goal is to provide a centralized, automated approach to discover, build, test, version, and publish multiple packages contained within a single repository. PoetFlow aims to simplify continuous integration (CI), continuous delivery (CD), and facilitate seamless package deployments to PyPI and other Python repositories.

## Key Objectives

1. **Centralized Monorepo Management**  
   - Automatically discover multiple packages in a monorepo structure.  
   - Standardize and simplify the entire process of building, testing, and publishing multiple packages.

2. **Automated CI/CD Integration**  
   - Offer simple, high-level commands to orchestrate builds, tests, and publication from a single interface.  
   - Integrate smoothly with existing CI/CD pipelines, reducing complexity and enhancing reliability.

3. **Intelligent Versioning and Changelogs**  
   - Support semantic versioning and automated version bumps based on conventional commit messages.  
   - Generate changelogs automatically, reflecting consolidated changes across all packages.

4. **Quality, Security, and Compliance**  
   - Run tests, linting, and other quality assurance checks before publishing.  
   - Manage credentials securely and optionally sign packages before publishing.

5. **Extensibility and Developer Experience**  
   - Allow customizable hooks (pre/post build/publish) and a plugin architecture for third-party extensions.  
   - Provide an intuitive CLI experience and thorough documentation for a frictionless developer journey.

## Scope

### Monorepo Structure

**Assumed Directory Layout**:  
```
my-monorepo/
    pyproject.toml            # Optional root-level configuration
    packages/
        packageA/
            pyproject.toml
            src/
        packageB/
            pyproject.toml
            src/
        ...
```

Each subpackage includes its own `pyproject.toml`. The root directory may contain a `pyproject.toml` for shared settings.

### Core Features and Commands

1. **Package Discovery**:  
   `poetflow discover`  
   - Scans the `packages/` directory to identify all subpackages.  
   - Lists packages along with their names, versions, and statuses.

2. **Building Packages**:  
   `poetflow build [--all | --package <name>]`  
   - Executes `poetry build` for all or specific packages.  
   - Resolves inter-package dependencies and ensures correct build order.

3. **Publishing Packages**:  
   `poetflow publish [--all | --package <name>] [--repository <repo>]`  
   - Publishes all or selected packages to PyPI, TestPyPI, or custom repositories.  
   - Automatically runs `poetry build` if needed before publication.  
   - Supports signing artifacts and secure token management.

4. **Testing and Quality Checks**:  
   `poetflow test [--all | --package <name>]`  
   - Runs tests (unit, integration), linters, type checkers, or other QA tools.  
   - Integrates with pre-defined hooks to ensure quality before build and publish steps.

5. **Versioning Management**:  
   `poetflow version [bump | set <version>] [--all | --package <name>]`  
   - Updates package versions uniformly or individually.  
   - Integrates with semantic versioning and can automatically determine the next version based on commit history.  
   - Synchronizes versions across multiple packages if desired.

6. **Changelog Generation**:  
   `poetflow changelog [--all | --package <name>]`  
   - Creates or updates changelogs by scanning commit messages.  
   - Supports conventional commits and flexible output formats (Markdown, JSON, etc.).

7. **Hooks and Customization**:  
   - Supports pre- and post-build/publish hooks.  
   - Allows custom scripts to run at various stages, e.g., generating documentation, minifying assets, or notifying external services.

### CI/CD Integration

- **Out-of-the-Box CI Examples**:  
  Provide sample configurations for GitHub Actions, GitLab CI, Jenkins, etc.
  
  Example GitHub Actions workflow:
  ```yaml
  name: CI
  on: [push, pull_request, release]

  jobs:
    build_and_test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - name: Install Dependencies
          run: poetry install
        - name: Test All Packages
          run: poetflow test --all
        - name: Build All Packages
          run: poetflow build --all

    publish:
      runs-on: ubuntu-latest
      if: github.ref == 'refs/tags/v*'
      steps:
        - uses: actions/checkout@v2
        - name: Install Dependencies
          run: poetry install
        - name: Publish All Packages
          run: poetflow publish --all --repository pypi
  ```

- **Parallelization and Caching**:  
  Supports the use of Poetry's caching in CI pipelines.  
  Potential future enhancements include parallel builds and tests.

### Security and Credentials Management

- Securely handle tokens and credentials via environment variables, GitHub Actions secrets, or external secret managers (Vault, AWS Secrets Manager).  
- Optionally sign wheels or source distributions before publishing to ensure integrity and authenticity.

### Logging and Observability

- Structured and verbose logging options to aid in troubleshooting.  
- Configurable log levels (debug, info, warning, error).  
- Potential integration with metrics systems to measure build/test durations and publication frequency.

### Extensibility

- **Plugin Architecture**:  
  Allow developers to extend PoetFlow with additional commands and integrations (e.g., documentation generation, metrics collection).  
- **Hooks and Configurable Pipelines**:  
  Users can define custom scripts to run at various stages, providing ultimate flexibility for unique workflows.

### Developer Experience and Documentation

- Comprehensive `--help` output and inline usage examples for all commands.  
- Tutorials and how-to guides on setting up CI/CD pipelines, enabling semantic versioning, and customizing hooks.  
- Clear roadmap and contribution guidelines for the community.

### Roadmap

1. **MVP Release**:  
   - Basic package discovery, build, publish, and test commands.  
   - Minimal documentation and CI templates.

2. **Intermediate Features**:  
   - Semantic versioning integration.  
   - Automatic changelog generation.  
   - Hooks for pre/post actions.  
   - Extended CI/CD templates.

3. **Advanced Enhancements**:  
   - Package signing and enhanced security options.  
   - Support for multiple repositories and selective deployments.  
   - Performance optimizations, parallel builds, and caching strategies.

4. **Future Considerations**:  
   - Observability features (metrics, dashboards).  
   - Deeper integrations with external tooling.  
   - Interactive CLI modes for configuration assistance.