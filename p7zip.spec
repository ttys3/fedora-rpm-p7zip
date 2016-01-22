Summary: Very high compression ratio file archiver
Name: p7zip
Version: 15.09
Release: 7%{?dist}
# Files under C/Compress/Lzma/ are dual LGPL or CPL
License: LGPLv2 and (LGPLv2+ or CPL)
Group: Applications/Archiving
URL: http://p7zip.sourceforge.net/
# RAR sources removed since their license is incompatible with the LGPL
#Source: http://downloads.sf.net/p7zip/p7zip_%%{version}_src_all.tar.bz2
# VERSION=
# wget http://downloads.sf.net/p7zip/p7zip_${VERSION}_src_all.tar.bz2
# tar xjvf p7zip_${VERSION}_src_all.tar.bz2
# rm -rf p7zip_${VERSION}/CPP/7zip/{Archive,Compress,Crypto}/Rar*
# rm p7zip_${VERSION}/DOC/unRarLicense.txt
# tar --numeric-owner -cjvf p7zip_${VERSION}_src_all-norar.tar.bz2 p7zip_${VERSION}
Source: p7zip_%{version}_src_all-norar.tar.bz2
Patch0: p7zip_15.09-norar_cmake.patch
Patch1: p7zip_15.09-s390.patch
Patch2: p7zip-15.09-CVE-2015-1038.patch
Patch3: p7zip_15.09-no7zG_and_7zFM.patch
Patch4: p7zip_15.09-incorrect-fsf-address.patch

BuildRequires: cmake
# BuildRequires: wxGTK3-devel wxGTK-devel # for 7zG GUI
%ifarch %{ix86}
BuildRequires: nasm
%endif
%ifarch x86_64
BuildRequires: yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary: Additional plugins for p7zip
Group: Applications/Archiving

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.


%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .norar_cmake
#Remove backups from DOC directory
rm DOC/License.txt.*
%patch1 -p1 -b .s390
%patch2 -p1 -b .CVE-2015-1038
%patch3 -p1 -b .no7zG_and_7zFM.patch
%patch4 -p1
# Move docs early so that they don't get installed by "make install" and we
# can include them in %%doc
mv DOC docs
mv ChangeLog README TODO docs/
# move license files
mv docs/License.txt docs/copying.txt .
# And fix useless executable bit while we're at it
find docs    -type f -exec chmod -x {} \;
find contrib -type f -exec chmod -x {} \;


%build
pushd CPP/7zip/CMAKE/
./generate.sh
popd
%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif
%ifarch ppc ppc64
cp -f makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif

make %{?_smp_mflags} all2 \
    OPTFLAGS="%{optflags}" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%install
