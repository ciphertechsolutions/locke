#!/usr/bin/python3
from locke.patterns import PatternPlugin
from locke.patterns.manager import Manager
import locke.patterns.plugins  # noqa - needed for module loading
import locke.transforms.plugins  # noqa - needed for module loading
import locke.transforms.utils as utils
from locke.transforms.transformer import select_transformers, run_transformations, \
    write_to_disk, TransformChar, TransformString, test_transforms
from locke.transforms.utils import generate_database, print_table

import csv as csvlib
from os import path, makedirs
import click

# Nest array. One for each level
TRANSFORMERS = ([], [], [])


def load_all_transformers():
    for cls in (TransformChar, TransformString):
        for trans in cls.__subclasses__():
            if 0 < trans.class_level() < 4:
                TRANSFORMERS[trans.class_level() - 1].append(trans)
            elif trans.class_level() == -1:
                print("!! %s is disabled" % trans.__name__)
            elif trans.class_level() == 0:
                pass
            else:
                print('%s has an invalid class level (1-3 | -1 --> disable\n)'
                      % trans.__name__)


def search_data(data):
    mgr = Manager(stage=2, raw=data)
    msgs = []
    for pat, matches in mgr.run():
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
@click.argument('files', type=click.File('rb'), nargs=-1)
@click.pass_context
def search(ctx, csv, files):
    """
    Search for patterns of interest in the supplied files.
    """

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

        for description, weight, hsh in search_data(f.read()):
            desc = description.decode()
            for offset, data in hsh.items():
                mstr = utils.prettyhex(data)
                if len(mstr) > 50:
                    mstr = mstr[:24] + '...' + mstr[-23:]

                click.echo('at %08X: %s - %s' % (offset, desc, mstr))

                if csv:
                    csv_writer.writerow([f.name, '0x%08X' % offset,
                                         desc, mstr, len(data)])

    if csv:
        csvfile.close()


@cli.command()
@click.option('-l', '--level', type=int, default=1,
              help='Select transformers with level 1, 2, or 3 and below')
@click.option('-o', '--output', type=str, default='output',
              help='Output directory for transformed files')
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
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.pass_context
def crack(ctx, level, output, name, keep, save, zip_file, password,
          no_save, verbose, filename):
    """
    Use patterns and transformations of interest to crack the supplied files.
    """
    if not path.exists(locke.transforms.utils.DBFILE):
        print('Run generate to create a new transforms.db')
        return 1
    if path.exists(output) and path.isfile(output):
        return 1
    makedirs(output, exist_ok=True)
    load_all_transformers()
    if not zip_file and password is not None:
        raise ValueError("Password field is set without zip enable")

    trans_list = select_transformers(TRANSFORMERS, name, level=level)
    results = run_transformations(trans_list, filename, keep,
                                  zip_file, password, verbose)[:save]

    # TODO
    # Call on save to disk here? or Make run_transformation call write to disk?
    if not no_save:
        write_to_disk(results, output, filename)


@cli.command()
@click.pass_context
def patterns(ctx):
    """
    List all patterns known by Locke.
    """
    headers = ['Stage','Description', 'Weight']
    values = [[pat.Stage, pat.Description, pat.Weight]
              for pat in PatternPlugin.plugins()]
    print_table(headers, values)


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
@click.option('-g', '--generate', is_flag=True, help='generate '
                                                     'transforms database')
@click.pass_context
def transforms(ctx, level, only, name, test, generate):
    """
    List all transformations known by Locke. Also generate a new transforms.db
    and test algorithm duplications.
    """
    load_all_transformers()
    trans_list = select_transformers(TRANSFORMERS, name, only, level,
                                     listing=True)
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
        headers = ['Level', 'Name', 'Description', 'Params']
        values = [[trans.class_level(),
                   trans.__name__,
                   trans.description,
                   trans.params]
                  for trans in trans_list]
        print_table(headers, values)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
