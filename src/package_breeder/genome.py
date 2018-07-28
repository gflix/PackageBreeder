from package_breeder import genome_dependencies, tags

class Genome(object):

    name = None
    version = None
    dependencies = None

    def __init__(self, genome_input):
        if not isinstance(genome_input, dict):
            raise TypeError('wrong arguments')

        self.load(genome_input)

    def load(self, genome_input):
        self.name = genome_input[tags.TAG_NAME]
        self.version = genome_input[tags.TAG_VERSION]
        self.dependencies = genome_dependencies.GenomeDependencies(genome_input.get(tags.TAG_DEPENDENCIES))

    def __repr__(self):
        return 'Genome(name=%s, version=%s, dependencies=%s)' % (self.name, self.version, self.dependencies)
