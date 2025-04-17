# AppDog - Agent Instructions

This document outlines the architecture, conventions, and rules for the `appdog` package, which provides automatic OpenAPI client generation and MCP server support.

## Development Environment

The project uses the following tools for development:

- **uv**: Package management and virtual environment
- **mypy**: Static type checking
- **ruff**: Linting and code formatting
- **pytest**: Testing framework

## Repository Structure

```
src/
└── appdog/                  # AppDog package
    ├── __init__.py        # Package initialization
    ├── __main__.py        # CLI entrypoint
    ├── _internal/         # Internal implementation (not exposed)
    │   ├── templates/     # Jinja templates for code generation
    │   ├── case.py        # Case conversion utilities
    │   ├── cli.py         # CLI implementation
    │   ├── clients.py     # Base client classes
    │   ├── errors.py      # Custom exceptions
    │   ├── generator.py   # Client generation
    │   ├── logging.py     # Logging configuration
    │   ├── managers.py    # Manager singletons
    │   ├── mcp.py         # MCP server integration
    │   ├── project.py     # Project configuration management
    │   ├── registry.py    # Registry management for installed API appdog
    │   ├── settings.py    # Settings models and utilities
    │   ├── specs.py       # OpenAPI spec parsing
    │   ├── store.py       # API client store implementation
    │   └── utils.py       # Utility functions
    │
    ├── .../             # Installed API appdog
    │   ├── __init__.py    # Package initialization
    │   ├── client.py      # Client implementation
    │   └── models.py      # Pydantic models
    └── (registry.json)    # Auto-generated registry of installed API appdog
```

## Project Structure

```
project/
├── apps.yaml                 # Installed API appdog settings
├── apps.lock                 # Lock file with app specs and hashes
└── ...                       # Project files
```

## Key Concepts

### Core Managers (managers.py)

The package provides two manager singletons:
- `registry_manager`: Handles registration and retrieval of API clients
- `project_manager`: Manages project configuration and client generation

### Registry Management (registry.py)

The Registry manages installed API clients, including:
- Folder locations for generated code
- OpenAPI spec metadata
- Version information through spec hashes
- Client registration and lookup

### Project Configuration (project.py)

The Project class handles:
- Loading and managing apps.yaml - user configuration for API clients
- Generating and updating client code
- Maintaining apps.lock - version locking for reproducibility

### Logging Configuration (cli.py)

The package configures logging using Rich:
- Different log levels based on verbosity (--verbose/--debug flags)
- Pretty formatting with Rich handlers
- Custom log levels for appdog vs. dependencies

### Client Configuration Files

The system maintains two key files:

1. **apps.yaml**: User-configurable registry of API clients
   - Contains client names, URLs, base URLs, and other settings
   - Does NOT store credentials (these are managed separately)
   - Can be manually edited or managed via CLI

2. **apps.lock**: System-managed lock file
   - Contains complete OpenAPI specs for each client
   - Includes cryptographic hashes for change detection
   - Used to determine when regeneration is needed
   - Should not be manually edited

### Settings Management (settings.py)

Contains setting models:
- `AppSettings`: Configuration for individual API clients
- `ClientSettings`: Configuration for API client instances with credentials and support for environment variable loading and validation using Pydantic settings

### OpenAPI Specs Processing (specs.py)

Handles OpenAPI specification processing:
- Downloading and parsing OpenAPI specs
- Minimizing and normalizing specs
- Calculating content hashes for change detection
- Extracting schemas and endpoints

## Command Line Interface

The system provides the following CLI commands:

- `appdog init`: Initialize a new apps.yaml file
- `appdog add <name> --uri <uri> --base-url <base_url>`: Add a new API client
- `appdog remove <name>`: Remove an API client
- `appdog list`: List all registered API clients
- `appdog show <name>`: Show details for a specific client
- `appdog lock`: Lock the current state of the apps.yaml file
- `appdog sync`: Sync the apps.yaml file with the apps.lock file

## Client Store (store.py)

The `Store` class provides:
- Generic key-value storage mechanism for application data
- JSON and YAML format support
- File-based persistence
- Type validation via Pydantic models

## Credential Management

API credentials are managed separate from the client registry:

1. **Environment Variables**:
   - Format: `APPDOG_<CLIENT_NAME>_TOKEN`, `APPDOG_<CLIENT_NAME>_API_KEY`, etc.
   - Highest priority source of credentials
   - Recommended for production use

2. **Direct Initialization**:
   - Credentials can be passed directly to client constructors
   - Useful for development and testing

3. **Settings Objects**:
   - Pydantic settings models with validation
   - Support for hierarchical configuration

## Client Generation Process

1. Client Discovery:
   - Parse apps.yaml to identify configured clients
   - Download and validate OpenAPI specs
   - Compare with cached specs in apps.lock

2. Code Generation:
   - Parse OpenAPI spec using datamodel-code-generator
   - Generate models with proper typing
   - Generate client methods with proper parameter handling
   - Ensure proper error handling and response parsing
   - Format generated code according to project standards

3. Registration:
   - Register generated clients in registry.json
   - Make clients available through the store

## Client Architecture

The base client classes provide:

1. Credentials and settings management via Pydantic settings
2. HTTP methods (GET, POST, PUT, PATCH, DELETE) using httpx
3. Error handling and response parsing
4. Support for Pydantic models as parameters and return types
5. Context manager support for resource cleanup
6. Asynchronous and synchronous client variants

## MCP Server Integration

The system can also generate MCP servers from OpenAPI specs:

1. Endpoint extraction from OpenAPI specs
2. Route generation for MCP servers
3. Request validation using generated model classes
4. Response serialization with proper content types

## Rules and Conventions

1. All internal implementation should be in `_internal/`
2. Public API is exposed through `__init__.py`
3. Generated code should be type-safe and follow project's linting rules
4. All configuration should be in `apps.yaml` or environment variables
5. Credentials should never be stored in registry files
6. Tests should be comprehensive and avoid network calls
7. Error messages should be clear and actionable
8. Code should follow the project's coding style (enforced by ruff)
