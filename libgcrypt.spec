%define major 11
%define libname %mklibname gcrypt %{major}
%define develname %mklibname gcrypt -d

# disable tests by default, no /dev/random feed, no joy
%define do_check 1
%{expand: %{?_with_check: %%global do_check 1}}

Summary:	GNU Cryptographic library
Name:		libgcrypt
Version:	1.4.6
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnupg.org/
# don't convert to bzip2, since we ship archive signature
Source0:	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2.sig
Patch1:		libgcrypt-1.2.0-libdir.patch
BuildRequires:	libgpg-error-devel >= 0.5
BuildRequires:	%{_lib}pth-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.

%package -n %{libname}
Summary:	GNU Cryptographic library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Libgcrypt is a general purpose cryptographic library
based on the code from GNU Privacy Guard.  It provides functions for all
cryptograhic building blocks: symmetric ciphers
(AES,DES,Blowfish,CAST5,Twofish,Arcfour), hash algorithms (MD5,
RIPE-MD160, SHA-1, TIGER-192), MACs (HMAC for all hash algorithms),
public key algorithms (RSA, ElGamal, DSA), large integer functions,
random numbers and a lot of supporting functions.

%package -n %{develname}
Summary:	Development files for GNU cryptographic library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d gcrypt 11

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
%configure2_5x \
	--disable-dev-random \
	--enable-random-daemon \
	--enable-m-guard
%make

%check
%if %{do_check}
make check
%endif

%install
rm -rf %{buildroot}
%makeinstall_std
%multiarch_binaries $RPM_BUILD_ROOT/%{_sbindir}/gcryptrnd

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%_install_info %{name}.info

%postun -n %{develname}
%_remove_install_info %{name}.info

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS README NEWS THANKS TODO
%multiarch %{multiarch_sbindir}/gcryptrnd
%{_libdir}/lib*.so.%{major}
%{_libdir}/lib*.so.%{major}.*

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
