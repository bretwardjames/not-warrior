# not-warrior

![WIP](https://img.shields.io/badge/status-WIP-yellow.svg)

A synchronization service that connects Notion assigned tasks/items with Taskwarrior, keeping them in sync between the two systems. The application bridges the gap between Notion's collaborative task management and Taskwarrior's powerful command-line task management.

## Overview

This tool enables bidirectional synchronization between:
- **Notion**: Web-based collaborative task management with rich formatting and team features
- **Taskwarrior**: Command-line task management with powerful filtering, reporting, and workflow automation

## Architecture

The application consists of several key components:

- **Notion API Integration**: Handle authentication and CRUD operations for Notion tasks
- **Taskwarrior Integration**: Interface with the local Taskwarrior installation via CLI or direct data access
- **Sync Engine**: Core logic to detect changes and maintain bidirectional synchronization
- **Configuration System**: Manage API keys, sync preferences, and field mappings
- **Conflict Resolution**: Handle cases where tasks are modified in both systems

## Key Features (Planned)

- Bidirectional sync between Notion databases and Taskwarrior
- Mapping of Notion properties to Taskwarrior attributes (priority, tags, due dates, etc.)
- Conflict resolution for tasks modified in both systems
- Configurable sync intervals and field mappings
- Support for task completion, deletion, and status changes
- Authentication management for Notion API access

## Development Status

🚧 **Work in Progress** - Project structure established with Python Click CLI framework. Core functionality implementation in progress.

## Technology Stack

**Python** with Click CLI framework has been chosen as the primary technology stack:

- **Click**: Command-line interface framework
- **Requests**: HTTP client for Notion API
- **Pydantic**: Data validation and models
- **PyYAML**: Configuration file handling
- **python-dateutil**: Date/time processing
- **python-dotenv**: Environment variable management

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/not-warrior.git
cd not-warrior

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

The CLI provides several command groups:

### Authentication
```bash
# Setup Notion API authentication
not-warrior auth setup

# Validate current authentication
not-warrior auth validate

# Refresh authentication tokens
not-warrior auth refresh
```

### Configuration
```bash
# Initialize configuration file
not-warrior config init

# Set configuration values
not-warrior config set key value

# Show current configuration
not-warrior config show

# Manage field mappings
not-warrior config mapping
```

### Synchronization
```bash
# Perform manual synchronization
not-warrior sync run

# Show sync status and statistics
not-warrior sync status

# Install Taskwarrior hook for auto-sync
not-warrior sync install-hook

# Remove Taskwarrior hook
not-warrior sync remove-hook
```

## Development

```bash
# Run tests
make test

# Run linter
make lint

# Install development dependencies
make install

# Build package
make build
```

## Contributing

This project is in early development. The basic structure is established, and implementation of core functionality is in progress.