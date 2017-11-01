#!/usr/bin/python3.5
import csv as csvlib
import sys
from os import path

import click

SCRIPT_DIR = path.dirname(path.abspath(__file__))  # shouldnt need this
sys.path.append(path.join(SCRIPT_DIR, 'apm'))  # shouldnt need this

import apm
import patterns # noqa - needed for module loading
import transformers # noqa - needed for module loading
import liblocke.utils as utils
from liblocke.transformer import select_transformers, run_transformations, \
    write_to_disk, TransformChar, TransformString, test_transforms
from transformers.utils import generate_database

# Nest array. One for each level
TRANSFORMERS = ([], [], [])


def load_all_transformers():
    for cls in (TransformChar, TransformString):
        for trans in cls.__subclasses__():
            if 0 < trans.class_level() < 4:
                TRANSFORMERS[trans.class_level() - 1].append(trans)
            elif trans.class_level() == -1:
                print("!! %s is disabled" % trans.__name__)
            else:
                print("%s has an invalid class level (1 - 3 | -1 --> disable\n)"
                      % trans.__name__)


def search_standalone(data):
    score = 0
    mgr = apm.Manager(raw=data)
    msgs = []
    for pat, matches in mgr.run_standalone():
        if not matches:
            continue

        match_hash = {}
        for match in matches:
            match_hash[match.offset] = match.data

        msgs.append([pat.Description.encode(), pat.Weight, match_hash])

    del mgr

    return msgs


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option('--csv', default=None, help='output results as CSV')
@click.option('-st', '--standalone', is_flag=True, help='standalone mode')
@click.argument('files', type=click.File('rb'), nargs=-1)
@click.pass_context
def search(ctx, csv, standalone, files):
    """
    Search for patterns of interest in the supplied files.
    """
    if not standalone:
        client = apm.client.TCPClient()
        print(client.host, client.port)
        client.connect()
        print('Made connection')

    if csv:
        click.echo('Writing CSV results to %s' % csv)
        csvfile = open(csv, 'w')
        csv_writer = csvlib.writer(csvfile)
        csv_writer.writerow(['Filename', 'Index', 'Pattern name', 'Match',
                             'Length'])

    # TODO: Could Pool the searches
    for f in files:
        click.echo("=" * 79)
        click.echo("File: %s\n" % f.name)

        for description, weight, hsh in search_standalone(
                f.read()) if standalone \
                else client.send_data(f.read()):
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
@click.option('-l', '--level', type=int, default=2,
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
@click.option('-z',
              '--zip_file',
              is_flag=True,
              help='Mark this file'
                   'as a zip file. Use --password to enter zip password')
@click.option('--password',
              nargs=1,
              default=None,
              help='Only works if -z is '
                   'set. Allows input of password for zip file')
@click.option('--no-save', is_flag=True, help="Don't save result to disk")
@click.option('-v',
              '--verbose',
              type=int,
              default=0,
              help='Set the verbose level '
                   'Valid inputs are 0 - 2 (lowest output to highest). '
                   'Note that -v 2 is not human friendly')
@click.option('-st', '--standalone', is_flag=True, help='standalone mode')
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.pass_context
def crack(ctx, level, only, name, keep, save, zip_file, password,
          no_save, verbose, standalone, filename):
    """
    Use patterns of interest to crack the supplied files.
    """
    if not path.exists(transformers.utils.DBFILE):
        print('Run generate to create a new transforms.db')
        return 1
    load_all_transformers()
    if not zip_file and password is not None:
        raise ValueError("Password field is set without zip enable")

    trans_list = select_transformers(TRANSFORMERS, name, only, level)
    results = run_transformations(trans_list, filename, keep, standalone,
                                  zip_file, password, verbose)[:save]

    # TODO
    # Call on save to disk here? or Make run_transformation call write to disk?
    if not no_save:
        write_to_disk(results, filename)


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
@click.option('-t', '--test', is_flag=True, help='test transformations '
                                                 'for simplification')
@click.option('-g', '--generate', is_flag=True, help='generate transformations '
                                                     'database')
@click.pass_context
def transforms(ctx, level, only, name, test, generate):
    """
    List all transformations known by Locke.
    """
    load_all_transformers()
    trans_list = select_transformers(TRANSFORMERS, name, only, level, listing=True)
    if test:
        test_transforms(trans_list)
    elif generate:
        print('Generating new transforms.db file')
        charonly = []
        for trans in trans_list:
            if issubclass(trans, TransformChar):
                charonly.append(trans)
        del trans
        generate_database(charonly)
    else:
        for trans in trans_list:
            click.echo(
                'Class: %s | Level: %i' % (trans.__name__, trans.class_level()))
            click.echo(trans.__doc__)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
