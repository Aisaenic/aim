import click, logging, subprocess, re, csv
logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.argument('targets', type=str)
@click.option('-v', '--verbose', is_flag=True, help='If provided, aggregates maximum report, verbose mode')
@click.option('-in', '--inputfile', type=click.Path(exists=True, readable=True), help='If provided, reads target IPs/domains from file at the given input file path. File must have one target on each line.')
@click.option('-out', '--outputfile', type=click.Path(), help='If provided, directs output of AIM into the file at the given output file path. Creates file if it does not exist.')
def main(targets : str, verbose : bool, inputfile : click.File, outputfile : click.File) -> None:
    """ TARGETS is the intended target IP/domain or space/comma-delimited list of targets"""

    # compile list of targets, remove duplicates, store improperly-formatted ones for error message
    dir_tar = list(map(lambda i : i.strip(), re.split(',\s|[, ]', targets)))
    if inputfile:
        with open(inputfile) as tar_in:
            dir_tar.extend(list(map(lambda i : i.strip(), tar_in)))
            dir_tar = set(dir_tar)
    # add 'unable to resolve here'
    

if __name__ == '__main__':
    main()
