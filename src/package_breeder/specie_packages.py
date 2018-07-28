import textwrap

from package_breeder import tags

class SpeciePackages(object):

    included = None
    excluded = None

    def __init__(self, common_input, specie_input):
        if not isinstance(common_input, dict) or \
           not isinstance(specie_input, dict):
            raise TypeError('wrong arguments')

        self.load(common_input, specie_input)

    def load(self, common_input, specie_input):
        common_included = common_input.get(tags.TAG_INCLUDED, [])
        common_excluded = common_input.get(tags.TAG_EXCLUDED, [])

        specie_included = specie_input.get(tags.TAG_INCLUDED, [])
        specie_excluded = specie_input.get(tags.TAG_EXCLUDED, [])

        for entry in common_excluded:
            if entry in specie_included:
                common_excluded.remove(entry)

        for entry in common_included:
            if entry in specie_excluded:
                common_included.remove(entry)

        self.included = sorted(list(set(common_included + specie_included)))
        self.excluded = sorted(list(set(common_excluded + specie_excluded)))

    def get_debootstrap_arguments(self):
        return [
            '--include=%s' % (','.join(self.included)),
            '--exclude=%s' % (','.join(self.excluded))
        ]

    def serialize(self):
        return {
            tags.TAG_INCLUDED: self.included,
            tags.TAG_EXCLUDED: self.excluded
        }

    def __repr__(self):
        return 'SpeciePackages(included=%s, excluded=%s)' % (str(self.included), str(self.excluded))

    def __str__(self):
        return textwrap.indent('''\
included: %s
excluded: %s'''
             % (self.included, self.excluded), '  ')
