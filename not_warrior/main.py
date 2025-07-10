#!/usr/bin/env python3
"""
Entry point for the not-warrior CLI application.
"""

import sys
from not_warrior.cli.main import cli

def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()