make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%files
%doc docs/*
%license copying.txt License.txt
%{_bindir}/7za
%{_libexecdir}/p7zip/
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%doc contrib/
%{_bindir}/7z
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
#{_libexecdir}/p7zip/Codecs/
#{_libexecdir}/p7zip/Formats/
%{_mandir}/man1/7z.1*


%changelog
* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-7
- Split incorrect-fsf-address.patch and do not pack backup files

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-6
- Stating in License.txt file that we removed non-Free unrar code
  from sources (#190277)
- Fix incorrect fsf address in the license files.
- Add p7zip_15.09-no7zG_and_7zFM.patch in a diferent patch.

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-5
- Add license tag
- better solutions for "create unowned directory" (#917366)

* Thu Dec 03 2015 Sérgio Basto <sergio@serjux.com> - 15.09-4
- Fix CVE-2015-1038 (#1179505)

* Wed Dec 02 2015 Sérgio Basto <sergio@serjux.com> - 15.09-3
- Fix build on s390 architecture (#1286992)

* Thu Nov 12 2015 Sérgio Basto <sergio@serjux.com> - 15.09-2
- fix rhbz #917366

* Thu Nov 05 2015 Sérgio Basto <sergio@serjux.com> - 15.09-1
- Update to p7zip_15.09
- Use cmake.
- Refactor norar patch.
- Deleted: p7zip_9.20.1-execstack.patch (upstreamed)
- Deleted: p7zip_9.20.1-install.patch (upstreamed)
- Deleted: p7zip_9.20.1-nostrip.patch (upstreamed)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 9.20.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Matthias Saou <matthias@saou.eu> 9.20.1-2
- Execstack patch to fix what's wanted by the yasm code (#718778).

* Tue Jul 26 2011 Matthias Saou <matthias@saou.eu> 9.20.1-1
- Update to 9.20.1 (#688564).
- Update norar, nostrip and install patches.
- Minor clean ups : Don't use trivial macros + new email address.
- Don't require the main package from the plugins package (#690551).
- Use the any_cpu_gcc_4.X makefile for ppc* since the ppc specific one is gone.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Matthias Saou <matthias@saou.eu> 9.13-1
- Update to 9.13.
- Update norar and nostrip patches.

* Tue Dec  8 2009 Matthias Saou <matthias@saou.eu> 9.04-1
- Update to 9.04.
- Update norar patch.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <matthias@saou.eu> 4.65-1
- Update to 4.65.
- Update norar patch.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Matthias Saou <matthias@saou.eu> 4.61-1
- Update to 4.61.
- Update norar patch.
- Use asm for x86 too (nasm).

* Wed Jun 18 2008 Matthias Saou <matthias@saou.eu> 4.58-1
- Update to 4.58.
- Update norar patch.
- Update install patch.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <matthias@saou.eu> 4.51-3
- Rebuild for new BuildID feature.

* Thu Aug  9 2007 Matthias Saou <matthias@saou.eu> 4.51-2
- Update License field some more (LGPL+ to LGPLv2+).

* Sun Aug  5 2007 Matthias Saou <matthias@saou.eu> 4.51-1
- Update to 4.51.
- Update License field.

* Tue Jun 19 2007 Matthias Saou <matthias@saou.eu> 4.47-1
- Update to 4.47.
- Include now required patch to exclude removed Rar bits from makefiles.
- Switch to using "make install" for installation... so patch and hack.
- Use the asm makefile for x86_64, so build require yasm for it too.
- Add ppc64 to the main %%ifarch.
- Remove no longer included Codecs and Formats dirs (7z.so replaces them?).
- Remove our wrapper scripts, since the install script creates its own.

* Thu Mar  1 2007 Matthias Saou <matthias@saou.eu> 4.44-2
- Remove _smp_mflags since some builds fail with suspicious errors.

* Thu Mar  1 2007 Matthias Saou <matthias@saou.eu> 4.44-1
- Update to 4.44.

* Mon Aug 28 2006 Matthias Saou <matthias@saou.eu> 4.42-2
- FC6 rebuild.

* Thu Jun 29 2006 Matthias Saou <matthias@saou.eu> 4.42-1
- Update to 4.42.

* Tue May  2 2006 Matthias Saou <matthias@saou.eu> 4.39-1
- Update to 4.39.
- Remove no longer needed gcc 4.1 patch.
- Use the gcc_4.X makefile.
- Remove RAR licensed files and RAR license itself (#190277).

* Mon Mar  6 2006 Matthias Saou <matthias@saou.eu> 4.30-3
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <matthias@saou.eu> 4.30-2
- Rebuild for new gcc/glibc.
- Include gcc 4.1 patch for extra qualification errors.

* Mon Nov 28 2005 Matthias Saou <matthias@saou.eu> 4.30-1
- Update to 4.30.

* Thu Oct 27 2005 Matthias Saou <matthias@saou.eu> 4.29-3
- Double quote args passed inside the shell scripts, to fix #171480.

* Mon Oct 10 2005 Matthias Saou <matthias@saou.eu> 4.29-2
- Update to 4.29.

* Sun Jun 05 2005 Dag Wieers <dag@wieers.com> - 4.20-1
- Updated to release 4.20.

* Sun Apr 10 2005 Dag Wieers <dag@wieers.com> - 4.16-1
- Moved inline scripts to %%prep stage.
- Removed quotes for $@ as it should not be necessary.

* Thu Mar 17 2005 Matthias Saou <matthias@saou.eu> 4.14.01-1
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

