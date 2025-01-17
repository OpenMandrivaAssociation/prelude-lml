%define _localstatedir %{_var}
%define _disable_ld_no_undefined 1
%define _disable_lto 1

Summary:	Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
Name:		prelude-lml
Version:	1.0.1
Release:	16
License:	GPLv2+
Group:		Networking/Other
Url:		https://www.prelude-ids.org/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-missing_rules.tar.gz
Source2:	%{name}.service
Patch1:		libprelude-1.0.0-Fix-building-with-glibc-2.16.6.patch
BuildRequires:	chrpath
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libprelude)
%rename		prelude-nids
Requires(post,preun):	rpm-helper

%description
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected.

%files
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_unitdir}/%{name}.service
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so
%dir %{_localstatedir}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.rules
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}/ruleset
%config(noreplace) %{_sysconfdir}/%{name}/ruleset/*.rules

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

#----------------------------------------------------------------------------

%package devel
Summary:	Libraries, includes, etc. to develop Prelude Log Analyzer Sensor
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected. 
The devel headers.

%files devel
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

#----------------------------------------------------------------------------

%prep
%setup -q -a1
perl -pi -e 's|/var/log/apache2|%{_logdir}/httpd|g' prelude-lml.conf.in
cp %{SOURCE2} %{name}.service
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
install -d %{buildroot}%{_unitdir}
install -m0755 prelude-lml.service %{buildroot}%{_unitdir}/%{name}.service

chrpath -d %{buildroot}%{_sbindir}/prelude-lml


