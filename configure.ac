AC_PREREQ([2.61])
AC_INIT([selectz], [0.1], [johnandersenpdx@gmail.com])
AC_CONFIG_AUX_DIR(aux-dist)
AM_INIT_AUTOMAKE

AC_PROG_MAKE_SET
AC_PROG_CXX
AC_LANG(C++)

INSECURE=""
SECURE=""

CXXFLAGS="-std=c++11 -Wall -Werror -Wformat -Wformat-security"
CXXFLAGS+="fstack-protector-all -fPIC -D_FORTIFY_SOURCE=2"
# For reference these can be helpful for development
# CXXFLAGS+="-ggdb3 -O0 -U_FORTIFY_SOURCE"

AC_CONFIG_MACRO_DIR([m4])

LT_PREREQ([2.2])
LT_INIT([dlopen shared])

AC_CONFIG_FILES([Makefile include/Makefile src/Makefile])

AC_OUTPUT

