AC_PREREQ([2.69])
AC_INIT([package-breeder],[0.1.0],[felix.mellmann@gmail.com])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE()

AM_PATH_PYTHON([3.5])

AC_DEFINE_DIR([PYTHONDIR], [pythondir], [Path at which python files are placed to.])

AC_CONFIG_FILES([
    Makefile
    contrib/Makefile
    src/Makefile
    src/package-breeder:src/package-breeder.py
    src/package_breeder/Makefile
])
AC_OUTPUT
