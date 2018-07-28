import textwrap

from package_breeder import tags

class GenomeDependencies(object):

    external = None
    internal = None

    def __init__(self, dependencies_input):
        self.load(dependencies_input)

    def load(self, dependencies_input):
        self.external = None
        self.internal = None

        if isinstance(dependencies_input, dict):
            self.external = dependencies_input.get(tags.TAG_EXTERNAL)
            self.internal = dependencies_input.get(tags.TAG_INTERNAL)

        if self.external is None:
            self.external = []

        if self.internal is None:
            self.internal = []

        if not isinstance(self.external, list) or \
           not isinstance(self.internal, list):
            raise TypeError('invalid dependencies')

    def __repr__(self):
        return 'GenomeDependencies(external=%s, internal=%s)' % (self.external, self.internal)

    def __str__(self):
        return textwrap.indent('''\
external: %s
internal: %s'''
             % (', '.join(self.external), ', '.join(self.internal)), '  ')
