---
archive_policy: text-only
attachments:
- filename: gcc-configure-options.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:4c1bbd16c144849b25a8c49130db00c75543fb54fa08e812dec37fd85c1cfa4b
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-0586015343b8
  position:
    end: 48608
    start: 48513
    type: TextPositionSelector
  quote_sha256: sha256:41eb97904c611aaf7fad37ed5275330229c39d1ed353f93ecebaaf5c195ac30b
  selector:
    exact: 'Specify that only a particular subset of compilers and

      their runtime libraries should be built.'
    prefix: 'e-languages=[^]lang1,[^]lang2,…

      '
    suffix: '  For a list of valid values for'
    type: TextQuoteSelector
  selector_sha256: sha256:9cb4c092fc4c959748b4ed7878f559ecac01e7736b3f5e1ea24e1b1f9aacb715
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-d0174128ad8a
  position:
    end: 20443
    start: 20320
    type: TextPositionSelector
  quote_sha256: sha256:b244e5093ac1a5bc2793a3625a6c20c69dd2a83df85e925377c356d1689c9b60
  selector:
    exact: Specify that multiple target libraries to support different target variants,
      calling conventions, etc. should not be built.
    prefix: 'ot be built.

      --disable-multilib

      '
    suffix: ' The default is to build a prede'
    type: TextQuoteSelector
  selector_sha256: sha256:ac81c9439f4dfdcb03f871ecb7b5dcd38f05e9a34247acbab24519ff4d66fecb
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-bd395148b2f9
  position:
    end: 63697
    start: 63347
    type: TextPositionSelector
  quote_sha256: sha256:9fae3ca331bed7bbad075da39c856c41cb892c3b69895d17ae66cd4efd194b7e
  selector:
    exact: 'If you want to build GCC but do not have the GMP library, the MPFR

      library and/or the MPC library installed in a standard location and

      do not have their sources present in the GCC source tree then you

      can explicitly specify the directory where they are installed

      (‘--with-gmp=gmpinstalldir’,

      ‘--with-mpfr=mpfrinstalldir’,

      ‘--with-mpc=mpcinstalldir’).'
    prefix: 'pathname--with-mpc-lib=pathname

      '
    suffix: '  The

      --with-gmp=gmpinstalldir o'
    type: TextQuoteSelector
  selector_sha256: sha256:29dbd27b8f58820a95fa413ec6f12101992c501c5d4b9775d022232f0e755eaf
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-b4d83f460536
  position:
    end: 6351
    start: 6258
    type: TextPositionSelector
  quote_sha256: sha256:0ad413f5897b3007ddf367cbd9c5189b25ffe3b2c001fb695b0c0da66b4a9e2a
  selector:
    exact: 'We highly recommend against dirname being the same or a

      subdirectory of objdir or vice versa.'
    prefix: 'rectory defaults to /usr/local.

      '
    suffix: '  If specifying a directory

      bene'
    type: TextQuoteSelector
  selector_sha256: sha256:2556f7c06f9f7530e04f2445d30f93d8d901b88c9f7c064b0501895bd043bf62
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-052a9cc37b85
  position:
    end: 48607
    start: 48474
    type: TextPositionSelector
  quote_sha256: sha256:db3c40807ad5717641c1890b1e49df0384d8cf4b20985fd4a8a69df517307a4a
  selector:
    exact: '--enable-languages=[^]lang1,[^]lang2,…

      Specify that only a particular subset of compilers and

      their runtime libraries should be built'
    prefix: 'havior --with-aix-soname=‘aix’.

      '
    suffix: .  For a list of valid values fo
    type: TextQuoteSelector
  selector_sha256: sha256:7ca859fcdf92c290384883fcc6a1600e906f25e4c3918d1bc7f95f9bf14a826f
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-fb605de0897a
  position:
    end: 20442
    start: 20301
    type: TextPositionSelector
  quote_sha256: sha256:3dadfae89cf55ea0a9f71264140c4fce27be5475211082b6d34f0f7c3ce166ef
  selector:
    exact: '--disable-multilib

      Specify that multiple target libraries to support different target variants,
      calling conventions, etc. should not be built'
    prefix: 'host tools should not be built.

      '
    suffix: . The default is to build a pred
    type: TextQuoteSelector
  selector_sha256: sha256:41b2936c414ba0775b120d5946ae7f04db2164b64432fe3fe2a31f8cbbc704f6
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
- evidence_id: evidence-1ddd3b797392
  position:
    end: 6350
    start: 6046
    type: TextPositionSelector
  quote_sha256: sha256:1f692d6152b06bf60873884e94a40c6077d26ab1168b19d7422c25f9a88491a3
  selector:
    exact: '--prefix=dirname

      Specify the toplevel installation directory. This is the recommended way to
      install the tools into a directory other than the default. The toplevel installation
      directory defaults to /usr/local.

      We highly recommend against dirname being the same or a

      subdirectory of objdir or vice versa'
    prefix: 'corresponding --without option.

      '
    suffix: '.  If specifying a directory

      ben'
    type: TextQuoteSelector
  selector_sha256: sha256:238d7ea632b70a8c18627cfef5d286d3557760f076a2a136d3a51582c2ed3e70
  snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
extractor: trafilatura/2.2.0
id: gcc-configure-options
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/4c1bbd16c144849b25a8c49130db00c75543fb54fa08e812dec37fd85c1cfa4b.html
  sha256: sha256:4c1bbd16c144849b25a8c49130db00c75543fb54fa08e812dec37fd85c1cfa4b
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://gcc.gnu.org/install/configure.html
  url: https://gcc.gnu.org/install/configure.html
