%define name		libgcrypt
%define version		1.4.0
%define release		%mkrel 1

%define major		11
%define libname		%mklibname gcrypt %{major}
%define develname	%mklibname -d gcrypt

# disable tests by default, no /dev/random feed, no joy
%define do_check 0
%{expand: %{?_with_check: %%global do_check 1}}

Summary: 	GNU Cryptographic library
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	LGPLv2+
Group: 		System/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
Url: 		http://www.gnupg.org/

# don't convert to bzip2, since we ship archive signature
Source0: 	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2.sig
Patch1:		libgcrypt-1.2.0-libdir.patch
#Patch2:		libgcrypt-1.2.3-ppc64.patch

BuildRequires:	libgpg-error-devel >= 0.5

%package	-n %{libname}
Summary:	GNU Cryptographic library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%package	-n %{develname}
Summary:	Development files for GNU cryptographic library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d gcrypt 11

%description
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.


%description -n %{libname}
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.


%description -n %{develname}
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.
This package contains files needed to develop
applications using libgcrypt. ( For example Ägypten project )


%prep
%setup -q
%patch1 -p1 -b .libdir
#%patch2 -p1 -b .ppc64

%build
%configure2_5x
%make

%check
%if %{do_check}
make check
%endif

%install
rm -rf %buildroot
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{develname}
%_install_info %{name}.info

%postun -n %{develname}
%_remove_install_info %{name}.info


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}
%{_libdir}/lib*.so.%{major}.*
%doc AUTHORS COPYING COPYING.LIB README NEWS THANKS TODO

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog README.*

%{_bindir}/*
%{_includedir}/*.h

%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so

%{_datadir}/aclocal/*
%{_infodir}/gcrypt.info*


