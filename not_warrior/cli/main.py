"""
Main CLI entry point with Click command groups.
"""

import click
from not_warrior.cli.auth import auth
from not_warrior.cli.sync import sync
from not_warrior.cli.config import config
from not_warrior.utils.logger import setup_logger


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config-file', '-c', help='Path to configuration file')
@click.pass_context
def cli(ctx, verbose, config_file):
    """not-warrior: Notion-Taskwarrior Synchronization Service"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config_file'] = config_file
    
    setup_logger(verbose)


# Add command groups
cli.add_command(auth)
cli.add_command(sync)
cli.add_command(config)


if __name__ == '__main__':
    cli()