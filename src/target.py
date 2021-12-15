import enum

class TargetType(enum.Enum):

    IP = 'IP'
    CIDR = 'CIDR'
    DOMAIN = 'DOMAIN'

class Target(object):

    def __init__(self, target : str, t_type : TargetType, verbose : bool):
        self.target = target
        self.t_type = t_type
        if verbose:
            self.r_type = 'verbose'
        else:
            self.r_type = 'concise'

    def __str__(self) -> str:
        return f'Target: {self.target}, Type: {self.t_type}'
    
    # returns all data aggregated on target in json form
    def report(self) -> dict:
        data = {'target': self.target, 'type': self.t_type, 'report_type': self.r_type}
        return data
