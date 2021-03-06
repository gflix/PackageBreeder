import datetime
import logging
import os
import shutil
import subprocess
import yaml

from package_breeder import genome, nest, specie, tags

DIRECTORY_GENOMES = 'genomes'
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
        print('  BASEDIR       Base directory to work on')
        print('  COMMAND       Execute the given command (see below)')
        print('  [ARGS]        Optional and mandatory arguments to the chosen command')
        print('')
        print('Commands:')
        print('  build-nest    Build a nest for a given specie (chroot environment)')
        print('  build-nests   Build nests for all species which do not have one already (chroot environments)')
        print('  hatch-an-egg  Hatch an egg for a given specie using a given genome (build a package)')
        print('  species       List the available species (distributions and their architecture)')
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
        elif command == 'build-nests':
            self.run_command_build_nests()
        elif command == 'hatch-an-egg':
            self.run_command_hatch_an_egg(arguments)
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
            self.species[key] = specie.Specie(common_input, species_input[key], key)

    def run_command_species(self):
        for key in self.species:
            specie = self.species[key]

            print('specie:')
            print(str(specie))
            try:
                built_nest = specie.get_nest(self.nests_dir)
                print('  nest: built %s' % built_nest.built.isoformat(timespec='seconds'))
            except OSError as e:
                print('  nest: not available (%s)' % str(e))

            print()

    def run_command_build_nest(self, arguments):
        if (len(arguments) < 1):
            raise IndexError('missing specie')

        specie_name = arguments[0]
        if not specie_name in self.species:
            raise KeyError('unknown specie "%s"' % specie_name)

        chosen_specie = self.species[specie_name]
        nest_dir = os.path.join(self.nests_dir, specie_name)
        nest_image = os.path.join(self.nests_dir, specie_name + '.cpio.gz')
        nest_information = os.path.join(self.nests_dir, specie_name + '.yaml')
        self.build_nest(chosen_specie, nest_dir, nest_image, nest_information)

    def build_nest(self, chosen_specie, nest_dir, nest_image, nest_information):
        if not isinstance(chosen_specie, specie.Specie):
            raise TypeError('wrong arguments')

        logging.info('Building the nest for the specie "%s" at "%s"' % (chosen_specie.name, nest_dir))
        logging.info('Nest will be stored to "%s"' % (nest_image))

        if os.path.isdir(nest_dir):
            logging.info('Removing the old nest first...')
            shutil.rmtree(nest_dir)

        arguments = ['qemu-debootstrap']
        arguments += chosen_specie.get_debootstrap_arguments()
        arguments += [nest_dir]
        logging.debug('arguments=%s', arguments)

        subprocess.check_call(arguments)

        arguments = ['sh', '-c', 'cd "%s" && ( find . | sort | cpio -o | gzip > %s )' % (nest_dir, nest_image)]
        logging.debug('arguments=%s', arguments)

        subprocess.check_call(arguments)

        build_information = {
            tags.TAG_SPECIE: chosen_specie.serialize(),
            tags.TAG_BUILT: datetime.datetime.now().isoformat(timespec='seconds')
        }

        open(nest_information, 'w').write(yaml.dump(build_information, default_flow_style=False))

        if os.path.isdir(nest_dir):
            logging.info('Temporary files...')
            shutil.rmtree(nest_dir)

        logging.info('Finished building the nest for the specie "%s"' % chosen_specie.name)

    def run_command_build_nests(self):
        for specie_name in self.species:
            nest_information = os.path.join(self.nests_dir, specie_name + '.yaml')
            try:
                built_nest = nest.Nest(yaml.load(open(nest_information)))
                logging.info('Nest for the specie "%s" already exists and was built %s. Skipping.' %
                    (specie_name, built_nest.built.isoformat(timespec='seconds')))
            except OSError:
                chosen_specie = self.species[specie_name]
                nest_dir = os.path.join(self.nests_dir, specie_name)
                nest_image = os.path.join(self.nests_dir, specie_name + '.cpio.gz')

                self.build_nest(chosen_specie, nest_dir, nest_image, nest_information)

    def run_command_hatch_an_egg(self, arguments):
        if (len(arguments) < 2):
            raise IndexError('give specie and genome')

        specie_name = arguments[0]
        genome_file = arguments[1]

        if not specie_name in self.species:
            raise KeyError('unknown specie "%s"' % specie_name)

        if len(os.path.dirname(genome_file)) == 0:
            genome_file = os.path.join(self.base_dir, DIRECTORY_GENOMES, genome_file)

        if not os.path.isfile(genome_file):
            raise OSError('genome file "%s" does not exists' % genome_file)

        chosen_genome = genome.Genome(yaml.load(open(genome_file)))
        chosen_specie = self.species[specie_name]

        logging.info('Chosen genome:')
        logging.info(str(chosen_genome))
        logging.info('Chosen specie:')
        logging.info(str(chosen_specie))

        self.hatch_an_egg(chosen_genome, chosen_specie)

    def hatch_an_egg(self, chosen_genome, chosen_specie):
        if not isinstance(chosen_genome, genome.Genome) or \
           not isinstance(chosen_specie, specie.Specie):
            raise TypeError('wrong arguments')

        built_nest = chosen_specie.get_nest(self.nests_dir)
        logging.info('Using nest of specie "%s" built %s to hatch the egg for genome "%s-%s"' % \
            (chosen_specie.name, built_nest.built.isoformat(timespec='seconds'), chosen_genome.name, chosen_genome.version))

        nest_image = os.path.join(self.nests_dir, chosen_specie.name + '.cpio.gz')
