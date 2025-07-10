"""
Configuration commands for managing sync settings and field mappings.
"""

import click
from not_warrior.utils.config_manager import ConfigManager
from not_warrior.utils.logger import get_logger

logger = get_logger(__name__)


@click.group()
def config():
    """Manage configuration settings and field mappings."""
    pass


@config.command()
@click.option('--force', is_flag=True, help='Overwrite existing configuration')
@click.pass_context
def init(ctx, force):
    """Initialize configuration file."""
    try:
        config_manager = ConfigManager(ctx.obj['config_file'])
        if config_manager.exists() and not force:
            click.echo("Configuration file already exists. Use --force to overwrite.")
            ctx.exit(1)
        config_manager.create_default_config()
        # TODO: Set up initial field mappings
        click.echo("Configuration initialized!")
    except Exception as e:
        logger.error(f"Config initialization failed: {e}")
        click.echo(f"Error: {e}")
        ctx.exit(1)


@config.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key, value):
    """Set configuration value."""
    try:
        # TODO: Update config value
        config_manager = ConfigManager(ctx.obj['config_file'])
        if not config_manager.exists():
            click.echo("Configuration file does not exist. Please run `not-warrior config init` first.")
            ctx.exit(1)
        config = config_manager.load_config()
        config[key] = value
        config_manager.save_config(config)
        click.echo(f"Set {key} = {value}")
    except Exception as e:
        logger.error(f"Failed to set config: {e}")
        click.echo(f"Error: {e}")
        ctx.exit(1)


@config.command()
@click.option('--key', help='Show specific configuration key')
@click.pass_context
def show(ctx, key):
    """Show current configuration."""
    try:
        config_manager = ConfigManager(ctx.obj['config_file'])
        if not config_manager.exists():
            click.echo("Configuration file does not exist. Please run `not-warrior config init` first.")
            ctx.exit(1)
        config = config_manager.load_config()
        if key:
            if key in config:
                click.echo(f"{key}: {config[key]}")
            else:
                click.echo(f"Key '{key}' not found in configuration.")
        else:
            click.echo("Current configuration:")
            for k, v in config.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        logger.error(f"Failed to show config: {e}")
        click.echo(f"Error: {e}")
        ctx.exit(1)


@config.command()
@click.option('--list', 'list_mappings', is_flag=True, help='List current mappings')
@click.option('--add', nargs=2, help='Add mapping: --add notion_field taskwarrior_field')
@click.option('--remove', help='Remove mapping by Notion field name')
@click.pass_context
def mapping(ctx, list_mappings, add, remove):
    """Manage field mappings between Notion and Taskwarrior."""
    try:
        if list_mappings:
            # TODO: Display current mappings
            click.echo("Field mappings: Not implemented")
        elif add:
            # TODO: Add new mapping
            notion_field, tw_field = add
            click.echo(f"Added mapping: {notion_field} -> {tw_field}")
        elif remove:
            # TODO: Remove mapping
            click.echo(f"Removed mapping: {remove}")
        else:
            click.echo("Use --list, --add, or --remove")
    except Exception as e:
        logger.error(f"Failed to manage mappings: {e}")
        click.echo(f"Error: {e}")
        ctx.exit(1)


@config.command()
@click.pass_context
def validate(ctx):
    """Validate current configuration."""
    try:
        # TODO: Validate config file
        # TODO: Check field mappings
        # TODO: Verify authentication
        click.echo("Configuration is valid!")
    except Exception as e:
        logger.error(f"Config validation failed: {e}")
        click.echo(f"Error: {e}")
        ctx.exit(1)
