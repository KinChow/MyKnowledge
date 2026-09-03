---
archive_policy: text-only
attachments:
- filename: gcc-prerequisites.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:c758be6ae6656d10e4173d1328c2e05b47ba3d2ca85e313ca7b0dcdfca03bfdf
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-0df0f0181d75
  position:
    end: 8130
    start: 8060
    type: TextPositionSelector
  quote_sha256: sha256:e7069697b5128d83d12fcae2a57bc7fffb36362ea42a46c7e544a6024cddfafe
  selector:
    exact: Necessary to build GCC. It can be downloaded from https://gmplib.org/.
    prefix: 't way to install the libraries.

      '
    suffix: ' If a GMP source distribution is'
    type: TextQuoteSelector
  selector_sha256: sha256:6d1d0c90525937c04262cd2a8c438a1aaf235584c86dfa59564993ac07993434
  snapshot_sha256: sha256:feec2a80c4acb4b3f9d496751c45199c69e4d68f8320a47f8740d43365102316
- evidence_id: evidence-afe64130d587
  position:
    end: 8619
    start: 8548
    type: TextPositionSelector
  quote_sha256: sha256:bd517e65fcf9a2b9cfc796faf749c73ce241cfdd0905df3c989ee00cb92658d7
  selector:
    exact: Necessary to build GCC. It can be downloaded from https://www.mpfr.org.
    prefix: 'ownload_prerequisites installs.

      '
    suffix: ' If an MPFR source distribution '
    type: TextQuoteSelector
  selector_sha256: sha256:3f228e406c952542b2549035e6850b6697fd7dd640dc86317be43ec967c56e2d
  snapshot_sha256: sha256:feec2a80c4acb4b3f9d496751c45199c69e4d68f8320a47f8740d43365102316
- evidence_id: evidence-60b61915a72e
  position:
    end: 9122
    start: 9036
    type: TextPositionSelector
  quote_sha256: sha256:0d8847386ef8548f5d22a06b113b14b33d5cb65388542d5d47b7b3de4ef280df
  selector:
    exact: Necessary to build GCC. It can be downloaded from https://www.multiprecision.org/mpc/.
    prefix: 'ownload_prerequisites installs.

      '
    suffix: ' If an MPC source distribution i'
    type: TextQuoteSelector
  selector_sha256: sha256:a764b3e0cbe1b9d7ea634abc6755fc596b01fbca4e8db0a257b41fe5427ff7de
  snapshot_sha256: sha256:feec2a80c4acb4b3f9d496751c45199c69e4d68f8320a47f8740d43365102316
extractor: trafilatura/2.2.0
id: gcc-prerequisites
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/c758be6ae6656d10e4173d1328c2e05b47ba3d2ca85e313ca7b0dcdfca03bfdf.html
  sha256: sha256:c758be6ae6656d10e4173d1328c2e05b47ba3d2ca85e313ca7b0dcdfca03bfdf
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://gcc.gnu.org/install/prerequisites.html
  url: https://gcc.gnu.org/install/prerequisites.html
