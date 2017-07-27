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


@cli.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def weight(ctx, files):
    pass


if __name__ == '__main__':
    cli(obj={})
