import datetime

from package_breeder import specie, tags

class Nest(object):

    built = None
    specie = None

    def __init__(self, nest_information):
        if not isinstance(nest_information, dict):
            raise TypeError('wrong arguments')

        self.load(nest_information)

    def load(self, nest_information):
        self.built = datetime.datetime.strptime(nest_information[tags.TAG_BUILT], "%Y-%m-%dT%H:%M:%S")
        self.specie = specie.Specie({}, nest_information[tags.TAG_SPECIE])

    def __repr__(self):
        return 'Nest(built=%s, specie=%s)' % (self.built.isoformat(timespec='seconds'), self.specie)
