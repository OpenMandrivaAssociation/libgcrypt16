%define	major	11
%define	libname	%mklibname gcrypt %{major}
%define	devname	%mklibname gcrypt -d

# disable tests by default, no /dev/random feed, no joy
%bcond_with	check

Summary:	GNU Cryptographic library
Name:		libgcrypt
Version:	1.5.0
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnupg.org/
# don't convert to bzip2, since we ship archive signature
Source0:	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2.sig
Patch1:		libgcrypt-1.2.0-libdir.patch
Patch2:		libgcrypt-1.5.0-gcry_mpi_print-volatile-len-variable.patch
BuildRequires:	libgpg-error-devel >= 0.5
BuildRequires:	pth-devel

%description
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.

%package -n	%{libname}
Summary:	GNU Cryptographic library
Group:		System/Libraries

%description -n	%{libname}
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.

%package -n	%{devname}
Summary:	Development files for GNU cryptographic library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d gcrypt 11

%description -n	%{devname}
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.
This package contains files needed to develop
applications using libgcrypt. ( For example Ägypten project )

%prep
%setup -q
%patch1 -p1 -b .libdir~
%patch2 -p1 -b .volatile~

%build
%configure2_5x \
	--enable-shared \
	--enable-static \
	--disable-dev-random \
	--enable-random-daemon \
	--enable-m-guard
%make

%if %{with check}
%check
make check
%endif

%install
%makeinstall_std

mv %{buildroot}%{_sbindir}/gcryptrnd %{buildroot}%{_bindir}/gcryptrnd

%multiarch_binaries %{buildroot}%{_bindir}/gcryptrnd

%files -n %{libname}
%doc AUTHORS README NEWS THANKS TODO
%{multiarch_bindir}/gcryptrnd
%{_bindir}/gcryptrnd
%{_libdir}/lib*.so.%{major}
%{_libdir}/lib*.so.%{major}.*

%files -n %{devname}
%doc ChangeLog README.*
%exclude %{multiarch_bindir}/gcryptrnd
%exclude %{_bindir}/gcryptrnd
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_datadir}/aclocal/*
%{_infodir}/gcrypt.info*


%changelog
* Fri Mar 16 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5.0-3
+ Revision: 785341
- nuke the libtool *.la file

* Fri Mar 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.0-2
+ Revision: 783777
- fix unitialized variable issue triggered by compiler optimizations (P2)
- clean out & rebuild with internal dependency generator

* Wed Aug 03 2011 Funda Wang <fwang@mandriva.org> 1.5.0-1
+ Revision: 692939
- new version 1.5.0 final

* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 1.5.0-0.beta1.2
+ Revision: 664000
- bump rel
- fix multiarch usage

* Mon Feb 21 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.5.0-0.beta1.1
+ Revision: 639204
- fix file duplicated across multiple packages
- sanitize dependencies a bit..
- new release: 1.5.0 beta1
- drop obsolete scriptlets

* Sat Jul 17 2010 Lonyai Gergely <aleph@mandriva.org> 1.4.6-3mdv2011.0
+ Revision: 554586
- Multiarch fix 2.

* Sat Jul 17 2010 Lonyai Gergely <aleph@mandriva.org> 1.4.6-2mdv2011.0
+ Revision: 554472
- gcryptrnd mv into %%_bindir from %%_sbindir
- Fix a multiarch problem

* Thu Jul 15 2010 Lonyai Gergely <aleph@mandriva.org> 1.4.6-1mdv2011.0
+ Revision: 553560
- Add BuildRequires libpth-devel
- 1.4.6
  Enable internal random generator
  Enable m-guard facility

* Sat Dec 12 2009 Lonyai Gergely <aleph@mandriva.org> 1.4.5-1mdv2010.1
+ Revision: 477947
- 1.4.5

* Thu Feb 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.4-1mdv2009.1
+ Revision: 337692
- update to new version 1.4.4

* Tue Oct 14 2008 Funda Wang <fwang@mandriva.org> 1.4.3-1mdv2009.1
+ Revision: 293496
- New version 1.4.3

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.4.1-2mdv2009.0
+ Revision: 264802
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.1-1mdv2009.0
+ Revision: 209083
- new version
- do not re-define stuff
- fix mixture of tabs and spaces
- do not install COPYING files
- spec file clean

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Dec 15 2007 Emmanuel Andry <eandry@mandriva.org> 1.4.0-1mdv2008.1
+ Revision: 120441
- New version
- license is now LGPLv2+
- add major version check
- drop patch2

* Tue Sep 18 2007 Funda Wang <fwang@mandriva.org> 1.2.4-2mdv2008.0
+ Revision: 89577
- New devel package policy


* Fri Feb 02 2007 Andreas Hasenack <andreas@mandriva.com> 1.2.4-1mdv2007.0
+ Revision: 115972
- updated to version 1.2.4

* Wed Dec 13 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.2.3-2mdv2007.1
+ Revision: 96333
- don't make check
- add ppc64 support

* Tue Aug 29 2006 Andreas Hasenack <andreas@mandriva.com> 1.2.3-1mdv2007.0
+ Revision: 58340
- updated to version 1.2.3 (upstream bugfixes)
- bunzipped patch
- Import libgcrypt

* Sun Dec 04 2005 Andreas Hasenack <andreasa@mandriva.com> 1.2.2-1mdk
- updated to version 1.2.2

* Tue Jun 21 2005 Erwan Velu <velu@seanodes.com> 1.2.1-1mdk
- 1.2.1
- Removed patch0 merged upstream
- Removed patch2 : no more necessary

* Tue May 31 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.0-7mdk
- Fix compile with gcc-4.0

* Fri Mar 11 2005 Stefan van der Eijk <stefan@eijk.nu> 1.2.0-6mdk
- reupload --> lost during ken crash

* Mon Feb 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.0-5mdk
- drop lib64 patch in favor of total nuking of -L$(libdir) where
  libdir is a standard library search path, aka fix parallel
  installation when you don't install them at once.

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.0-4mdk
- lib64/multiarch

* Fri Dec 17 2004 Abel Cheung <deaddog@mandrake.org> 1.2.0-3mdk
- Rebuild

* Thu Aug 19 2004 Abel Cheung <deaddog@deaddog.org> 1.2.0-2mdk
- Rebuild

* Fri May 21 2004 Abel Cheung <deaddog@deaddog.org> 1.2.0-1mdk
- Patch0: automake 1.8 compatibility
- New stable version
- make check
- Use UTF-8 for spec!

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.1.94-1mdk
- Release 1.1.94
- Switch back to gzip archives, since they are signed upstream

