import textwrap

from package_breeder import specie_packages, tags

class Specie(object):

    name = None
    distribution = None
    architecture = None
    packages = None

    def __init__(self, common_input, specie_input, name = None):
        if not isinstance(common_input, dict) or \
           not isinstance(specie_input, dict):
            raise TypeError('wrong arguments')

        self.name = name
        self.load(common_input, specie_input)

    def load(self, common_input, specie_input):
        self.name = \
            specie_input.get(tags.TAG_NAME, self.name)
        self.distribution = \
            specie_input.get(tags.TAG_DISTRIBUTION, common_input.get(tags.TAG_DISTRIBUTION))
        self.architecture = \
            specie_input.get(tags.TAG_ARCHITECTURE, common_input.get(tags.TAG_ARCHITECTURE))
        self.packages = \
            specie_packages.SpeciePackages(
                common_input.get(tags.TAG_PACKAGES, {}),
                specie_input.get(tags.TAG_PACKAGES, {})
            )

        if not isinstance(self.distribution, str) or \
           not isinstance(self.architecture, str):
            raise TypeError('invalid specie')

    def get_debootstrap_arguments(self):
        arguments = ['--arch=%s' % self.architecture]
        arguments += self.packages.get_debootstrap_arguments()
        arguments += [self.distribution]

        return arguments

    def serialize(self):
        return {
            tags.TAG_NAME: self.name,
            tags.TAG_ARCHITECTURE: self.architecture,
            tags.TAG_DISTRIBUTION: self.distribution,
            tags.TAG_PACKAGES: self.packages.serialize()
        }

    def __repr__(self):
        return 'Specie(distribution=%s, architecture=%s, packages=%s)' % \
            (self.distribution, self.architecture, self.packages)

    def __str__(self):
        return textwrap.indent('''\
name: %s
distribution: %s
architecture: %s
packages:
%s'''
             % (self.name, self.distribution, self.architecture, str(self.packages)), '  ')
