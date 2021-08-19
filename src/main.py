import click, logging, subprocess, re, csv, functools, validators, subprocess
from target import Target, TargetType
logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.argument('targets', type=str)
@click.option('-v', '--verbose', is_flag=True, help='If provided, aggregates maximum report, verbose mode.')
@click.option('-in', '--inputfile', type=click.Path(exists=True, readable=True), help='If provided, reads target IPs/domains from file at the given input file path. File must have one target on each line.')
@click.option('-out', '--outputfile', type=click.Path(), help='If provided, directs output of AIM into the file at the given output file path. Creates file if it does not exist.')
@click.option('-debug', '--debug', is_flag=True, help='If provided, debug mode displays all the targets that were tossed out.')
def main(targets : str, verbose : bool, inputfile : click.Path, outputfile : click.Path, debug : bool) -> None:
    """ TARGETS is the intended target IP/CIDR range/domain name or space/comma-delimited list of targets"""

    # compile list of targets, remove duplicates, store improperly-formatted ones for error message
    dir_tar = list(map(lambda i : i.strip(), re.split(',\s|[, ]', targets)))
    if inputfile:
        with open(inputfile) as tar_in:
            dir_tar.extend(list(map(lambda i : i.strip(), tar_in)))
            dir_tar = set(dir_tar)
    # add 'unable to resolve here'
    affirm = []
    for t in dir_tar:
        t_type = can_resolve(t)
        if t_type:
            if t_type == TargetType.DOMAIN:
                t = t.replace('https://', '')
                t = t.replace('http://', '')
            affirm.append(Target(t, t_type, verbose))
        elif debug:
            logging.error(f'Invalid target provided: {t}')

    for a in affirm:
        print(str(a))
    # now resolve targets
    # do basic if not verbose
    # otherwise do everything
            
# returns the type of format the given target is in, or None if the format is invalid
def can_resolve(candidate : str) -> Target:
    split_by_dot = re.split('[./]', candidate)
    # check if it's a valid IP address
    if len(split_by_dot) <= 5 and not re.search('[a-zA-Z]', candidate) and all(0 <= int(i) and int(i) <= 255 for i in split_by_dot): # can cast to int because check for alpha has to pass first
        if candidate.count('/') == 1 and len(split_by_dot) == 5 and 0 <= int(split_by_dot[-1]) and int(split_by_dot[-1]) <= 32: # check if is CIDR range
            return TargetType.CIDR
        elif len(split_by_dot) == 4:
            return TargetType.IP
    elif validators.domain(candidate.replace('https://','')) or validators.domain(candidate.replace('http://', '')): # check if it is a valid domain name, remove prepending protocol if there
        return TargetType.DOMAIN
    return None

if __name__ == '__main__':
    main()
