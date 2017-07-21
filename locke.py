import click


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='be verbose')
@click.pass_context
def cli(ctx, verbose):
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
