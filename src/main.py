import click, logging, subprocess, re

@click.command()
@click.argument('targets', type=str, nargs=-1)
@click.option('-v', '--verbose', is_flag=True, help='If provided, aggregates maximum report, verbose mode')
@click.option('-in', '--inputfile', type=click.File('rb', lazy=True), help='If provided, reads target IPs/domains from given input file')
@click.option('-out', '--outfile', type=click.File('wb', lazy=True), help='If provided, directs output of AIM into given output file')
def main(targets : str, verbose : bool, inputfile : click.File, outputfile : click.File) -> None:
    dir_tar = list(map(lambda i : i.strip(), re.split('[, ]', targets)))
    print(dir_tar)

if __name__ == '__main__':
    main()
