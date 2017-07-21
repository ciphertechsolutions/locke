import click
import os.path
import glob
from locke import *


# Locke pattern plugins are expected to be in this directory.
PATTERN_PLUGIN_DIR = os.path.abspath('patterns')

PATTERN_PLUGIN_GLOB = os.path.join(PATTERN_PLUGIN_DIR, '*.py')

# Locke pattern plugins are expected to modify this array.
LOCKE_PATTERNS = []


def load_all_patterns():
    print(PATTERN_PLUGIN_GLOB)
    for plugin in glob.glob(PATTERN_PLUGIN_GLOB):
        print(plugin)
        exec(open(plugin).read())


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
    load_all_patterns()
    ctx.obj['verbose'] = verbose
    pass


@cli.command()
@click.option('--csv', default=False, help='output results as CSV')
@click.pass_context
def search(ctx, csv):
    """
    Search for patterns of interest in the supplied files.
    """
    click.echo('Search')
    click.echo(LOCKE_PATTERNS)


@cli.command()
@click.option('-l', '--level', default=2)
@click.option('-i', '--inclevel', type=int)
@click.option('-k', '--keep', default=20)
@click.option('-s', '--save', default=10)
@click.option('-t', '--transform')
@click.option('-p', '--profiling', is_flag=True)
@click.pass_context
def crack(ctx, level, inclevel, keep, save, transform, profiling):
    """
    Use patterns of interest to crack the supplied files.
    """
    click.echo('Crack')


@cli.command()
@click.pass_context
def patterns(ctx):
    """
    List all patterns known by Locke.
    """
    click.echo('Patterns')


@cli.command()
@click.pass_context
def transforms(ctx):
    """
    List all transformations known by Locke.
    """
    click.echo('Transforms')


if __name__ == '__main__':
    cli(obj={})