schema_version: source/v1
snapshot_sha256: sha256:a4573e801a544775767608a700ae244d6d2a0a7008ca09d02a4a5e1893d6b5d8
source_type: doc
vault_id: public
---
Like most GNU software, GCC must be configured before it can be built. This document describes the recommended configuration procedure for both native and cross targets.
We use srcdir to refer to the toplevel source directory for GCC; we use objdir to refer to the toplevel build/object directory.
If you obtained the sources by cloning the repository, srcdir must refer to the top gcc directory, the one where the MAINTAINERS file can be found, and not its gcc subdirectory, otherwise the build will fail.
If either srcdir or objdir is located on an automounted NFS
file system, the shell’s built-in pwd command will return
temporary pathnames.  Using these can lead to various sorts of build
problems.  To avoid this issue, set the PWDCMD environment
variable to an automounter-aware pwd command, e.g.,
pawd or ‘amq -w’, during the configuration and build
phases.
First, we highly recommend that GCC be built into a separate directory from the sources which does not reside within the source tree. This is how we generally build GCC; building where objdir is a subdirectory of srcdir should work as well; building where objdir == srcdir is unsupported.
If you have previously built GCC in the same directory for a different target machine, do ‘make distclean’ to delete all files that might be invalid. One of the files this deletes is Makefile; if ‘make distclean’ complains that Makefile does not exist or issues a message like “don’t know how to make distclean” it probably means that the directory is already suitably clean. However, with the recommended method of building in a separate objdir, you should simply use a different objdir for each target.
Second, when configuring a native system, either cc or
gcc must be in your path or you must set CC in
your environment before running configure.  Otherwise the configuration
scripts may fail.
To configure GCC:
% mkdir objdir
% cd objdir
% srcdir/configure [options] [target]
If you will be distributing binary versions of GCC, with modifications to the source code, you should use the options described in this section to make clear that your version contains modifications.
--with-pkgversion=version
Specify a string that identifies your package.  You may wish
to include a build number or build date.  This version string will be
included in the output of gcc --version.  This suffix does
not replace the default version string, only the ‘GCC’ part.
The default value is ‘GCC’.
--with-bugurl=url
Specify the URL that users should visit if they wish to report a bug. You are of course welcome to forward bugs reported to you to the FSF, if you determine that they are not bugs in your modifications.
The default value refers to the FSF’s GCC bug tracker.
--with-documentation-root-url=url
Specify the URL root that contains GCC option documentation.  The url
should end with a / character.
The default value is https://gcc.gnu.org/onlinedocs/
on the GCC main development trunk.  On release branches, the default
is https://gcc.gnu.org/onlinedocs/gcc-major.minor.0/.
--with-changes-root-url=url
Specify the URL root that contains information about changes in GCC
releases like gcc-version/changes.html.
The url should end with a / character.
The default value is https://gcc.gnu.org/.
Specify the host, build and target machine configurations. You do this when you run the configure script.
The build machine is the system which you are using, the host machine is the system where you want to run the resulting compiler (normally the build machine), and the target machine is the system for which you want the compiler to generate code.
If you are building a compiler to produce code for the machine it runs on (a native compiler), you normally do not need to specify any operands to configure; it will try to guess the type of machine you are on and use that as the build, host and target machines. So you don’t need to specify a configuration when building a native compiler unless configure cannot figure out what your configuration is or guesses wrong.
In those cases, specify the build machine’s configuration name with the --host option; the host and target will default to be the same as the host machine.
Here is an example:
./configure --host=x86_64-pc-linux-gnu
A configuration name may be canonical or it may be more or less abbreviated (config.sub script produces canonical versions).
A canonical configuration name has three parts, separated by dashes. It looks like this: ‘cpu-company-system’.
Here are the possible CPU types:
aarch64, aarch64_be, alpha, alpha64, amdgcn, arc, arceb, arm, armeb, avr, bfin, bpf, cris, csky, epiphany, fido, fr30, frv, ft32, h8300, hppa, hppa2.0, hppa64, i486, i686, ia64, iq2000, lm32, loongarch64, m32r, m32rle, m68k, mcore, microblaze, microblazeel, mips, mips64, mips64el, mips64octeon, mips64orion, mips64vr, mipsel, mipsisa32, mipsisa32r2, mipsisa64, mipsisa64r2, mipsisa64r2el, mipsisa64sb1, mipsisa64sr71k, mipstx39, mmix, mn10300, moxie, msp430, nds32be, nds32le, nvptx, or1k, pdp11, powerpc, powerpc64, powerpc64le, powerpcle, pru, riscv32, riscv32be, riscv64, riscv64be, rl78, rx, s390x, sh, shle, sparc, sparc64, tic6x, v850, v850e, v850e1, vax, visium, x86_64, xstormy16, xtensa
Here is a list of system types:
aixversion, amdhsa, aout, cygwin, darwinversion, eabi, eabialtivec, eabisim, eabisimaltivec, elf, elf32, elfbare, elfoabi, freebsdversion, gnu, hpux, hpuxversion, kfreebsd-gnu, kopensolaris-gnu, linux-androideabi, linux-gnu, linux-gnu_altivec, linux-musl, linux-uclibc, lynxos, mingw32, mingw32crt, mmixware, msdosdjgpp, netbsd, netbsdelfversion, nto-qnx, openbsd, rtems, solarisversion, symbianelf, tpf, uclinux, uclinux_eabi, vms, vxworks, vxworksae, vxworksmils
Use options to override several configure time options for GCC. A list of supported options follows; ‘configure --help’ may list other options, but those not listed below may not work and should not normally be used.
Note that each --enable option has a corresponding --disable option and that each --with option has a corresponding --without option.
--prefix=dirname
Specify the toplevel installation directory. This is the recommended way to install the tools into a directory other than the default. The toplevel installation directory defaults to /usr/local.
We highly recommend against dirname being the same or a
subdirectory of objdir or vice versa.  If specifying a directory
beneath a user’s home directory tree, some shells will not expand
dirname correctly if it contains the ‘~’ metacharacter; use
$HOME instead.
The following standard autoconf options are supported.  Normally you
should not need to use these options.
--exec-prefix=dirname
Specify the toplevel installation directory for architecture-dependent files. The default is prefix.
--bindir=dirname
Specify the installation directory for the executables called by users
(such as gcc and g++).  The default is
exec-prefix/bin.
--libdir=dirname
Specify the installation directory for object code libraries and internal data files of GCC. The default is exec-prefix/lib.
--libexecdir=dirname
Specify the installation directory for internal executables of GCC. The default is exec-prefix/libexec.
--with-slibdir=dirname
Specify the installation directory for the shared libgcc library. The default is libdir.
--datarootdir=dirname
Specify the root of the directory tree for read-only architecture-independent data files referenced by GCC. The default is prefix/share.
--infodir=dirname
Specify the installation directory for documentation in info format. The default is datarootdir/info.
--datadir=dirname
Specify the installation directory for some architecture-independent data files referenced by GCC. The default is datarootdir.
--docdir=dirname
Specify the installation directory for documentation files (other than Info) for GCC. The default is datarootdir/doc.
--htmldir=dirname
Specify the installation directory for HTML documentation files. The default is docdir.
--pdfdir=dirname
Specify the installation directory for PDF documentation files. The default is docdir.
--mandir=dirname
Specify the installation directory for manual pages. The default is datarootdir/man. (Note that the manual pages are only extracts from the full GCC manuals, which are provided in Texinfo format. The manpages are derived by an automatic conversion process from parts of the full manual.)
--with-gxx-include-dir=dirname
Specify the installation directory for G++ header files. The default depends on other configuration options, and differs between cross and native configurations.
--with-specs=specs
Specify additional command line driver SPECS. This can be useful if you need to turn on a non-standard feature by default without modifying the compiler’s source code, for instance --with-specs=%{!fcommon:%{!fno-common:-fno-common}}. See “Spec Files” in the GCC Internals manual.
--program-prefix=prefix
GCC supports some transformations of the names of its programs when installing them. This option prepends prefix to the names of programs to install in bindir (see above). For example, specifying --program-prefix=foo- would result in ‘gcc’ being installed as /usr/local/bin/foo-gcc.
--program-suffix=suffix
Appends suffix to the names of programs to install in bindir (see above). For example, specifying --program-suffix=-3.1 would result in ‘gcc’ being installed as /usr/local/bin/gcc-3.1.
--program-transform-name=pattern
Applies the ‘sed’ script pattern to be applied to the names of programs to install in bindir (see above). pattern has to consist of one or more basic ‘sed’ editing commands, separated by semicolons. For example, if you want the ‘gcc’ program name to be transformed to the installed program /usr/local/bin/myowngcc and the ‘g++’ program name to be transformed to /usr/local/bin/gspecial++ without changing other program names, you could use the pattern --program-transform-name='s/^gcc$/myowngcc/; s/^g++$/gspecial++/' to achieve this effect.
All three options can be combined and used together, resulting in more complex conversion patterns. As a basic rule, prefix (and suffix) are prepended (appended) before further transformations can happen with a special transformation script pattern.
As currently implemented, this option only takes effect for native builds; cross compiler binaries’ names are not transformed even when a transformation is explicitly asked for by one of these options.
For native builds, some of the installed programs are also installed with the target alias in front of their name, as in ‘i686-pc-linux-gnu-gcc’. All of the above transformations happen before the target alias is prepended to the name—so, specifying --program-prefix=foo- and program-suffix=-3.1, the resulting binary would be installed as /usr/local/bin/i686-pc-linux-gnu-foo-gcc-3.1.
As a last shortcoming, none of the installed Ada programs are transformed yet, which will be fixed in some time.
--with-local-prefix=dirname
Specify the installation directory for local include files. The default is /usr/local. Specify this option if you want the compiler to search directory dirname/include for locally installed header files instead of /usr/local/include.
You should specify --with-local-prefix only if your site has a different convention (not /usr/local) for where to put site-specific files.
The default value for --with-local-prefix is /usr/local regardless of the value of --prefix. Specifying --prefix has no effect on which directory GCC searches for local header files. This may seem counterintuitive, but actually it is logical.
The purpose of --prefix is to specify where to install GCC. The local header files in /usr/local/include—if you put any in that directory—are not part of GCC. They are part of other programs—perhaps many others. (GCC installs its own header files in another directory which is based on the --prefix value.)
Both the local-prefix include directory and the GCC-prefix include directory are part of GCC’s “system include” directories. Although these two directories are not fixed, they need to be searched in the proper order for the correct processing of the include_next directive. The local-prefix include directory is searched before the GCC-prefix include directory. Another characteristic of system include directories is that pedantic warnings are turned off for headers in these directories.
Some autoconf macros add -I directory options to the compiler command line, to ensure that directories containing installed packages’ headers are searched. When directory is one of GCC’s system include directories, GCC will ignore the option so that system directories continue to be processed in the correct order. This may result in a search order different from what was specified but the directory will still be searched.
GCC automatically searches for ordinary libraries using
GCC_EXEC_PREFIX.  Thus, when the same installation prefix is
used for both GCC and packages, GCC will automatically search for
both headers and libraries.  This provides a configuration that is
easy to use.  GCC behaves in a manner similar to that when it is
installed as a system compiler in /usr.
Sites that need to install multiple versions of GCC may not want to
use the above simple configuration.  It is possible to use the
--program-prefix, --program-suffix and
--program-transform-name options to install multiple versions
into a single directory, but it may be simpler to use different prefixes
and the --with-local-prefix option to specify the location of the
site-specific files for each version.  It will then be necessary for
users to specify explicitly the location of local site libraries
(e.g., with LIBRARY_PATH).
The same value can be used for both --with-local-prefix and --prefix provided it is not /usr. This can be used to avoid the default search of /usr/local/include.
Do not specify /usr as the --with-local-prefix!
The directory you use for --with-local-prefix must not
contain any of the system’s standard header files.  If it did contain
them, certain programs would be miscompiled (including GNU Emacs, on
certain targets), because this would override and nullify the header
file corrections made by the fixincludes script.
Indications are that people who use this option use it based on mistaken ideas of what it is for. People use it as if it specified where to install part of GCC. Perhaps they make this assumption because installing GCC creates the directory.
--with-gcc-major-version-only
Specifies that GCC should use only the major number rather than major.minor.patchlevel in filesystem paths.
--with-native-system-header-dir=dirname
Specifies that dirname is the directory that contains native system header files, rather than /usr/include. This option is most useful if you are creating a compiler that should be isolated from the system as much as possible. It is most commonly used with the --with-sysroot option and will cause GCC to search dirname inside the system root specified by that option.
--enable-shared[=package[,…]]
Build shared versions of libraries, if shared libraries are supported on the target platform. Unlike GCC 2.95.x and earlier, shared libraries are enabled by default on all platforms that support shared libraries.
If a list of packages is given as an argument, build shared libraries only for the listed packages. For other packages, only static libraries will be built. Package names currently recognized in the GCC tree are ‘libgcc’ (also known as ‘gcc’), ‘libstdc++’ (not ‘libstdc++-v3’), ‘libffi’, ‘zlib’, ‘boehm-gc’, ‘ada’, ‘libada’, ‘libgo’, ‘libobjc’, and ‘libphobos’. Note ‘libiberty’ does not support shared libraries at all.
Use --disable-shared to build only static libraries. Note that --disable-shared does not accept a list of package names as argument, only --enable-shared does.
Contrast with --enable-host-shared, which affects host code.
--enable-host-shared
Specify that the host code should be built into position-independent machine code (with -fPIC), allowing it to be used within shared libraries, but yielding a slightly slower compiler.
This option is required when building the libgccjit.so library.
Contrast with --enable-shared, which affects target libraries.
--enable-versioned-jit
Specify that the ‘libgccjit’ library is built with a soname matching the GCC major version.
--enable-host-pie
Specify that the host executables should be built into position-independent executables (with -fPIE and -pie), yielding a slightly slower compiler (but faster than --enable-host-shared). Position-independent executables are loaded at random addresses each time they are executed, therefore provide additional protection against Return Oriented Programming (ROP) attacks.
--enable-host-pie may be used with --enable-host-shared, in which case -fPIC is used when compiling, and -pie when linking.
--enable-host-bind-now
Specify that the host executables should be linked with the option -Wl,-z,now, which means that the dynamic linker will resolve all symbols when the executables are started, and that in turn allows RELRO to mark the GOT read-only, resulting in better security.
--with-as=pathname
Specify that the compiler should use the assembler pointed to by pathname, rather than the one found by the standard rules to find an assembler, which are:
PATH for a tool whose name is prefixed by the
target system triple.
You may want to use --with-as if no assembler is installed in the directories listed above, or if you have multiple assemblers installed and want to choose one that is not found by the above rules.
--with-ld=pathname
Same as --with-as but for the linker.
--with-dsymutil=pathname
Same as --with-as but for the debug linker (only used on Darwin platforms so far).
--with-windres=pathname
Same as --with-as but for the Windows resource compiler.
--with-tls=dialect
Specify the default TLS dialect, for systems where there is a choice.
For ARM targets, possible values for dialect are gnu or
gnu2, which select between the original GNU dialect and the GNU TLS
descriptor-based dialect.
For RISC-V targets, possible values for dialect are trad or
desc, which select between the traditional GNU dialect and the GNU TLS
descriptor-based dialect.
For i386, x86-64 targets, possible values for dialect are gnu or
gnu2, which select between the original GNU dialect and the GNU TLS
descriptor-based dialect.
--enable-multiarch
Specify whether to enable or disable multiarch support. The default is to check for glibc start files in a multiarch location, and enable it if the files are found. The auto detection is enabled for native builds, and for cross builds configured with --with-sysroot, and without --with-native-system-header-dir. More documentation about multiarch can be found at https://wiki.debian.org/Multiarch.
--enable-sjlj-exceptions
Force use of the setjmp/longjmp-based scheme for exceptions.
‘configure’ ordinarily picks the correct value based on the platform.
Only use this option if you are sure you need a different setting.
--enable-vtable-verify
Specify whether to enable or disable the vtable verification feature. Enabling this feature causes libstdc++ to be built with its virtual calls in verifiable mode. This means that, when linked with libvtv, every virtual call in libstdc++ will verify the vtable pointer through which the call will be made before actually making the call. If not linked with libvtv, the verifier will call stub functions (in libstdc++ itself) and do nothing. If vtable verification is disabled, then libstdc++ is not built with its virtual calls in verifiable mode at all. However the libvtv library will still be built (see --disable-libvtv to turn off building libvtv). --disable-vtable-verify is the default.
--enable-libgdiagnostics
Specify whether to build libgdiagnostics, a shared library exposing
GCC’s diagnostics capabilities via a C API, and a C++ wrapper API adding
“syntactic sugar”.
This option requires --enable-host-shared on non-Windows hosts.
This option also enables sarif-replay, a command-line tool for
viewing SARIF files.
sarif-replay takes one or more .sarif files as input and
attempts to replay any diagnostics within them to stderr (via
libgdiagnostics) in the style of GCC’s diagnostics.
--disable-gcov
Specify that the run-time library used for coverage analysis and associated host tools should not be built.
--disable-multilib
Specify that multiple target libraries to support different target variants, calling conventions, etc. should not be built. The default is to build a predefined set of them.
Some targets provide finer-grained control over which multilibs are built (e.g., --disable-softfloat):
arm-*-*
fpu, 26bit, underscore, interwork, biendian, nofmult.
m68*-*-*
softfloat, m68881, m68000, m68020.
mips*-*-*
single-float, biendian, softfloat.
msp430-*-*
no-exceptions
powerpc*-*-*, rs6000*-*-*
aix64, pthread, softfloat, powercpu, powerpccpu, powerpcos, biendian, sysv, aix.
--with-multilib-list=list--without-multilib-list
Specify what multilibs to build. list is a comma separated list of values, possibly consisting of a single value. Currently only implemented for aarch64*-*-*, amdgcn*-*-*, arm*-*-*, loongarch*-*-*, nvptx-*, riscv*-*-*, sh*-*-* and x86-64-*-linux*. The accepted values and meaning for each target is given below.
aarch64*-*-*
list is a comma separated list of ilp32, and lp64
to enable ILP32 and LP64 run-time libraries, respectively.  If
list is empty, then there will be no multilibs and only the
default run-time library will be built.  If list is
default or –with-multilib-list= is not specified, then the
default set of libraries is selected based on the value of
--target.
amdgcn*-*-*
list is a comma separated list of ISA names (allowed values:
gfx900, gfx902, gfx904, gfx906, gfx908,
gfx909, gfx90a, gfx90c, gfx942, gfx950,
gfx9-generic, gfx9-4-generic, gfx1030, gfx1031,
gfx1032, gfx1033, gfx1034, gfx1035, gfx1036,
gfx10-3-generic, gfx1100, gfx1101, gfx1102,
gfx1103, gfx1150, gfx1151, gfx1152, gfx1153,
gfx11-generic).  It ought not include the name of the default
ISA, specified via --with-arch.  If list is empty, then there
will be no multilibs and only the default run-time library will be built.  If
list is default or --with-multilib-list= is not
specified, then the default set of libraries is selected.
arm*-*-*
list is a comma separated list of aprofile and
rmprofile to build multilibs for A or R and M architecture
profiles respectively.  Note that, due to some limitation of the current
multilib framework, using the combined aprofile,rmprofile
multilibs selects in some cases a less optimal multilib than when using
the multilib profile for the architecture targeted.  The special value
default is also accepted and is equivalent to omitting the
option, i.e., only the default run-time library will be enabled.
list may instead contain @name, to use the multilib
configuration Makefile fragment name in gcc/config/arm in
the source tree (it is part of the corresponding sources, after all).
It is recommended, but not required, that files used for this purpose to
be named starting with t-ml-, to make their intended purpose
self-evident, in line with GCC conventions.  Such files enable custom,
user-chosen multilib lists to be configured.  Whether multiple such
files can be used together depends on the contents of the supplied
files.  See gcc/config/arm/t-multilib and its supplementary
gcc/config/arm/t-*profile files for an example of what such
Makefile fragments might look like for this version of GCC.  The macros
expected to be defined in these fragments are not stable across GCC
releases, so make sure they define the MULTILIB-related macros
expected by the version of GCC you are building.
See “Target Makefile Fragments” in the internals manual.
The table below gives the combination of ISAs, architectures, FPUs and
floating-point ABIs for which multilibs are built for each predefined
profile.  The union of these options is considered when specifying both
aprofile and rmprofile.
loongarch*-*-*
list is a comma-separated list, with each of the element starting with
the following ABI identifiers: lp64d[/base] lp64f[/base]
lp64d[/base] (the /base suffix may be omitted)
to enable their respective run-time libraries.
A suffix [/arch][/option/…] may follow immediately
after the ABI identifier to customize the compiler options for building the
given set of libraries.  arch denotes the architecture name recognized
by the -march=arch compiler option, which acts as a basic target
ISA configuration that can be adjusted using the subsequent option
suffixes, where each option is a compiler option without a leading dash
(’-’).
If no such suffix is present for a given multilib variant, the configured value of --with-multilib-default is appended as a default suffix. If --with-multilib-default is not given, the default build option -march=abi-default is applied when building the variants without a suffix.
As a special case, fixed may be used in the position of arch,
which means using the architecture configured with
--with-arch=arch, or its default value (e.g. loongarch64
for loongarch64-* targets).
If list is empty or default, or if --with-multilib-list
is not specified, then only the default variant of the libraries are built,
where the default ABI is implied by the configured target triplet.
nvptx-*
The target libraries corresponding to the default value of the -march option are always built, see host/target specific installation notes. If list is empty, ‘no’, or --without-multilib-list is specified, then no additional multilibs are built. Otherwise, list is a comma separated list specifying which multilibs to build. List items are either ‘sm_SM’, or ‘default’, which is a placeholder specifying a default set of multilibs: ‘sm_52’. Any duplicates are filtered out. If --with-multilib-list is not specified, then --with-multilib-list=default is assumed. For ‘sm_30’, ‘sm_35’ target libraries, -mptx-3.1 sub-variants are additionally built.
riscv*-*-*
list is a single ABI name.  The target architecture must be either
rv32gc or rv64gc.  This will build a single multilib for the
specified architecture and ABI pair.  If --with-multilib-list is not
given, then a default set of multilibs is selected based on the value of
--target.  This is usually a large set of multilibs.
sh*-*-*
list is a comma separated list of CPU names.  These must be of the
form sh* or m* (in which case they match the compiler option
for that processor).  The list should not contain any endian options -
these are handled by --with-endian.
If list is empty, then there will be no multilibs for extra processors. The multilib for the secondary endian remains enabled.
As a special case, if an entry in the list starts with a !
(exclamation point), then it is added to the list of excluded multilibs.
Entries of this sort should be compatible with ‘MULTILIB_EXCLUDES’
(once the leading ! has been stripped).
If --with-multilib-list is not given, then a default set of multilibs is selected based on the value of --target. This is usually the complete set of libraries, but some targets imply a more specialized subset.
Example 1: to configure a compiler for SH4A only, but supporting both endians, with little endian being the default:
--with-cpu=sh4a --with-endian=little,big --with-multilib-list=
Example 2: to configure a compiler for both SH4A and SH4AL-DSP, but with only little endian SH4AL:
--with-cpu=sh4a --with-endian=little,big \
--with-multilib-list=sh4al,!mb/m4al
x86-64-*-linux*
list is a comma separated list of m32, m64 and
mx32 to enable 32-bit, 64-bit and x32 run-time libraries,
respectively.  If list is empty, then there will be no multilibs
and only the default run-time library will be enabled.
If --with-multilib-list is not given, then only 32-bit and 64-bit run-time libraries will be enabled.
--with-multilib-default
On LoongArch targets, set the default build options for enabled multilibs
without build options appended to their corresponding
--with-multilib-list items.  The format of this value is
[/arch][/option/…], where arch is an
architecture name recognized by -march=arch compiler option,
and subsequent option suffixes are compiler options minus a leading
dash (’-’).
Multiple options may appear consecutively while arch may only appear in the beginning or be omitted (which means -march=abi-default is applied when building the libraries).
--with-strict-align-lib
On LoongArch targets, build all enabled multilibs with -mstrict-align (Not enabled by default).
--with-multilib-generator=config
Specify what multilibs to build. config is a semicolon separated list of values, possibly consisting of a single value. Currently only implemented for riscv*-*-elf*. The accepted values and meanings are given below.
Every config is constructed with four mandatory components and one optional component: architecture string, ABI, reuse rule with architecture string, reuse rule with sub-extension and an optional list of extra options.
Example 1: Add multi-lib support for rv32i with ilp32.
rv32i-ilp32--
Example 2: Add multi-lib support for rv32i with ilp32 and rv32imafd with ilp32.
rv32i-ilp32--;rv32imafd-ilp32--
Example 3: Add multi-lib support for rv32i with ilp32; rv32im with ilp32 and rv32ic with ilp32 will reuse this multi-lib set.
rv32i-ilp32-rv32im-c
Example 4: Add multi-lib support for rv64ima with lp64; rv64imaf with lp64, rv64imac with lp64 and rv64imafc with lp64 will reuse this multi-lib set.
rv64ima-lp64--f,c,fc
--with-multilib-generator have an optional configuration argument --cmodel=val for code model, this option will expand with other config options, val is a comma separated list of possible code model, currently we support medlow and medany.
Example 5: Add multi-lib support for rv64ima with lp64; rv64ima with lp64 and medlow code model
rv64ima-lp64--;--cmodel=medlow
Example 6: Add multi-lib support for rv64ima with lp64; rv64ima with lp64 and medlow code model; rv64ima with lp64 and medany code model
rv64ima-lp64--;--cmodel=medlow,medany
A config may carry an optional fifth component, a list of extra options, which is appended after the sub-extension reuse rule:
<arch>-<abi>-<extra-arch>-<sub-ext>[-<extra-options>]
The extra options are a comma separated list, and each entry pairs an option name with the multilib directory it should map to, separated by a slash:
<extra-options> := <extra-option> ',' <extra-options>
                 | <extra-option>
