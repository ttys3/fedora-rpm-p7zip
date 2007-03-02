Summary: Very high compression ratio file archiver
Name: p7zip
Version: 4.44
Release: 2%{?dist}
License: LGPL
Group: Applications/Archiving
URL: http://p7zip.sourceforge.net/
# RAR sources removed since their license is incompatible with the LGPL
#Source: http://dl.sf.net/p7zip/p7zip_%{version}_src_all.tar.bz2
# VERSION=
# tar xjvf p7zip_${VERSION}_src_all.tar.bz2
# rm -rf p7zip_${VERSION}/CPP/7zip/{Archive,Compress,Crypto}/Rar*
# rm -f p7zip_${VERSION}/DOCS/unRarLicense.txt
# tar --numeric-owner -cjvf p7zip_${VERSION}_src_all-norar.tar.bz2 p7zip_${VERSION}
Source: p7zip_%{version}_src_all-norar.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary: Additional plugins for p7zip
Group: Applications/Archiving
Requires: %{name} = %{version}-%{release}

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.


%prep
%setup -q -n %{name}_%{version}

# Create wrapper scripts, as 7zCon.sfx and Codecs/Formats need to be in the
# same directory as the binaries, and we don't want them in %{_bindir}.
%{__cat} << 'EOF' > 7za.sh
#!/bin/sh
exec %{_libexecdir}/p7zip/7za "$@"
EOF

%{__cat} << 'EOF' > 7z.sh
#!/bin/sh
exec %{_libexecdir}/p7zip/7z "$@"
EOF


%build
%ifarch %{ix86} ppc
%{__cp} -f makefile.linux_x86_ppc_alpha__gcc_4.X makefile.machine
%endif
%ifarch x86_64
%{__cp} -f makefile.linux_amd64 makefile.machine
%endif

# Use optflags
%{__perl} -pi -e 's|^ALLFLAGS=.*|ALLFLAGS=-Wall %{optflags} -fPIC \\|g' \
    makefile.machine
# Don't use _smp_mflags since the build sometimes fails with it (as of 4.44)
%{__make} 7z 7za sfx


%install
%{__rm} -rf %{buildroot}

# Install binaries (7za, 7z, 7zCon.sfx and Codecs/Formats)
%{__mkdir_p} %{buildroot}%{_libexecdir}/p7zip/
%{__cp} -a bin/* %{buildroot}%{_libexecdir}/p7zip/

# Install wrapper scripts
%{__install} -D -m 0755 7z.sh  %{buildroot}%{_bindir}/7z
%{__install} -D -m 0755 7za.sh %{buildroot}%{_bindir}/7za


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog README TODO DOCS/*
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx

%files plugins
%defattr(-,root,root,-)
%doc contrib/
%{_bindir}/7z
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/Codecs/
%{_libexecdir}/p7zip/Formats/


%changelog
* Thu Mar  1 2007 Matthias Saou <http://freshrpms.net/> 4.44-2
- Remove _smp_mflags since some builds fail with suspicious errors.

* Thu Mar  1 2007 Matthias Saou <http://freshrpms.net/> 4.44-1
- Update to 4.44.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 4.42-2
- FC6 rebuild.

* Thu Jun 29 2006 Matthias Saou <http://freshrpms.net/> 4.42-1
- Update to 4.42.

* Tue May  2 2006 Matthias Saou <http://freshrpms.net/> 4.39-1
- Update to 4.39.
- Remove no longer needed gcc 4.1 patch.
- Use the gcc_4.X makefile.
- Remove RAR licensed files and RAR license itself (#190277).

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 4.30-3
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 4.30-2
- Rebuild for new gcc/glibc.
- Include gcc 4.1 patch for extra qualification errors.

* Mon Nov 28 2005 Matthias Saou <http://freshrpms.net/> 4.30-1
- Update to 4.30.

* Thu Oct 27 2005 Matthias Saou <http://freshrpms.net/> 4.29-3
- Double quote args passed inside the shell scripts, to fix #171480.

* Mon Oct 10 2005 Matthias Saou <http://freshrpms.net/> 4.29-2
- Update to 4.29.

* Sun Jun 05 2005 Dag Wieers <dag@wieers.com> - 4.20-1
- Updated to release 4.20.

* Sun Apr 10 2005 Dag Wieers <dag@wieers.com> - 4.16-1
- Moved inline scripts to %%prep stage.
- Removed quotes for $@ as it should not be necessary.

* Thu Mar 17 2005 Matthias Saou <http://freshrpms.net/> 4.14.01-1
- Spec file cleanup.
- Fix wrapper scripts : Double quote $@ for filenames with spaces to work.
- Move files from /usr/share to /usr/libexec.
- Various other minor changes.

* Mon Jan 24 2005 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.14.01

* Sun Jan 16 2005 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.14

* Mon Dec 20 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - added 7za script and moved SFX module to _datadir/name/ to allow 7za & 7z
   use it simultaneously
 - returned to plugins in separate package

* Sat Dec 18 2004 Charles Duffy <cduffy@spamcop.net>
 - upgraded to 4.13
 - added 7z (not just 7za) with a shell wrapper
 - added gcc-c++ to the BuildRequires list

* Sat Nov 20 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.12
 - added virtual file system for Midnight Commander

* Thu Nov 11 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.10
 - plugins support was dropped out from p7zip

* Sun Aug 29 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - initial release

