#!/usr/bin/python3.5

import click
import glob
import sys
import inspect
import csv as csvlib
from os import path

from locke import pattern, locke, transformer, utils
from locke.pattern import *
from locke.transformer import *


SCRIPT_DIR = path.dirname(path.abspath(__file__))

APM_PATH = path.join(SCRIPT_DIR, 'apm')

if APM_PATH not in sys.path:
    sys.path.append(APM_PATH)

import apm
import patterns

# Locke transformer plugins
TRANSFORM_PLUGIN_DIR = path.join(SCRIPT_DIR, 'transformers')
TRANSFORM_PLUGIN_GLOB = path.join(TRANSFORM_PLUGIN_DIR, '*.py')
# Nest array. One for each level
LOCKE_TRANSFORMERS = [[], [], []]


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
            elif clss[1].class_level() == -1:
                print("!! %s is disable" % clss[0])
            else:
                print("%s has an invalid class level (1 - 3 | -1 > disable)"
                      % clss[0])
    print("")


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
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
    client = apm.client.TCPClient()
    client.connect()

    if csv:
        click.echo('Writing CSV results to %s' % csv)
        csvfile = open(csv, 'w')
        csv_writer = csvlib.writer(csvfile)
        csv_writer.writerow(['Filename', 'Index', 'Pattern name', 'Match',
                             'Length'])

    for f in files:
        click.echo("=" * 79)
        click.echo("File: %s\n" % f.name)

        for description, weight, hsh in client.send_data(f.read()):
            desc = description.decode()
            for offset, data in hsh.items():
                mstr = utils.prettyhex(data)
                if len(mstr) > 50:
                    mstr = mstr[:24] + '...' + mstr[-23:]

                click.echo('at %08X: %s - %s' % (offset, desc, mstr))

                if csv:
                    csv_writer.writerow([f.name, '0x%08X' % offset,
                                         desc, mstr, len(data)])

    client.disconnect()

    if csv:
        csvfile.close()


@cli.command()
@click.option('-l', '--level', type=int, default=3,
              help='Select transformers with level 1, 2, or 3 and below')
@click.option('-o', '--only', type=int, default=None,
              help='Only use transformers on that specific level')
@click.option('-n', '--name', nargs=1, default=None,
              help='A list of transformer classes to use in quotes and '
              'is commas separated')
@click.option('-k', '--keep', default=20, help='How many transforms to save'
              'after stage 1')
@click.option('-s', '--save', default=10, help='How many transforms to save'
              'after stage 2')
@click.option('-z', '--zip', is_flag=True, help='Mark this file'
              'as a zip file. Use --password to enter zip password')
@click.option('--password', nargs=1, default=None, help='Only works if -z is '
              'set. Allows input of password for zip file')
@click.option('--no-save', is_flag=True, help="Don't save result to disk")
@click.option('-p', '--profiling', is_flag=True)
@click.option('-v', '--verbose', type=int, default=0,
              help='Set the verbose level (0 - 2)')
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.pass_context
def crack(ctx, level, only, name, keep, save, zip, password,
          no_save, profiling, verbose, filename):
    """
    Use patterns of interest to crack the supplied files.
    """
    load_all_transformers()

    if not zip and password is not None:
        raise ValueError("Password field is set without zip enable")

    trans = Transfomer(filename, password,
            LOCKE_TRANSFORMERS, zip,
            level, only, name, keep, save,
            no_save, verbose)

@cli.command()
@click.pass_context
def patterns(ctx):
    """
    List all patterns known by Locke.
    """
    for pat in apm.PatternPlugin.plugins():
        click.echo('%s (%s)' % (pat.Description, pat.Weight))


@cli.command()
@click.option('-l', '--level', type=int, default=3,
              help='Select transformers with level 1, 2, or 3 and below')
@click.option('-o', '--only', type=int, default=None,
              help='Only use transformers on that specific level')
@click.option('-n', '--name', nargs=1, default=None,
              help='A list of transformer classes to use in quotes and '
              'is commas separated')
@click.pass_context
def transforms(ctx, level, only, name):
    """
    List all transformations known by Locke.
    """
    load_all_transformers()
    trans_list = select_transformers(LOCKE_TRANSFORMERS, name, only, level)
    for trans in trans_list:
        click.echo('Class: %s | Level: %i' % (trans[0], trans[1].class_level()))
        click.echo(trans[1].__doc__)


if __name__ == '__main__':
    cli(obj={})