<extra-option>  := <option> '/' <multilib-folder>
Because the dash (‘-’) is used as the component separator, any dash in an
option name must be rewritten as an underscore (‘_’), and the leading dash
of the option must be dropped.  For example, -fcf-protection=full is
written as fcf_protection=full.
Example 7: Add multi-lib support for rv64imafdc with lp64d, plus a variant built with -fcf-protection=full placed in the cfi directory.
rv64imafdc_zicfiss_zicfilp-lp64d---fcf_protection=full/cfi
This builds a multilib with -march=rv64imafdc_zicfiss_zicfilp -mabi=lp64d -fcf-protection=full and uses rv64imafdc_zicfiss_zicfilp/lp64d/cfi as the multilib folder.
--with-multi-buildlist=file
Specify a file containing a list of multilib directories to build.
Each line in the file should contain a single multilib directory name,
as printed by gcc --print-multi-lib.  Only the listed directories
will be built and installed.
This option is useful for reducing build time and binary size by excluding unnecessary multilib variants. It is especially beneficial for embedded targets or vendor-specific toolchains.
Example file contents:
mips-r6-hard/lib
mips-r6-soft/lib32
mipsel-r6-hard/lib64
This option is target-independent and can be used with any architecture that supports multilibs. It is passed to both host and target configuration stages and used during fixed includes installation and multilib directory generation.
--with-endian=endians
Specify what endians to use. Currently only implemented for sh*-*-*.
endians may be one of the following:
big
Use big endian exclusively.
little
Use little endian exclusively.
big,little
Use big endian by default. Provide a multilib for little endian.
little,big
Use little endian by default. Provide a multilib for big endian.
--with-cmodel=cmodel
Specify what code model to use by default. Currently only implemented for loongarch*-*-* and riscv*-*-*.
--enable-threads
Specify that the target supports threads. This affects the Objective-C compiler and runtime library, and exception handling for other languages like C++. On some systems, this is the default.
In general, the best (and, in many cases, the only known) threading model available will be configured for use. Beware that on some systems, GCC has not been taught what threading models are generally available for the system. In this case, --enable-threads is an alias for --enable-threads=single.
--disable-threads
Specify that threading support should be disabled for the system. This is an alias for --enable-threads=single.
--enable-threads=lib
Specify that lib is the thread support library. This affects the Objective-C compiler and runtime library, and exception handling for other languages like C++. The possibilities for lib are:
aix
AIX thread support.
dce
DCE thread support.
lynx
LynxOS thread support.
mipssde
MIPS SDE thread support.
no
This is an alias for ‘single’.
posix
Generic POSIX/Unix98 thread support.
rtems
RTEMS thread support.
single
Disable thread support, should work for all platforms.
tpf
TPF thread support.
vxworks
VxWorks thread support.
win32
Microsoft Win32 API thread support.
--enable-tls
Specify that the target supports TLS (Thread Local Storage). Usually configure can correctly determine if TLS is supported. In cases where it guesses incorrectly, TLS can be explicitly enabled or disabled with --enable-tls or --disable-tls. This can happen if the assembler supports TLS but the C library does not, or if the assumptions made by the configure test are incorrect.
--disable-tls
Specify that the target does not support TLS. This is an alias for --enable-tls=no.
--disable-tm-clone-registry
Disable TM clone registry in libgcc. It is enabled in libgcc by default. This option helps to reduce code size for embedded targets which do not use transactional memory.
--with-cpu=cpu--with-cpu-32=cpu--with-cpu-64=cpu
Specify which CPU variant the compiler should generate code for by default. cpu will be used as the default value of the -mcpu= switch. This option is only supported on some targets, including ARC, ARM, i386, M68k, PowerPC, RISC-V, and SPARC. It is mandatory for ARC. The --with-cpu-32 and --with-cpu-64 options specify separate default CPUs for 32-bit and 64-bit modes; these options are only supported for aarch64, i386, x86-64, PowerPC, and SPARC.
--with-schedule=cpu--with-arch=cpu--with-arch-32=cpu--with-arch-64=cpu--with-tune=cpu--with-tune-32=cpu--with-tune-64=cpu--with-abi=abi--with-fpu=type--with-float=type--with-simd=type
These configure options provide default values for the -mschedule=, -march=, -mtune=, -mabi=, and -mfpu= options and for -mhard-float or -msoft-float. As with --with-cpu, which switches will be accepted and acceptable values of the arguments depend on the target.
--with-mode=mode
Specify if the compiler should default to -marm or -mthumb. This option is only supported on ARM targets.
--with-stack-offset=num
This option sets the default for the -mstack-offset=num option, and will thus generally also control the setting of this option for libraries. This option is only supported on Epiphany targets.
--with-fpmath=isa
This options sets -mfpmath=sse by default and specifies the default ISA for floating-point arithmetic. You can select either ‘sse’ which enables -msse2 or ‘avx’ which enables -mavx by default. This option is only supported on i386 and x86-64 targets.
--with-fp-32=mode
On MIPS targets, set the default value for the -mfp option when using the o32 ABI. The possibilities for mode are:
32
Use the o32 FP32 ABI extension, as with the -mfp32 command-line option.
xx
Use the o32 FPXX ABI extension, as with the -mfpxx command-line option.
64
Use the o32 FP64 ABI extension, as with the -mfp64 command-line option.
In the absence of this configuration option the default is to use the o32 FP32 ABI extension.
--with-odd-spreg-32
On MIPS targets, set the -modd-spreg option by default when using the o32 ABI.
--without-odd-spreg-32
On MIPS targets, set the -mno-odd-spreg option by default when using the o32 ABI. This is normally used in conjunction with --with-fp-32=64 in order to target the o32 FP64A ABI extension.
--with-nan=encoding
On MIPS targets, set the default encoding convention to use for the special not-a-number (NaN) IEEE 754 floating-point data. The possibilities for encoding are:
legacy
Use the legacy encoding, as with the -mnan=legacy command-line option.
2008
Use the 754-2008 encoding, as with the -mnan=2008 command-line option.
To use this configuration option you must have an assembler version installed that supports the -mnan= command-line option too. In the absence of this configuration option the default convention is the legacy encoding, as when neither of the -mnan=2008 and -mnan=legacy command-line options has been used.
--with-divide=type
Specify how the compiler should generate code for checking for division by zero. This option is only supported on the MIPS target. The possibilities for type are:
traps
Division by zero checks use conditional traps (this is the default on systems that support conditional traps).
breaks
Division by zero checks use the break instruction.
--with-compact-branches=policy
Specify how the compiler should generate branch instructions. This option is only supported on the MIPS target. The possibilities for type are:
optimal
Cause a delay slot branch to be used if one is available in the current ISA and the delay slot is successfully filled. If the delay slot is not filled, a compact branch will be chosen if one is available.
never
Ensures that compact branch instructions will never be generated.
always
Ensures that a compact branch instruction will be generated if available. If a compact branch instruction is not available, a delay slot form of the branch will be used instead. This option is supported from MIPS Release 6 onwards. For pre-R6/microMIPS/MIPS16, this option is just same as never/optimal.
--with-llsc
On MIPS targets, make -mllsc the default when no -mno-llsc option is passed. This is the default for Linux-based targets, as the kernel will emulate them if the ISA does not provide them.
--without-llsc
On MIPS targets, make -mno-llsc the default when no -mllsc option is passed.
--with-synci
On MIPS targets, make -msynci the default when no -mno-synci option is passed.
--without-synci
On MIPS targets, make -mno-synci the default when no -msynci option is passed. This is the default.
--with-lxc1-sxc1
On MIPS targets, make -mlxc1-sxc1 the default when no -mno-lxc1-sxc1 option is passed. This is the default.
--without-lxc1-sxc1
On MIPS targets, make -mno-lxc1-sxc1 the default when no
-mlxc1-sxc1 option is passed.  The indexed load/store
instructions are not directly a problem but can lead to unexpected
behavior when deployed in an application intended for a 32-bit address
space but run on a 64-bit processor.  The issue is seen because all
known MIPS 64-bit Linux kernels execute o32 and n32 applications
with 64-bit addressing enabled which affects the overflow behavior
of the indexed addressing mode.  GCC will assume that ordinary
32-bit arithmetic overflow behavior is the same whether performed
as an addu instruction or as part of the address calculation
in lwxc1 type instructions.  This assumption holds true in a
pure 32-bit environment and can hold true in a 64-bit environment if
the address space is accurately set to be 32-bit for o32 and n32.
--with-madd4
On MIPS targets, make -mmadd4 the default when no -mno-madd4 option is passed. This is the default.
--without-madd4
On MIPS targets, make -mno-madd4 the default when no
-mmadd4 option is passed.  The madd4 instruction
family can be problematic when targeting a combination of cores that
implement these instructions differently.  There are two known cores
that implement these as fused operations instead of unfused (where
unfused is normally expected).  Disabling these instructions is the
only way to ensure compatible code is generated; this will incur
a performance penalty.
--with-msa
On MIPS targets, make -mmsa the default when no -mno-msa option is passed.
--without-msa
On MIPS targets, make -mno-msa the default when no -mmsa option is passed. This is the default.
--with-mips-plt
On MIPS targets, make use of copy relocations and PLTs. These features are extensions to the traditional SVR4-based MIPS ABIs and require support from GNU Binutils and the runtime C library.
--with-stack-clash-protection-guard-size=size
On certain targets this option sets the default stack clash protection guard size as a power of two in bytes. On AArch64 size is required to be either 12 (4KB) or 16 (64KB).
--with-isa-spec=ISA-spec-string
On RISC-V targets specify the default version of the RISC-V Unprivileged (formerly User-Level) ISA specification to produce code conforming to. The possibilities for ISA-spec-string are:
2.2
Produce code conforming to version 2.2.
20190608
Produce code conforming to version 20190608.
20191213
Produce code conforming to version 20191213.
In the absence of this configuration option the default version is 20191213.
--enable-__cxa_atexit
Define if you want to use __cxa_atexit, rather than atexit,
to register C++ destructors for local statics and global objects.
This is essential for fully standards-compliant handling of
destructors, but requires __cxa_atexit in libc.  This option is
currently only available on systems with GNU libc.  When enabled, this
will cause -fuse-cxa-atexit to be passed by default.
--enable-gnu-indirect-function
Define if you want to enable the ifunc attribute.  This option is
currently only available on systems with GNU libc on certain targets.
--enable-target-optspace
Specify that target libraries should be optimized for code space instead of code speed. This is the default for the m32r platform.
--with-cpp-install-dir=dirname
Specify that the user visible cpp program should be installed
in prefix/dirname/cpp, in addition to bindir.
--enable-comdat
Enable COMDAT group support. This is primarily used to override the automatically detected value.
--enable-initfini-array
Force the use of sections .init_array and .fini_array
(instead of .init and .fini) for constructors and
destructors.  Option --disable-initfini-array has the
opposite effect.  If neither option is specified, the configure script
will try to guess whether the .init_array and
.fini_array sections are supported and, if they are, use them.
--enable-link-mutex
When building GCC, use a mutex to avoid linking the compilers for multiple languages at the same time, to avoid thrashing on build systems with limited free memory. The default is not to use such a mutex.
--enable-link-serialization
When building GCC, use make dependencies to serialize linking the compilers for multiple languages, to avoid thrashing on build systems with limited free memory. The default is not to add such dependencies and thus with parallel make potentially link different compilers concurrently. If the argument is a positive integer, allow that number of concurrent link processes for the large binaries.
--enable-maintainer-mode
The build rules that regenerate the Autoconf and Automake output files as
well as the GCC master message catalog gcc.pot are normally
disabled.  This is because it can only be rebuilt if the complete source
tree is present.  If you have changed the sources and want to rebuild the
catalog, configuring with --enable-maintainer-mode will enable
this.  Note that you need a recent version of the gettext tools
to do so.
--disable-bootstrap
For a native build, the default configuration is to perform a 3-stage bootstrap of the compiler when ‘make’ is invoked, testing that GCC can compile itself correctly. If you want to disable this process, you can configure with --disable-bootstrap.
--enable-bootstrap
In special cases, you may want to perform a 3-stage build even if the target and host triplets are different. This is possible when the host can run code compiled for the target (e.g. host is i686-linux, target is i486-linux). Starting from GCC 4.2, to do this you have to configure explicitly with --enable-bootstrap.
--enable-generated-files-in-srcdir
Neither the .c and .h files that are generated from Bison and flex nor the info manuals and man pages that are built from the .texi files are present in the repository development tree. When building GCC from that development tree, or from one of our snapshots, those generated files are placed in your build directory, which allows for the source to be in a readonly directory.
If you configure with --enable-generated-files-in-srcdir then those generated files will go into the source directory. This is mainly intended for generating release or prerelease tarballs of the GCC sources, since it is not a requirement that the users of source releases to have flex, Bison, or makeinfo.
--enable-version-specific-runtime-libs
Specify that runtime libraries should be installed in the compiler specific subdirectory (libdir/gcc) rather than the usual places. In addition, ‘libstdc++’’s include files will be installed into libdir unless you overruled it by using --with-gxx-include-dir=dirname. Using this option is particularly useful if you intend to use several versions of GCC in parallel. The default is ‘yes’ for ‘libada’, and ‘no’ for the remaining libraries.
--with-darwin-extra-rpath
This is provided to allow distributions to add a single additional runpath on Darwin / macOS systems. This allows for cases where the installed GCC library directories are then symlinked to a common directory outside of the GCC installation.
--with-aix-soname=‘aix’, ‘svr4’ or ‘both’
Traditional AIX shared library versioning (versioned Shared Object
files as members of unversioned Archive Library files named
‘lib.a’) causes numerous headaches for package managers. However,
Import Files as members of Archive Library files allow for
filename-based versioning of shared libraries as seen on Linux/SVR4,
where this is called the "SONAME". But as they prevent static linking,
Import Files may be used with Runtime Linking only, where the
linker does search for ‘libNAME.so’ before ‘libNAME.a’ library
filenames with the ‘-lNAME’ linker flag.
For detailed information please refer to the AIX ld Command reference.
As long as shared library creation is enabled, upon:
--with-aix-soname=aix--with-aix-soname=both
A (traditional AIX) Shared Archive Library file is created:
 