schema_version: source/v1
snapshot_sha256: sha256:feec2a80c4acb4b3f9d496751c45199c69e4d68f8320a47f8740d43365102316
source_type: doc
vault_id: public
---
GCC requires that various tools and packages be available for use in the build procedure. Modifying GCC sources requires additional tools described below.
Necessary to bootstrap GCC. GCC 5.4 or newer has sufficient support for used C++14 features.
Versions of GCC prior to 15 allow bootstrapping with an ISO C++11 compiler, versions prior to 10.5 allow bootstrapping with an ISO C++98 compiler, and versions prior to 4.8 allow bootstrapping with an ISO C89 compiler.
If you need to build an intermediate version of GCC in order to bootstrap current GCC, consider GCC 9.5: it can build the current D compiler, and was also the version that declared C++17 support stable.
To build all languages in a cross-compiler or other configuration where 3-stage bootstrap is not performed, you need to start with an existing GCC binary (of a new enough version) because source code for language frontends other than C and C++ might use GCC extensions.
In order to build GCC, the C standard library and headers must be present for all target variants for which target libraries will be built (and not only the variant of the host C++ compiler).
This affects the popular ‘x86_64-pc-linux-gnu’ platform (among other multilib targets), for which 64-bit (‘x86_64’) and 32-bit (‘i386’) libc headers are usually packaged separately. If you do a build of a native compiler on ‘x86_64-pc-linux-gnu’, make sure you either have the 32-bit libc developer package properly installed (the exact name of the package depends on your distro) or you must build GCC as a 64-bit only compiler by configuring with the option --disable-multilib. Otherwise, you may encounter an error such as ‘fatal error: gnu/stubs-32.h: No such file’
If you configure a RISC-V compiler with the option --with-arch and
the specified architecture string is non-canonical, then you will need
python installed on the build system.
In order to build GNAT, the Ada compiler, you need a working GNAT compiler (GCC version 5.4 or later).
This includes GNAT tools such as gnatmake and
gnatlink, since the Ada front end is written in Ada and
uses some GNAT-specific extensions.
In order to build a cross compiler, it is strongly recommended to install the new compiler as native first, and then use it to build the cross compiler. Other native compiler versions may work but this is not guaranteed and will typically fail with hard to understand compilation errors during the build.
Similarly, it is strongly recommended to use an older version of GNAT to build GNAT. More recent versions of GNAT than the version built are not guaranteed to work and will often fail during the build with compilation errors.
Note that configure does not test whether the GNAT installation works
and has a sufficiently recent version; if too old a GNAT version is
installed and --enable-languages=ada is used, the build will fail.
ADA_INCLUDE_PATH and ADA_OBJECT_PATH environment variables
must not be set when building the Ada compiler, the Ada tools, or the
Ada runtime libraries. You can check that your build environment is clean
by verifying that ‘gnatls -v’ lists only one explicit path in each
section.
The COBOL compiler, gcobol, first appeared in GCC 15. To build the COBOL parser, you need GNU Bison 3.8.2, the current version of as of this writing, released 2021-09-25. To build the lexer requires GNU Flex 2.6.4, also the current version as of this writing, released on 2017-05-06.
The gcobol documentation is maintained as manpages using troff mdoc. GNU groff is required to convert them to PDF format. Conversion to HTML is done with mandoc, available at https://mandoc.bsd.lv.
The COBOL runtime library. libgcobol, requires libxml2 2.9 or later.
It implements support for XML PARSE.
Because ISO COBOL defines strict requirements for numerical precision,
gcobol computes with 128-bit operands.  This requirement applies to
both host and target. For integers, gcobol requires the platform to
support the GCC __int128 type.  For floating point it uses
_Float128 or similar.
gcobol has so far been tested on two architectures only: x86_64 and aarch64 with little-endian encoding.
In order to build GDC, the D compiler, you need a working GDC compiler (GCC version 9.4 or later) and D runtime library, ‘libphobos’, as the D front end is written in D.
Versions of GDC prior to 12 can be built with an ISO C++11 compiler, which can then be installed and used to bootstrap newer versions of the D front end.
It is strongly recommended to use an older version of GDC to build GDC. More recent versions of GDC than the version built are not guaranteed to work and will often fail during the build with compilation errors relating to deprecations or removed features.
Note that configure does not test whether the GDC installation works
and has a sufficiently recent version.  Though the implementation of the D
front end does not make use of any GDC-specific extensions, or novel features
of the D language, if too old a GDC version is installed and
--enable-languages=d is used, the build will fail.
On some targets, ‘libphobos’ isn’t enabled by default, but compiles and works if --enable-libphobos is used. Specifics are documented for affected targets.
Python3 is required if you want to build the complete Modula-2
documentation including the target SYSTEM definition module.
If Python3 is unavailable Modula-2 documentation will include a target
independent version of the SYSTEM modules.
The official Rust compiler and Rust build system (cargo) are required for building various parts of the gccrs frontend, until gccrs can compile them by itself. The minimum supported Rust version is 1.49.
Necessary when running configure because some
/bin/sh shells have bugs and may crash when configuring the
target libraries.  In other cases, /bin/sh or ksh
have disastrous corner-case performance problems.  This
can cause target configure runs to literally take days to
complete in some cases.
So on some platforms /bin/ksh is sufficient, on others it
isn’t.  See the host/target specific instructions for your platform, or
use bash to be sure.  Then set CONFIG_SHELL in your
environment to your “good” shell prior to running
configure/make.
zsh is not a fully compliant POSIX shell and will not
work when configuring GCC.
Necessary to build the lexical analysis module.
Necessary for creating some of the generated source files for GCC. If in doubt, use a recent GNU awk version.
Necessary in some circumstances, optional in others. See the host/target specific instructions for your platform for the exact requirements.
Binutils 2.35 or newer is required for LTO to work correctly with GNU libtool that includes doing a bootstrap with LTO enabled.
Necessary to uncompress GCC tar files when source code is
obtained via HTTPS mirror sites.
You must have GNU make installed to build GCC.
Necessary (only on some platforms) to untar the source code.  Many
systems’ tar programs will also work, only try GNU
tar if you have problems.
Necessary when targeting Darwin, building ‘libstdc++’,
and not using --disable-symvers.
Necessary when targeting Solaris with Solaris ld and not using
--disable-symvers.
Necessary when regenerating Makefile dependencies in libiberty. Necessary when regenerating libiberty/functions.texi. Necessary when generating manpages from Texinfo manuals. Used by various scripts to generate some files included in the source repository (mainly Unicode-related and rarely changing) from source tables.
Used by automake.
If available, enables parallel testing of ‘libgomp’ in case that
flock is not available.
Several support libraries are necessary to build GCC, some are required, others optional. While any sufficiently new version of required tools usually work, library requirements are generally stricter. Newer versions may work in some cases, but it’s safer to use the exact versions documented. We appreciate bug reports about problems with newer versions, though. If your OS vendor provides packages for the support libraries then using those packages may be the simplest way to install the libraries.
Necessary to build GCC. It can be downloaded from https://gmplib.org/. If a GMP source distribution is found in a subdirectory of your GCC sources named gmp, it will be built together with GCC. Alternatively, if GMP is already installed but it is not in your library search path, you will have to configure with the --with-gmp configure option. See also --with-gmp-lib and --with-gmp-include. The in-tree build is only supported with the GMP version that download_prerequisites installs.
Necessary to build GCC. It can be downloaded from https://www.mpfr.org. If an MPFR source distribution is found in a subdirectory of your GCC sources named mpfr, it will be built together with GCC. Alternatively, if MPFR is already installed but it is not in your default library search path, the --with-mpfr configure option should be used. See also --with-mpfr-lib and --with-mpfr-include. The in-tree build is only supported with the MPFR version that download_prerequisites installs.
Necessary to build GCC. It can be downloaded from https://www.multiprecision.org/mpc/. If an MPC source distribution is found in a subdirectory of your GCC sources named mpc, it will be built together with GCC. Alternatively, if MPC is already installed but it is not in your default library search path, the --with-mpc configure option should be used. See also --with-mpc-lib and --with-mpc-include. The in-tree build is only supported with the MPC version that download_prerequisites installs.
Necessary to build GCC with the Graphite loop optimizations. It can be downloaded from https://gcc.gnu.org/pub/gcc/infrastructure/. If an isl source distribution is found in a subdirectory of your GCC sources named isl, it will be built together with GCC. Alternatively, the --with-isl configure option should be used if isl is not installed in your default library search path.
Necessary to build GCC with zstd compression used for LTO bytecode. The library is searched in your default library patch search. Alternatively, the --with-zstd configure option should be used.
The complete list of Python3 modules broken down by GCC subcomponent is shown below:
gdb, gdb.printing, gdb.types,
os.path, re, sys and tempfile,
gcov, gzip, json, os and pytest.
Tests of SARIF output will use the check-jsonschema program from
the check-jsonschema module (if available) to validate generated
.sarif files.  If this tool is not found, the validation parts of those
tests are skipped.
csv, os, sys and time.
argparse, os, pathlib, shutil and
sys.
os and sys.
latex_elements, os, pygments, re,
sys and time.
Necessary to build GCC with internationalization support via --enable-nls. It can be downloaded from https://www.gnu.org/software/gettext/. If a GNU gettext distribution is found in a subdirectory of your GCC sources named gettext, it will be built together with GCC, unless present in the system (either in libc or as a stand-alone library).
The in-tree configuration requires GNU gettext version 0.22 or later.
Necessary when modifying configure.ac, aclocal.m4, etc. to regenerate configure and config.in files.
Necessary when modifying a Makefile.am file to regenerate its associated Makefile.in.
Much of GCC does not use automake, so directly edit the Makefile.in file. Specifically this applies to the gcc, intl, libcpp, libiberty, libobjc directories as well as any of their subdirectories.
For directories that use automake, GCC requires the latest release in the 1.15 series, which is currently 1.15.1. When regenerating a directory to a newer version, please update all the directories using an older 1.15 to the latest released version.
Needed to regenerate gcc.pot.
Necessary when modifying gperf input files, e.g.
gcc/cp/cfns.gperf to regenerate its associated header file, e.g.
gcc/cp/cfns.h.
Necessary to run the GCC testsuite; see the section on testing for details.
Necessary to regenerate fixinc/fixincl.x from fixinc/inclhack.def and fixinc/*.tpl.
Necessary to run ‘make check’ for fixinc.
Necessary to regenerate the top level Makefile.in file from Makefile.tpl and Makefile.def.
Necessary to regenerate the bits/version.h header for libstdc++.
Necessary when modifying *.l files.
Necessary to build GCC during development because the generated output files are not included in the version-controlled source repository. They are included in releases.
Necessary when modifying *.y files in the COBOL front end.
Necessary for running makeinfo when modifying *.texi
files to test your changes.
Necessary for running make dvi, make pdf,
or make html to create formatted documentation.  Texinfo version
4.8 or later is required for make pdf.
Necessary to build GCC documentation in info format during development because the generated output files are not included in the repository. (They are included in release tarballs.)
Note that the minimum requirement is for a very old version of Texinfo, but recent versions of Texinfo produce better-quality output, especially for HTML format. The version of Texinfo packaged with any current operating system distribution is likely to be adequate for building the documentation without error, but you may still want to install a newer release to get the best appearance and usability of the generated manuals.
Also note that Texinfo older than version 7.1 may throw incorrect build warnings, though the generated documentation is correct.
Necessary for running texi2dvi and texi2pdf, which
are used when running make dvi or make pdf to create
DVI or PDF files, respectively.
Necessary to regenerate jit/docs/_build/texinfo from the .rst files in the directories below jit/docs.
Necessary to access the source repository. Public releases and weekly snapshots of the development sources are also available via HTTPS.
Useful when submitting patches for the GCC source code.
Necessary when applying patches, created with diff, to one’s
own sources.
Copyright (C) Free Software Foundation, Inc. Verbatim copying and distribution of this entire article is permitted in any medium, provided this notice is preserved.
These pages are maintained by the GCC team. Last modified 2026-07-21.