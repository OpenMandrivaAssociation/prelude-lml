%define _localstatedir %{_var}

Name:           prelude-lml
Version:        1.0.1
Release:        0
Summary:        Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
License:        GPLv2+
Group:          Networking/Other
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/%name/prelude-lml-%{version}.tar.gz
Source1:        prelude-lml-1.0.1-missing_rules.tar.gz
Source5:        prelude-lml.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:  chrpath
BuildRequires:  gnutls-devel
BuildRequires:  pcre-devel
BuildRequires:  prelude-devel

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

cp %{SOURCE5} prelude-lml.init

%build
%configure2_5x \
    --bindir=%{_sbindir} \
    --enable-shared \
    --enable-static \
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
%{_libdir}/%{name}/*.a
%attr(0755,root,root) %{_libdir}/%{name}/*.la