Shared Object file as archive member named
  ‘libNAME.so.V’ (except for ‘libgcc_s’, where the dlopen("libNAME.a(libNAME.so.V)", RTLD_MEMBER)
   Static Archive
   Library file is needed
  --with-aix-soname=svr4
A (second) Shared Archive Library file is created:
 
-G linker flag
   F_LOADONLY flag set
   dlopen("libNAME.so.V(shr.o)",
   RTLD_MEMBER)
  Import File as archive member named ‘shr.imp’,
 which
  Loader Section of subsequent binaries
   ‘weak’ Keyword
   A symbolic link using the ‘libNAME.so’ filename scheme is created:
Shared Archive Library file
  ld Command to find ‘lib.so.V(shr.imp)’ via
  the ‘-lNAME’ argument (requires Runtime Linking to be enabled)
  dlopen("libNAME.so(shr.o)",
  RTLD_MEMBER)
  As long as static library creation is enabled, upon:
A Static Archive Library is created:
 
Static Object files as archive members, which
  While the aix-soname=‘svr4’ option does not create Shared Object
files as members of unversioned Archive Library files any more, package
managers still are responsible to
transfer Shared Object files
found as member of a previously installed unversioned Archive Library
file into the newly installed Archive Library file with the same
filename.
WARNING: Creating Shared Object files with Runtime Linking
enabled may bloat the TOC, eventually leading to TOC overflow errors,
requiring the use of either the -Wl,-bbigtoc linker flag (seen to
break with the GDB debugger) or some of the TOC-related compiler flags,
see “RS/6000 and PowerPC Options” in the main manual.
--with-aix-soname is currently supported by ‘libgcc_s’ only, so this option is still experimental and not for normal use yet.
Default is the traditional behavior --with-aix-soname=‘aix’.
--enable-languages=[^]lang1,[^]lang2,…
Specify that only a particular subset of compilers and
their runtime libraries should be built.  For a list of valid values for
langN you can issue the following command in the
gcc directory of your GCC source tree:
grep ^language= */config-lang.in
Currently, you can use any of the following:
all, default, ada, algol68, c, c++,
cobol, d, fortran, go, jit,
lto, m2, objc, obj-c++.
Building the Ada compiler has special requirements, see below.
If you do not pass this flag, or specify the option default, then the
default languages available in the gcc sub-tree will be configured.
Algol 68, Ada, COBOL, D, Go, Jit, Objective-C++ and Modula-2 are not default languages.
LTO is not a
default language, but is built by default because --enable-lto is
enabled by default.  The other languages are default languages.  If
all is specified, then all available languages are built.  An
exception is the jit language, which requires
--enable-host-shared to be included with all.
If a language name is prefixed with a caret, such as
‘--enable-languages=all,^obj-c++’, then that language will
not be built.  This is most useful when combined with all or
default.  A language disabled in this way will be disabled even
if it is also included without the leading caret earlier or later in
the argument to --enable-languages.  An attempt to disable a
language that is a prerequisite for an enabled language—(whether
the latter language was enabled explicitly, or implicitly via the
default or all directives)—is invalid.
--enable-stage1-languages=lang1,lang2,…
Specify that a particular subset of compilers and their runtime
libraries should be built with the system C compiler during stage 1 of
the bootstrap process, rather than only in later stages with the
bootstrapped C compiler.  The list of valid values is the same as for
--enable-languages, and the option all will select all
of the languages enabled by --enable-languages.  This option is
primarily useful for GCC development; for instance, when a development
version of the compiler cannot bootstrap due to compiler bugs, or when
one is debugging front ends other than the C front end.  When this
option is used, one can then build the target libraries for the
specified languages with the stage-1 compiler by using make
stage1-bubble all-target, or run the testsuite on the stage-1 compiler
for the specified languages using make stage1-start check-gcc.
--disable-libada
Specify that the run-time libraries and tools used by GNAT should not be built. This can be useful for debugging, or for compatibility with previous Ada build procedures, when it was required to explicitly do a ‘make -C gcc gnatlib_and_tools’.
--disable-libgm2
Specify that the run-time libraries and tools used by Modula-2 should not be built. This can be useful for debugging.
--disable-libsanitizer
Specify that the run-time libraries for the various sanitizers should not be built.
--disable-libssp
Specify that the run-time libraries for stack smashing protection should not be built or linked against. On many targets library support is provided by the C library instead.
--disable-libquadmath
Specify that the GCC quad-precision math library should not be built. On some systems, the library is required to be linkable when building the Fortran front end, unless --disable-libquadmath-support is used.
--disable-libquadmath-support
Specify that the Fortran front end and libgfortran do not add
support for libquadmath on systems supporting it.
--disable-libgomp
Specify that the GNU Offloading and Multi Processing Runtime Library should not be built.
--disable-libvtv
Specify that the run-time libraries used by vtable verification should not be built.
--with-dwarf2
Specify that the compiler should use DWARF debugging information as the default; the exact DWARF version that is the default is target-specific.
--with-advance-toolchain=at
On 64-bit PowerPC Linux systems, configure the compiler to use the header files, library files, and the dynamic linker from the Advance Toolchain release at instead of the default versions that are provided by the Linux distribution. In general, this option is intended for the developers of GCC, and it is not intended for general use.
--enable-targets=all--enable-targets=target_list
Some GCC targets, e.g. powerpc64-linux, build bi-arch compilers. These are compilers that are able to generate either 64-bit or 32-bit code. Typically, the corresponding 32-bit target, e.g. powerpc-linux for powerpc64-linux, only generates 32-bit code. This option enables the 32-bit target to be a bi-arch compiler, which is useful when you want a bi-arch compiler that defaults to 32-bit, and you are building a bi-arch or multi-arch Binutils in a combined tree. On mips-linux, this will build a tri-arch compiler (ABI o32/n32/64), defaulted to o32. Currently, this option only affects sparc-linux, powerpc-linux, x86-linux, and mips-linux.
--enable-default-pie
Turn on -fPIE and -pie by default.
--enable-secureplt
This option enables -msecure-plt by default for powerpc-linux. See “RS/6000 and PowerPC Options” in the main manual
--enable-default-ssp
Turn on -fstack-protector-strong by default.
--enable-cld
This option enables -mcld by default for 32-bit x86 targets. See “i386 and x86-64 Options” in the main manual
--enable-large-address-aware
The --enable-large-address-aware option arranges for MinGW executables to be linked using the --large-address-aware option, that enables the use of more than 2GB of memory. If GCC is configured with this option, its effects can be reversed by passing the -Wl,--disable-large-address-aware option to the so-configured compiler driver.
--enable-win32-registry--enable-win32-registry=key--disable-win32-registry
The --enable-win32-registry option enables Microsoft Windows-hosted GCC to look up installations paths in the registry using the following key:
HKEY_LOCAL_MACHINE\SOFTWARE\Free Software Foundation\key
key defaults to GCC version number, and can be overridden by the --enable-win32-registry=key option. Vendors and distributors who use custom installers are encouraged to provide a different key, perhaps one comprised of vendor name and GCC version number, to avoid conflict with existing installations. This feature is enabled by default, and can be disabled by --disable-win32-registry option. This option has no effect on the other hosts.
--nfp
Specify that the machine does not have a floating point unit. This option only applies to ‘m68k-sun-sunosn’. On any other system, --nfp has no effect.
--enable-werror--disable-werror--enable-werror=yes--enable-werror=no
When you specify this option, it controls whether certain files in the compiler are built with -Werror in bootstrap stage2 and later. If you don’t specify it, -Werror is turned on for the main development trunk. However it defaults to off for release branches and final releases. The specific files which get -Werror are controlled by the Makefiles.
--enable-checking--disable-checking--enable-checking=list
This option controls performing internal consistency checks in the compiler. It does not change the generated code, but adds error checking of the requested complexity. This slows down the compiler and may only work properly if you are building the compiler with GCC.
When the option is not specified, the active set of checks depends on context. Namely, bootstrap stage 1 defaults to ‘--enable-checking=yes’, builds from release branches or release archives default to ‘--enable-checking=release’, and otherwise ‘--enable-checking=yes,extra’ is used. When the option is specified without a list, the result is the same as ‘--enable-checking=yes’. Likewise, ‘--disable-checking’ is equivalent to ‘--enable-checking=no’.
The categories of checks available in list are ‘yes’ (most common checks ‘assert,misc,gc,gimple,rtlflag,runtime,tree,types’), ‘no’ (no checks at all), ‘all’ (all but ‘valgrind’), ‘release’ (cheapest checks ‘assert,runtime’) or ‘none’ (same as ‘no’). ‘release’ checks are always on and to disable them ‘--disable-checking’ or ‘--enable-checking=no[,<other checks>]’ must be explicitly requested. Disabling assertions makes the compiler and runtime slightly faster but increases the risk of undetected internal errors causing wrong code to be generated.
Individual checks can be enabled with these flags: ‘assert’, ‘df’, ‘extra’, ‘fold’, ‘gc’, ‘gcac’, ‘gimple’, ‘misc’, ‘rtl’, ‘rtlflag’, ‘runtime’, ‘tree’, ‘types’ and ‘valgrind’. ‘extra’ extends ‘misc’ checking with extra checks that might affect code generation and should therefore not differ between stage1 and later stages in bootstrap.
The ‘valgrind’ check requires the external valgrind simulator,
available from https://valgrind.org.  The ‘rtl’ checks are
expensive and the ‘df’, ‘gcac’ and ‘valgrind’ checks are very
expensive.
--disable-stage1-checking--enable-stage1-checking--enable-stage1-checking=list
This option affects only bootstrap build. If no --enable-checking option is specified the stage1 compiler is built with ‘yes’ checking enabled, otherwise the stage1 checking flags are the same as specified by --enable-checking. To build the stage1 compiler with different checking options use --enable-stage1-checking. The list of checking options is the same as for --enable-checking. If your system is too slow or too small to bootstrap a released compiler with checking for stage1 enabled, you can use ‘--disable-stage1-checking’ to disable checking for the stage1 compiler.
--enable-coverage--enable-coverage=level
With this option, the compiler is built to collect self coverage information, every time it is run. This is for internal development purposes, and only works when the compiler is being built with gcc. The level argument controls whether the compiler is built optimized or not, values are ‘opt’ and ‘noopt’. For coverage analysis you want to disable optimization, for performance analysis you want to enable optimization. When coverage is enabled, the default level is without optimization.
--enable-gather-detailed-mem-stats
When this option is specified more detailed information on memory allocation is gathered. This information is printed when using -fmem-report.
--enable-valgrind-annotations
Mark selected memory related operations in the compiler when run under valgrind to suppress false positives.
--enable-nls--disable-nls
The --enable-nls option enables Native Language Support (NLS), which lets GCC output diagnostics in languages other than American English. Native Language Support is enabled by default if not doing a canadian cross build. The --disable-nls option disables NLS.
Note that this functionality requires either libintl (provided by GNU gettext) or C standard library that contains support for gettext (such as the GNU C Library). See –with-included-gettext, for more information on the conditions required to get gettext support.
--with-libintl-prefix=dir--without-libintl-prefix
Searches for libintl in dir/include and dir/lib, or disables manual searching for it, letting the linker handle it.
--with-libintl-type=type
Specifies the type of library to search for when looking for libintl.
type can be one of auto, static or shared.
--with-included-gettext
Only available if gettext is present in the source tree.
Forces the gettext tree to be configured to build and use a new static libintl, overriding the system libintl. Results in GCC being built against the newly built libintl rather than the system libintl.
The build system makes a somewhat complicated choice when picking where to get gettext routines from. The following table is a summary of the possible options:
--with-catgets
If NLS is enabled, and if the host lacks gettext but has the
inferior catgets interface, the GCC build procedure normally
ignores catgets and instead uses GCC’s copy of the GNU
gettext library.  The --with-catgets option causes the
build procedure to use the host’s catgets in this situation.
--with-libiconv-prefix=dir
Search for libiconv header files in dir/include and libiconv library files in dir/lib.
--enable-obsolete
Enable configuration for an obsoleted system. If you attempt to configure GCC for a system (build, host, or target) which has been obsoleted, and you do not specify this flag, configure will halt with an error message.
All support for systems which have been obsoleted in one release of GCC is removed entirely in the next major release, unless someone steps forward to maintain the port.
--enable-decimal-float--enable-decimal-float=yes--enable-decimal-float=no--enable-decimal-float=bid--enable-decimal-float=dpd--disable-decimal-float
Enable (or disable) support for the C decimal floating point extension that is in the IEEE 754-2008 standard. This is enabled by default only on AArch64, PowerPC, i386, and x86_64 GNU/Linux systems. Other systems may also support it, but require the user to specifically enable it. You can optionally control which decimal floating point format is used (either ‘bid’ or ‘dpd’). The ‘bid’ (binary integer decimal) format is default on AArch64, i386 and x86_64 systems, and the ‘dpd’ (densely packed decimal) format is default on PowerPC systems.
--enable-fixed-point--disable-fixed-point
Enable (or disable) support for C fixed-point arithmetic. This option is enabled by default for some targets (such as MIPS) which have hardware-support for fixed-point operations. On other targets, you may enable this option manually.
--with-long-double-128
Specify if long double type should be 128-bit by default on selected
GNU/Linux architectures.  If using --without-long-double-128,
long double will be by default 64-bit, the same as double type.
When neither of these configure options are used, the default will be
128-bit long double when built against GNU C Library 2.4 and later,
64-bit long double otherwise.
--with-long-double-format=ibm--with-long-double-format=ieee
Specify whether long double uses the IBM extended double format
or the IEEE 128-bit floating point format on PowerPC Linux systems.
This configuration switch will only work on little endian PowerPC
Linux systems and on big endian 64-bit systems where the default CPU
is at least power7 (i.e. --with-cpu=power7,
--with-cpu=power8, or --with-cpu=power9 is used).
If you use the --without-long-double-128 configuration option, the --with-long-double-format=ibm and --with-long-double-format=ieee options are ignored.
The default long double format is to use IBM extended double.
Until all of the libraries are converted to use IEEE 128-bit floating
point, it is not recommended to use
--with-long-double-format=ieee.
--enable-fdpic
On SH Linux systems, generate ELF FDPIC code.
--with-gmp=pathname--with-gmp-include=pathname--with-gmp-lib=pathname--with-mpfr=pathname--with-mpfr-include=pathname--with-mpfr-lib=pathname--with-mpc=pathname--with-mpc-include=pathname--with-mpc-lib=pathname
If you want to build GCC but do not have the GMP library, the MPFR
library and/or the MPC library installed in a standard location and
do not have their sources present in the GCC source tree then you
can explicitly specify the directory where they are installed
(‘--with-gmp=gmpinstalldir’,
‘--with-mpfr=mpfrinstalldir’,
‘--with-mpc=mpcinstalldir’).  The
--with-gmp=gmpinstalldir option is shorthand for
--with-gmp-lib=gmpinstalldir/lib and
--with-gmp-include=gmpinstalldir/include.  Likewise the
--with-mpfr=mpfrinstalldir option is shorthand for
--with-mpfr-lib=mpfrinstalldir/lib and
--with-mpfr-include=mpfrinstalldir/include, also the
--with-mpc=mpcinstalldir option is shorthand for
--with-mpc-lib=mpcinstalldir/lib and
--with-mpc-include=mpcinstalldir/include.  If these
shorthand assumptions are not correct, you can use the explicit
include and lib options directly.  You might also need to ensure the
shared libraries can be found by the dynamic linker when building and
using GCC, for example by setting the runtime shared library path
variable (LD_LIBRARY_PATH on GNU/Linux and Solaris systems).
These flags are applicable to the host platform only. When building a cross compiler, they will not be used to configure target libraries.
--with-isl=pathname--with-isl-include=pathname--with-isl-lib=pathname
If you do not have the isl library installed in a standard location and you want to build GCC, you can explicitly specify the directory where it is installed (‘--with-isl=islinstalldir’). The --with-isl=islinstalldir option is shorthand for --with-isl-lib=islinstalldir/lib and --with-isl-include=islinstalldir/include. If this shorthand assumption is not correct, you can use the explicit include and lib options directly.
--with-stage1-ldflags=flags
This option may be used to set linker flags to be used when linking stage 1 of GCC. These are also used when linking GCC if configured with --disable-bootstrap. If --with-stage1-libs is not set to a value, then the default is ‘-static-libstdc++ -static-libgcc’, if supported.
--with-stage1-libs=libs
This option may be used to set libraries to be used when linking stage 1 of GCC. These are also used when linking GCC if configured with --disable-bootstrap.
--with-boot-ldflags=flags
This option may be used to set linker flags to be used when linking stage 2 and later when bootstrapping GCC. If –with-boot-libs is not is set to a value, then the default is ‘-static-libstdc++ -static-libgcc’.
--with-boot-libs=libs
This option may be used to set libraries to be used when linking stage 2 and later when bootstrapping GCC.
--with-debug-prefix-map=map
Convert source directory names using -fdebug-prefix-map when building runtime libraries. ‘map’ is a space-separated list of maps of the form ‘old=new’.
--enable-linker-build-id
Tells GCC to pass --build-id option to the linker for all final links (links performed without the -r or --relocatable option), if the linker supports it. If you specify --enable-linker-build-id, but your linker does not support --build-id option, a warning is issued and the --enable-linker-build-id option is ignored. The default is off.
--with-linker-hash-style=choice
Tells GCC to pass --hash-style=choice option to the linker for all final links. choice can be one of ‘sysv’, ‘gnu’, and ‘both’ where ‘sysv’ is the default.
--enable-gnu-unique-object--disable-gnu-unique-object
Tells GCC to use the gnu_unique_object relocation for C++ template static data members and inline function local statics. Enabled by default for a toolchain with an assembler that accepts it and GLIBC 2.11 or above, otherwise disabled.
--with-diagnostics-color=choice
Tells GCC to use choice as the default for -fdiagnostics-color=
option (if not used explicitly on the command line).  choice
can be one of ‘never’, ‘auto’, ‘always’, and ‘auto-if-env’
where ‘auto’ is the default.  ‘auto-if-env’ makes
-fdiagnostics-color=auto the default if GCC_COLORS
is present and non-empty in the environment of the compiler, and
-fdiagnostics-color=never otherwise.
--with-diagnostics-urls=choice
Tells GCC to use choice as the default for -fdiagnostics-urls=
option (if not used explicitly on the command line).  choice
can be one of ‘never’, ‘auto’, ‘always’, and ‘auto-if-env’
where ‘auto’ is the default.  ‘auto-if-env’ makes
-fdiagnostics-urls=auto the default if GCC_URLS
or TERM_URLS is present and non-empty in the environment of the
compiler, and -fdiagnostics-urls=never otherwise.
--enable-lto--disable-lto
Enable support for link-time optimization (LTO). This is enabled by default, and may be disabled using --disable-lto.
--enable-linker-plugin-configure-flags=FLAGS--enable-linker-plugin-flags=FLAGS
By default, linker plugins (such as the LTO plugin) are built for the host system architecture. For the case that the linker has a different (but run-time compatible) architecture, these flags can be specified to build plugins that are compatible to the linker. For example, if you are building GCC for a 64-bit x86_64 (‘x86_64-pc-linux-gnu’) host system, but have a 32-bit x86 GNU/Linux (‘i686-pc-linux-gnu’) linker executable (which is executable on the former system), you can configure GCC as follows for getting compatible linker plugins:
% srcdir/configure \
    --host=x86_64-pc-linux-gnu \
    --enable-linker-plugin-configure-flags=--host=i686-pc-linux-gnu \
    --enable-linker-plugin-flags='CC=gcc\ -m32\ -Wl,-rpath,[...]/i686-pc-linux-gnu/lib'
--with-plugin-ld=pathname
Enable an alternate linker to be used at link-time optimization (LTO) link time when -fuse-linker-plugin is enabled. This linker should have plugin support such as gold starting with version 2.20 or GNU ld starting with version 2.21. See -fuse-linker-plugin for details.
--enable-canonical-system-headers--disable-canonical-system-headers
Enable system header path canonicalization for libcpp. This can produce shorter header file paths in diagnostics and dependency output files, but these changed header paths may conflict with some compilation environments. Enabled by default, and may be disabled using --disable-canonical-system-headers.
--with-glibc-version=major.minor
Tell GCC that when the GNU C Library (glibc) is used on the target it will be version major.minor or later. Normally this can be detected from the C library’s header files, but this option may be needed when bootstrapping a cross toolchain without the header files available for building the initial bootstrap compiler.
If GCC is configured with some multilibs that use glibc and some that do not, this option applies only to the multilibs that use glibc. However, such configurations may not work well as not all the relevant configuration in GCC is on a per-multilib basis.
--enable-as-accelerator-for=target
Build as offload target compiler. Specify offload host triple by target.
--enable-offload-targets=target1[=path1],…,targetN[=pathN]
Enable offloading to targets target1, …, targetN. Offload compilers are expected to be already installed. Default search path for them is exec-prefix, but it can be changed by specifying paths path1, …, pathN.
% srcdir/configure \
    --enable-offload-targets=amdgcn-amdhsa,nvptx-none
--enable-offload-defaulted
Tell GCC that configured but not installed offload compilers and libgomp plugins are silently ignored. Useful for distribution compilers where those are in separate optional packages and where the presence or absence of those optional packages should determine the actual supported offloading target set rather than the GCC configure-time selection.
--enable-cet--disable-cet
Enable building target run-time libraries with control-flow
instrumentation, see -fcf-protection option.  When
--enable-cet is specified target libraries are configured
to add -fcf-protection and, if needed, other target
specific options to a set of building options.
--enable-cet=auto is default.  CET is enabled on Linux/x86 if
target Binutils supports Intel CET instructions and disabled
otherwise.  In this case, the target libraries are configured to get
additional -fcf-protection option.
--enable-x86-64-mfentry--disable-x86-64-mfentry
Enable -mfentry by default on x86-64 to put the profiling
counter call, __fentry__, before the prologue so that -pg
can be used with -fshrink-wrap which is enabled at -O1.
This configure option is 64-bit only because __fentry__ doesn’t
support PIC in 32-bit mode.
--enable-x86-64-mfentry=auto is default. -mfentry is enabled on Linux/x86-64 by default.
--with-riscv-attribute=‘yes’, ‘no’ or ‘default’
Generate RISC-V attribute by default, in order to record extra build information in object.
The option is disabled by default. It is enabled on RISC-V/ELF (bare-metal) target if target Binutils supported.
--enable-s390-excess-float-precision--disable-s390-excess-float-precision
On s390x targets, enable treatment of float expressions with double precision
when in standards-compliant mode (e.g., when --std=c99 or
-fexcess-precision=standard are given).
For a native build and cross compiles that have target headers, the option’s default is derived from glibc’s behavior. When glibc clamps float_t to double, GCC follows and enables the option. For other cross compiles, the default is disabled.
--with-zstd=pathname--with-zstd-include=pathname--with-zstd-lib=pathname
If you do not have the zstd library installed in a standard
location and you want to build GCC, you can explicitly specify the
directory where it is installed (‘--with-zstd=zstdinstalldir’).
The --with-zstd=zstdinstalldir option is shorthand for
--with-zstd-lib=zstdinstalldir/lib and
--with-zstd-include=zstdinstalldir/include. If this
shorthand assumption is not correct, you can use the explicit
include and lib options directly.
The following options only apply to building cross compilers.
--with-toolexeclibdir=dir
Specify the installation directory for libraries built with a cross compiler. The default is ${gcc_tooldir}/lib.
--with-sysroot--with-sysroot=dir
Tells GCC to consider dir as the root of a tree that contains (a subset of) the root filesystem of the target operating system. Target system headers, libraries and run-time object files will be searched for in there. More specifically, this acts as if --sysroot=dir was added to the default options of the built compiler. The specified directory is not copied into the install tree, unlike the options --with-headers and --with-libs that this option obsoletes. The default value, in case --with-sysroot is not given an argument, is ${gcc_tooldir}/sys-root. If the specified directory is a subdirectory of ${exec_prefix}, then it will be found relative to the GCC binaries if the installation tree is moved.
This option affects the system root for the compiler used to build
target libraries (which runs on the build system) and the compiler newly
installed with make install; it does not affect the compiler which is
used to build GCC itself.
If you specify the --with-native-system-header-dir=dirname option then the compiler will search that directory within dirname for native system headers rather than the default /usr/include.
--with-build-sysroot--with-build-sysroot=dir
Tells GCC to consider dir as the system root (see --with-sysroot) while building target libraries, instead of the directory specified with --with-sysroot. This option is only useful when you are already using --with-sysroot. You can use --with-build-sysroot when you are configuring with --prefix set to a directory that is different from the one in which you are installing GCC and your target libraries.
This option affects the system root for the compiler used to build target libraries (which runs on the build system); it does not affect the compiler which is used to build GCC itself.
--with-headers--with-headers=dir
Deprecated in favor of --with-sysroot.
Specifies that target headers are available when building a cross compiler.
The dir argument specifies a directory which has the target include
files.  These include files will be copied into the gcc install
directory.  This option with the dir argument is required when
building a cross compiler, if prefix/target/sys-include
doesn’t pre-exist.  If prefix/target/sys-include does
pre-exist, the dir argument may be omitted.  fixincludes
will be run on these files to make them compatible with GCC.
--without-headers
Tells GCC not use any target headers from a libc when building a cross compiler. When crossing to GNU/Linux, you need the headers so GCC can build the exception handling for libgcc.
--with-libs--with-libs="dir1 dir2 … dirN"
Deprecated in favor of --with-sysroot. Specifies a list of directories which contain the target runtime libraries. These libraries will be copied into the gcc install directory. If the directory list is omitted, this option has no effect.
--with-newlib
Specifies that ‘newlib’ is
being used as the target C library.  This causes __eprintf to be
omitted from libgcc.a on the assumption that it will be provided by
‘newlib’.
--with-avrlibc
Only supported for the AVR target. Specifies that
AVR-LibC
is being used as the target C  library.  This causes float support
functions like __addsf3 to be omitted from libgcc.a on
the assumption that it will be provided by libm.a.  For more
technical details, cf. PR54461.
It is not supported for
RTEMS configurations, which currently use Newlib.  The option is
supported since version 4.7.2 and is the default in 4.8.0 and newer.
--with-double={32|64|32,64|64,32}--with-long-double={32|64|32,64|64,32|double}
Only supported for the AVR target since version 10. Specify the default layout available for the C/C++ ‘double’ and ‘long double’ type, respectively. The following rules apply:
Not all combinations of --with-double= and --with-long-double= are valid. For example, the combination --with-double=32,64 --with-long-double=32 will be rejected because the first option specifies the availability of multilibs for ‘double’, whereas the second option implies that ‘long double’ — and hence also ‘double’ — is always 32 bits wide.
--with-double-comparison={tristate|bool|libf7}
Only supported for the AVR target since version 10.
Specify what result format is returned by library functions that
compare 64-bit floating point values (DFmode).
The GCC default is ‘tristate’.  If the floating point
implementation returns a boolean instead, set it to ‘bool’.
--with-libf7={libgcc|math|math-symbols|no}
Only supported for the AVR target since version 10.
Specify to which degree code from LibF7 is included in libgcc.
LibF7 is an ad-hoc, AVR-specific, 64-bit floating point emulation
written in C and (inline) assembly. ‘libgcc’ adds support
for functions that one would usually expect in libgcc like double addition,
double comparisons and double conversions. ‘math’ also adds routines
that one would expect in libm.a, but with __ (two underscores)
prepended to the symbol names as specified by math.h.
‘math-symbols’ also defines weak aliases for the functions
declared in math.h.  However, --with-libf7 won’t
install no math.h header file whatsoever, this file must come
from elsewhere.  This option sets --with-double-comparison
to ‘bool’.
--with-nds32-lib=library
Specifies that library setting is used for building libgcc.a. Currently, the valid library is ‘newlib’ or ‘mculib’. This option is only supported for the NDS32 target.
--with-build-time-tools=dir
Specifies where to find the set of target tools (assembler, linker, etc.) that will be used while building GCC itself. This option can be useful if the directory layouts are different between the system you are building GCC on, and the system where you will deploy it.
For example, on an ‘ia64-hp-hpux’ system, you may have the GNU assembler and linker in /usr/bin, and the native tools in a different path, and build a toolchain that expects to find the native tools in /usr/bin.
When you use this option, you should ensure that dir includes
ar, as, ld, nm,
ranlib and strip if necessary, and possibly
objdump.  Otherwise, GCC may use an inconsistent set of
tools.
configure test results
Sometimes, it might be necessary to override the result of some
configure test, for example in order to ease porting to a new
system or work around a bug in a test.  The toplevel configure
script provides three variables for this:
build_configargs
The contents of this variable is passed to all build configure
scripts.
host_configargs
The contents of this variable is passed to all host configure
scripts.
target_configargs
The contents of this variable is passed to all target configure
scripts.
In order to avoid shell and make quoting issues for complex
overrides, you can pass a setting for CONFIG_SITE and set
variables in the site file.
The following options apply to the build of the Algol 68 runtime library.
--enable-algol68-gc
Specify that an additional variant of the GNU Algol 68 runtime library is built, using an external build of the Boehm-Demers-Weiser garbage collector (https://www.hboehm.info/gc/).
This library needs to be available for each multilib variant, unless configured with --enable-algol68-gc=‘auto’ in which case the build of the additional runtime library is skipped when not available and the build continues.
--with-target-bdw-gc=list--with-target-bdw-gc-include=list--with-target-bdw-gc-lib=list
Specify search directories for the garbage collector header files and libraries. list is a comma separated list of key value pairs of the form ‘multilibdir=path’, where the default multilib key is named as ‘.’ (dot), or is omitted (e.g. ‘--with-target-bdw-gc=/opt/bdw-gc,32=/opt-bdw-gc32’).
The options --with-target-bdw-gc-include and --with-target-bdw-gc-lib must always be specified together for each multilib variant and they take precedence over --with-target-bdw-gc. If --with-target-bdw-gc-include is missing values for a multilib, then the value for the default multilib is used (e.g. ‘--with-target-bdw-gc-include=/opt/bdw-gc/include’ ‘--with-target-bdw-gc-lib=/opt/bdw-gc/lib64,32=/opt-bdw-gc/lib32’). If none of these options are specified, the library is assumed in default locations.
The following options apply to the build of the Objective-C runtime library.
--enable-objc-gc
Specify that an additional variant of the GNU Objective-C runtime library is built, using an external build of the Boehm-Demers-Weiser garbage collector (https://www.hboehm.info/gc/). This library needs to be available for each multilib variant, unless configured with --enable-objc-gc=‘auto’ in which case the build of the additional runtime library is skipped when not available and the build continues.
The following options apply to the build of the D runtime library.
--enable-libphobos-checking--disable-libphobos-checking--enable-libphobos-checking=list
This option controls whether run-time checks and contracts are compiled into the D runtime library. When the option is not specified, the library is built with ‘release’ checking. When the option is specified without a list, the result is the same as ‘--enable-libphobos-checking=yes’. Likewise, ‘--disable-libphobos-checking’ is equivalent to ‘--enable-libphobos-checking=no’.
The categories of checks available in list are ‘yes’ (compiles libphobos with -fno-release), ‘no’ (compiles libphobos with -frelease), ‘all’ (same as ‘yes’), ‘none’ or ‘release’ (same as ‘no’).
Individual checks available in list are ‘assert’ (compiles libphobos with an extra option -fassert).
--with-libphobos-druntime-only--with-libphobos-druntime-only=choice
Specify whether to build only the core D runtime library (druntime), or both the core and standard library (phobos) into libphobos. This is useful for targets that have full support in druntime, but no or incomplete support in phobos. choice can be one of ‘auto’, ‘yes’, and ‘no’ where ‘auto’ is the default.
When the option is not specified, the default choice ‘auto’ means that it is inferred whether the target has support for the phobos standard library. When the option is specified without a choice, the result is the same as ‘--with-libphobos-druntime-only=yes’.
--with-target-system-zlib
Use installed ‘zlib’ rather than that included with GCC. This needs to be available for each multilib variant, unless configured with --with-target-system-zlib=‘auto’ in which case the GCC included ‘zlib’ is only used when the system installed library is not available.
The following options apply to the build of the COBOL runtime library.
--with-target-libxml2=list--with-target-libxml2-include=list--with-target-libxml2-lib=list
Specify search directories for the libxml2 header files and libraries. list is a comma separated list of key value pairs of the form ‘multilibdir=path’, where the default multilib key is named as ‘.’ (dot), or is omitted (e.g. ‘--with-target-libxml2=/opt/libxml2,32=/opt-libxml2-32’).
The options --with-target-libxml2-include and --with-target-libxml2-lib must always be specified together for each multilib variant and they take precedence over --with-target-libxml2. If --with-target-libxml2-include is missing values for a multilib, then the value for the default multilib is used (e.g. ‘--with-target-libxml2-include=/opt/libxml2/include’ ‘--with-target-libxml2-lib=/opt/libxml2/lib64,32=/opt-libxml2/lib32’). If none of these options are specified, the library is assumed in default locations.
Copyright (C) Free Software Foundation, Inc. Verbatim copying and distribution of this entire article is permitted in any medium, provided this notice is preserved.
These pages are maintained by the GCC team. Last modified 2026-09-03.