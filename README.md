PackageBreeder
==============

This tool aims to provide a mechanism to semi-automatically build a set of
Debian packages for various platforms (Debian based distributions and
architectures).

Terms were chosen according to birds building nests and breeding eggs.
Each specie is specified by a target distribution and a architecture.
The tool can be used to build a nest for this specie.
The nest is a chroot environment equipped with a build environment and a statically linked QEMU instance to run foreign binaries on the host system.
Genomes specify the blueprint for built packages.
Genomes can depend on packages from official sources and our own packages.
The tool will try to resolve dependencies.
When hatching eggs the genome is taken and put into each species nest. For each specie and egg is hatched based on the genome.
