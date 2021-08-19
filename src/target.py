import enum

class TargetType(enum.Enum):

    IP = 'IP'
    CIDR = 'CIDR'
    DOMAIN = 'DOMAIN'

class Target(object):

    def __init__(self, target : str, t_type : TargetType):
        self.target = target
        self.t_type = t_type
        self.info = {} # placeholder for intel

