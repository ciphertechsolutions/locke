#!/usr/bin/env python3

import click

import apm
import patterns


def abbr(bytes_):
    pretty = repr(bytes_)[1:]
    if len(pretty) > 50:
        pretty = pretty[:24] + '...' + pretty[-23:]
    return pretty


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def match(ctx, files):
    """
    Run all patterns against each supplied file, printing all matches
    in each file.
    """
    for file in files:
        click.echo('=' * 79)
        click.echo('File: %s\n' % file)
        mgr = apm.Manager(file)
        tups = mgr.run_all()
        for pat, matches in tups:
            if not matches:
                continue

            click.echo('%s: ' % pat.Description)
            for match in matches:
                click.echo('\tat %08X: %s' % (match.offset, abbr(match.data)))

        click.echo()
    click.echo('=' * 79)


@cli.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def weight(ctx, files):
    """
    Run all patterns against each supplied file, printing out a digest
    of each file's weight.
    """
    for file in files:
        click.echo('=' * 79)
        click.echo('File: %s\n' % file)
        mgr = apm.Manager(file)
        tups = mgr.run_all()
        weight = 0
        for pat, matches in tups:
            if not matches:
                continue
            else:
                weight += pat.Weight * len(matches)
        click.echo('Weight: %d' % weight)
        click.echo()
    click.echo('=' * 79)


if __name__ == '__main__':
    cli(obj={})
