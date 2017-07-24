import click
import os.path
import glob
import sys
import inspect

from locke import *

# Locke pattern plugins are expected to be in this directory.
PATTERN_PLUGIN_DIR = os.path.abspath('patterns')
PATTERN_PLUGIN_GLOB = os.path.join(PATTERN_PLUGIN_DIR, '*.py')

# Locke pattern plugins are expected to modify this array.
LOCKE_PATTERNS = []

# Locke transformer plugins
TRANSFORM_PLUGIN_DIR = os.path.abspath('transformers')
TRANSFORM_PLUGIN_GLOB = os.path.join(TRANSFORM_PLUGIN_DIR, '*.py')
LOCKE_TRANSFORMERS = []


def load_all_patterns():
    for plugin in glob.glob(PATTERN_PLUGIN_GLOB):
        exec(open(plugin).read())


def load_all_transformers():
    for plugin in glob.glob(TRANSFORM_PLUGIN_GLOB):
            exec(open(plugin).read(), globals())
    for clss in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if "Transform" in clss[0]:
            LOCKE_TRANSFORMERS.append(clss)


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
@click.option('-l', '--level', default=2, help="Select transformers with"
        "level 1, 2, or 3 and below")
@click.option('-i', '--inclevel', type=int, help="Select transformers with"
        "level 1, 2, or 3 and above")
@click.option('-k', '--keep', default=20, help="How many transforms to save"
        "after stage 1")
@click.option('-s', '--save', default=10, help="How many transforms to save"
        "after stage 2")
@click.option('-z', '--zip', is_flag=True, help="Mark this file"
        "as a zip file. Use -p to enter zip's password")
@click.option('--password', nargs=1, help="Only works if -z is "
        "set. Allows input of password for zip file")
@click.option('-d', '--display', is_flag=True, help="Display all available "
        "transformers")
@click.option('-p', '--profiling', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.pass_context
def crack(ctx, level, inclevel, keep, save, zip, password, display,
        profiling, filename, verbose):
    """
    Use patterns of interest to crack the supplied files.
    """
    load_all_transformers()

    if display:
        for trans in LOCKE_TRANSFORMERS:
            click.echo(trans[0])
    elif zip:
        data = read_zip(filename, password, verbose)
    else:
        data = read_file(filename, verbose)

    print(data)


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
    load_all_transformers()
    for trans in LOCKE_TRANSFORMERS:
        click.echo(trans[0])


if __name__ == '__main__':
    cli(obj={})
