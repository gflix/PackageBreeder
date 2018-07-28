import logging
import os
import yaml

from package_breeder import specie

DIRECTORY_NESTS = 'nests'
SPECIES_FILE = 'species.yaml'
COMMON_SPECIE = 'common'

class Main(object):

    program_name = None
    version_information = None

    base_dir = None
    nests_dir = None
    species_file = None

    species = None

    def __init__(self, program_name, version_information):
        if not isinstance(program_name, str) or \
           not isinstance(version_information, str):
            raise TypeError('wrong arguments')

        self.program_name = program_name
        self.version_information = version_information

    def print_usage(self):
        print('USAGE: %s BASEDIR COMMAND [ARGS]' % self.program_name)
        print('')
        print('Arguments:')
        print('  BASEDIR     Base directory to work on')
        print('  COMMAND     Execute the given command (see below)')
        print('  [ARGS]      Optional and mandatory arguments to the chosen command')
        print('')
        print('Commands:')
        print('  build-nest  Build a nest for a given specie (chroot environment)')
        print('  species     List the available species (distributions and their architecture)')
        print('')
        print('Version information:')
        print('  %s' % self.version_information)
        print('')

    def run(self, base_dir, command, arguments):
        if not isinstance(base_dir, str) or \
           not isinstance(command, str) or \
           not isinstance(arguments, list):
            raise TypeError('wrong arguments')

        self.setup_paths(base_dir)
        self.check_preconditions()
        self.load_files()

        if command == 'species':
            self.run_command_species()
        elif command == 'build-nest':
            self.run_command_build_nest(arguments)
        else:
            self.print_usage()
            raise ValueError('unknown command "%s"' % command)

    def setup_paths(self, base_dir):
        self.base_dir = base_dir
        self.nests_dir = os.path.join(base_dir, DIRECTORY_NESTS)
        self.species_file = os.path.join(base_dir, SPECIES_FILE)

    def check_preconditions(self):
        if not os.path.isdir(self.base_dir):
            raise OSError('base directory "%s" does not exist' % self.base_dir)

        if not os.path.isdir(self.nests_dir):
            os.mkdir(self.nests_dir)

        if not os.path.isfile(self.species_file):
            raise OSError('species file "%s" does not exist' % self.species_file)

    def load_files(self):
        self.load_species(yaml.load(open(self.species_file)))

    def load_species(self, species_input):
        if not isinstance(species_input, dict):
            raise TypeError('invalid species file, expected a dictionary')

        self.species = {}
        common_input = {}
        if COMMON_SPECIE in species_input:
            common_input = species_input[COMMON_SPECIE]
            del species_input[COMMON_SPECIE]

        for key in species_input:
            self.species[key] = specie.Specie(common_input, species_input[key])

    def run_command_species(self):
        for key in self.species:
            specie = self.species[key]

            print('specie: %s' % key)
            print(str(specie))
            print()

    def run_command_build_nest(self, arguments):
        if (len(arguments) < 1):
            raise IndexError('missing specie')

        specie_name = arguments[0]
        if not specie_name in self.species:
            raise KeyError('unknown specie "%s"' % specie_name)

        nest_dir = os.path.join(self.nests_dir, specie_name)
        nest_image = os.path.join(self.nests_dir, specie_name + '.cpio.gz')
        logging.info('Building the nest for the specie "%s" at "%s"' % (specie_name, nest_dir))
        logging.info('Nest will be stored to "%s"' % (nest_image))
