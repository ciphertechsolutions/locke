import click
import os.path
import glob
import sys
import inspect
import csv as csvlib

from locke import pattern, locke, transformer
from locke.pattern import *
from locke.transformer import *


# Locke pattern plugins are expected to be in this directory.
PATTERN_PLUGIN_DIR = os.path.abspath('patterns')
PATTERN_PLUGIN_GLOB = os.path.join(PATTERN_PLUGIN_DIR, '*.py')

# Locke pattern plugins are expected to modify this array.
LOCKE_PATTERNS = []

# Locke transformer plugins
TRANSFORM_PLUGIN_DIR = os.path.abspath('transformers')
TRANSFORM_PLUGIN_GLOB = os.path.join(TRANSFORM_PLUGIN_DIR, '*.py')
# Nest array. One for each level
LOCKE_TRANSFORMERS = [[], [], []]


def load_all_patterns():
    for plugin in glob.glob(PATTERN_PLUGIN_GLOB):
        exec(open(plugin).read())


def load_all_transformers():
    for plugin in glob.glob(TRANSFORM_PLUGIN_GLOB):
            exec(open(plugin).read(), globals())
    for clss in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if "Transform" in clss[0]:
            if "locke" in clss[1].__module__:
                continue
            if clss[1].class_level() == 1:
                LOCKE_TRANSFORMERS[0].append(clss)
            elif clss[1].class_level() == 2:
                LOCKE_TRANSFORMERS[1].append(clss)
            elif clss[1].class_level() == 3:
                LOCKE_TRANSFORMERS[2].append(clss)

@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
    load_all_patterns()
    ctx.obj['verbose'] = verbose
    pass


@cli.command()
@click.option('--csv', default=None, help='output results as CSV')
@click.argument('files', type=click.File('rb'), nargs=-1)
@click.pass_context
def search(ctx, csv, files):
    """
    Search for patterns of interest in the supplied files.
    """
    if csv:
        print('Writing CSV results to %s' % csv)
        csvfile = open(csv, 'w')
        csv_writer = csvlib.writer(csvfile)
        csv_writer.writerow(['Filename', 'Index', 'Pattern name', 'Match',
                             'Length'])

    l = locke.Locke(LOCKE_PATTERNS)
    for f in files:
        print("=" * 79)
        print("File: %s\n" % f.name)
        for pat, matches in l.scan(f.read()):
            for index, match in matches:
                mstr = utils.prettyhex2(match)
                if len(mstr) > 50:
                    mstr = mstr[:24] + '...' + mstr[-23:]

                print('at %08X: %s - %s' % (index, pat.name, mstr))

                if csv:
                    csv_writer.writerow([f.name, '0x%08X' % index, pat.name,
                                         mstr, len(match)])
        print()

    if csv:
        csvfile.close()


@cli.command()
@click.option('-l', '--level', type=int, default=None,
        help="Select transformers with level 1, 2, or 3 and below")
@click.option('-o', '--only', type=int, default=None,
        help="Only use transformers on that "
        "specific level")
@click.option('-n', '--name', nargs=1, default=None,
        help="A list of transformers' class name to use in quotes and "
        "is commas separated")
@click.option('-k', '--keep', default=20, help="How many transforms to save"
              "after stage 1")
@click.option('-s', '--save', default=10, help="How many transforms to save"
              "after stage 2")
@click.option('-z', '--zip', is_flag=True, help="Mark this file"
              "as a zip file. Use --password to enter zip's password")
@click.option('--password', nargs=1, default=None, help="Only works if -z is "
        "set. Allows input of password for zip file")
@click.option('-p', '--profiling', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.pass_context
def crack(ctx, level, only, name, keep, save, zip, password,
        profiling, filename, verbose):
    """
    Use patterns of interest to crack the supplied files.
    """
    load_all_transformers()

    if not zip and password is not None:
        raise ValueError("Password field is set without zip enable")

    lock = locke.Locke(LOCKE_PATTERNS)
    trans = Transfomer(filename, password,
            LOCKE_TRANSFORMERS, lock, zip,
            level, only, name, keep, save,
            verbose)


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
    for transList in LOCKE_TRANSFORMERS:
        for trans in transList:
            print('Class: %s | Level: %i' % (trans[0], trans[1].class_level()))
            print(trans[1].__doc__)


if __name__ == '__main__':
    cli(obj={})
