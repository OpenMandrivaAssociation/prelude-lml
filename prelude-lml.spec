%define _localstatedir %{_var}

Name:           prelude-lml
Version:        1.0.1
Release:        2
Summary:        Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
License:        GPLv2+
Group:          Networking/Other
URL:            http://www.prelude-ids.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-missing_rules.tar.gz
Source2:        %{name}.init
Patch1:		libprelude-1.0.0-Fix-building-with-glibc-2.16.6.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:  chrpath
BuildRequires:  gnutls-devel
BuildRequires:  pcre-devel
BuildRequires:  prelude-devel
Obsoletes:      prelude-nids < %{version}-%{release}
Provides:       prelude-nids = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected. 

%package        devel
Summary:        Libraries, includes, etc. to develop Prelude Log Analyzer Sensor
Group:          Development/C
Requires:       %{name} = %{version}

%description    devel
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected. 
The devel headers.

%prep
%setup -q -a1
%{__perl} -pi -e 's|/var/log/apache2|%{_logdir}/httpd|g' prelude-lml.conf.in
cp %{SOURCE2} %{name}.init
%patch1 -p1 

%build
%configure2_5x \
    --bindir=%{_sbindir} \
    --enable-shared \
    --disable-static \
    --enable-unsupported-rulesets \
    --with-libprelude-prefix=%{_prefix}
%make

%install
install -d %{buildroot}%{_localstatedir}/%{name}
%makeinstall_std

install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_initrddir}
install -m0755 prelude-lml.init %{buildroot}%{_initrddir}/%{name}

%{_bindir}/chrpath -d %{buildroot}%{_sbindir}/prelude-lml

rm -f %{buildroot}%{_libdir}/%{name}/*.*a

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so
%dir %{_localstatedir}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.rules
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}/ruleset
%config(noreplace) %{_sysconfdir}/%{name}/ruleset/*.rules

%files devel
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

%changelog
* Tue Aug 28 2012 Vladimir Testov <vladimir.testov@rosalab.ru> 1.0.1-1
- update to 1.0.1

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2011.0
+ Revision: 667822
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2011.0
+ Revision: 607207
- rebuild

* Sun Apr 25 2010 Funda Wang <fwang@mandriva.org> 1.0.0-1mdv2010.1
+ Revision: 538663
- new version 1.0.0

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.15-2mdv2010.1
+ Revision: 523707
- rebuilt for 2010.1

* Fri Jul 24 2009 Frederik Himpe <fhimpe@mandriva.org> 0.9.15-1mdv2010.0
+ Revision: 399132
- update to new version 0.9.15

* Fri Oct 17 2008 Funda Wang <fwang@mandriva.org> 0.9.14-1mdv2009.1
+ Revision: 294710
- New version 0.9.14

* Thu Aug 21 2008 Funda Wang <fwang@mandriva.org> 0.9.13-1mdv2009.0
+ Revision: 274721
- New version 0.9.13

* Fri Jul 18 2008 Funda Wang <fwang@mandriva.org> 0.9.12.2-1mdv2009.0
+ Revision: 238159
- New version 0.9.12.2

* Tue Jan 22 2008 Funda Wang <fwang@mandriva.org> 0.9.11-1mdv2008.1
+ Revision: 156155
- New version 0.9.11

* Tue Jan 22 2008 Funda Wang <fwang@mandriva.org> 0.9.10.1-3mdv2008.1
+ Revision: 156136
- BR prelude
- rebuild against latest gnutls

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 08 2007 David Walluck <walluck@mandriva.org> 0.9.10.1-1mdv2008.0
+ Revision: 60516
- 0.9.10.1

* Sat May 19 2007 David Walluck <walluck@mandriva.org> 0.9.10-1mdv2008.0
+ Revision: 28529
- 0.9.10
- move prelude-lml to %%{_sbindir} from %%{_bindir}
- run %%{_bindir}/chrpath -d on prelude-lml
- more explicit file permissions
- remove BuildRequires on autoconf2.5 and automake1.8

* Thu May 17 2007 David Walluck <walluck@mandriva.org> 0.9.9-2mdv2008.0
+ Revision: 27668
- version Obsoletes/Provides for prelude-nids
- don't regenerate configure
- don't echo_success when prelude-lml starts

* Wed May 02 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 0.9.9-1mdv2008.0
+ Revision: 20542
- New release 0.9.9


* Thu Dec 21 2006 David Walluck <walluck@mandriva.org> 0.9.8.1-1mdv2007.0
+ Revision: 100906
- 0.9.8.1

* Sat Dec 16 2006 David Walluck <walluck@mandriva.org> 0.9.8-1mdv2007.1
+ Revision: 98032
- 0.9.8

* Fri Nov 03 2006 David Walluck <walluck@mandriva.org> 0.9.7-7mdv2007.1
+ Revision: 76066
- fix directory

* Thu Nov 02 2006 David Walluck <walluck@mandriva.org> 0.9.7-6mdv2007.1
+ Revision: 75993
- fix lib path on x86-64

* Wed Nov 01 2006 David Walluck <walluck@mandriva.org> 0.9.7-5mdv2007.1
+ Revision: 74970
- fix _localstatedir

* Wed Nov 01 2006 David Walluck <walluck@mandriva.org> 0.9.7-4mdv2007.1
+ Revision: 74961
- call chkconfig
- add initscript

* Thu Oct 19 2006 David Walluck <walluck@mandriva.org> 0.9.7-2mdv2007.0
+ Revision: 71046
- fix build
- remove onceonly patch (fixed upstream)
- 0.9.7
- Import prelude-lml

* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdv2007.0
- 0.9.6
- added P1 (missing m4 macros)

* Fri Jun 30 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-1mdv2007.0
- rebuilt against gnutls-1.4.0
- fix deps

* Thu May 18 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-1mdk
- 0.9.5

* Mon Mar 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.4-1mdk
- 0.9.4

* Wed Feb 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-1mdk
- 0.9.3 (Major bugfixes)

* Wed Feb 01 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-2mdk
- iurt fixes

* Tue Jan 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdk
- 0.9.2 (Major feature enhancements)

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdk
- 0.9.1

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.6-4mdk
- rebuilt against openssl-0.9.8a

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.6-3mdk
- rebuilt against MySQL-4.1.x and PostgreSQL-8.x system libs
- fix conflicting declaration with MySQL-4.1.x
- fix deps

* Wed Jun 30 2004 Michael Scherer <misc@mandrake.org> 0.8.6-2mdk
- rebuild for new gcc
- [DIRM]

* Sun May 23 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.6-1mdk
- 0.8.6
- use %%configure macro
- wipe out $RPM_BUILD_ROOT before installing

