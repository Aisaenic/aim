import click, logging, subprocess, re, csv, functools, validators

from target import Target, TargetType
logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.option('-t', '--targets', help='The intended target IPs/CIDR ranges/domain names or space/comma-delimited list of targets. Must be provided if no input file is provided.')
@click.option('-v', '--verbose', is_flag=True, help='If provided, aggregates maximum report, verbose mode.')
@click.option('-in', '--inputfile', type=click.Path(exists=True, readable=True), help='If provided, reads targets from file at the given input file path. All other inputs will be ignored. File must have one target per line.')
@click.option('-debug', '--debug', is_flag=True, help='If provided, debug mode displays all the targets that were tossed out.')
def main(targets : str, verbose : bool, inputfile : click.Path, debug : bool) -> None:
    """TODO: Add OWASP Sanitizer and Fix this Message"""

    # compile list of targets, remove duplicates, store improperly-formatted ones for error message
    dir_tar = None
    if inputfile: # only from input or from direct cli, not both
        with open(inputfile, 'r') as tar_in:
            dir_tar = set(map(lambda i : i.strip(), tar_in))
    elif targets:
        dir_tar = set(map(lambda i : i.strip(), re.split(',\s|[, ]', targets.strip())))
    else:
        logging.error("If no input file is provided, targets must be directly provided. Please run aim with --help for more info.")
        return

    affirmed = get_validated_targets(dir_tar, verbose, debug)
    
    for a in affirmed:
        print(str(a))
    
    """
    # TODO: now resolve targets
    # do basic if not verbose
    # otherwise do everything
    results = []
    mod_base = subprocess.run(["python3", "resolve_non_verbose.py", affirmed], stdout=subprocess.PIPE)
    results.append(mod_base.stdout)

    if verbose:
        mod_one = subprocess.run(["python3", "one.py", affirmed], stdout=subprocess.PIPE)
        mod_two = subprocess.run(["python3", "two.py", affirmed], stdout=subprocess.PIPE)
        results.append(mod_one.stdout, mod_two.stdout)

    # handle output, by writing it to stdout or output file, if specified
    if outputfile:
        with open(outputfile, 'w') as results_out:
            for r in results:
                results_out.write(r)
    """

# gets list of resolvable targets, returns list
def get_validated_targets(dir_tar : list, verbose : bool = False, debug : bool = False) -> list:
    affirmed = []
    if dir_tar:
        for t in dir_tar:
            try:
                t_type = can_resolve(t)
                if t_type == TargetType.DOMAIN:
                    t = t.replace('https://', '')
                    t = t.replace('http://', '')
                affirmed.append(Target(t, t_type, verbose))
            except Exception as e:
                if debug:
                    logging.error(e)
    return affirmed

# returns the type of format the given target is in, or raises exception if the format is invalid
def can_resolve(candidate : str) -> Target:
    if candidate and candidate != '':
        split_by_dot = re.split('[./]', candidate)
        # check if it's a valid IP address
        if len(split_by_dot) <= 5 and not re.search('[a-zA-Z]', candidate) and all(0 <= int(i) and int(i) <= 255 for i in split_by_dot): # can cast to int because check for alpha has to pass first
            if candidate.count('/') == 1 and len(split_by_dot) == 5 and 0 <= int(split_by_dot[-1]) and int(split_by_dot[-1]) <= 32: # check if is CIDR range
                return TargetType.CIDR
            elif len(split_by_dot) == 4:
                return TargetType.IP
        elif validators.domain(candidate.replace('https://','')) or validators.domain(candidate.replace('http://', '')): # check if it is a valid domain name, remove prepending protocol if there
            return TargetType.DOMAIN
    raise ValueError(f'Invalid value for target provided: {candidate}')

if __name__ == '__main__':
    main()
