%define _localstatedir %{_var}

Name:           prelude-lml
Version:        0.9.11
Release:        %mkrel 1
Summary:        Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
License:        GPLv2+
Group:          Networking/Other
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/prelude-lml-%{version}.tar.gz
Source1:        http://www.prelude-ids.org/download/releases/prelude-lml-%{version}.tar.gz.sig
Source2:        http://www.prelude-ids.org/download/releases/prelude-lml-%{version}.tar.gz.md5
Source3:        http://www.prelude-ids.org/download/releases/prelude-lml-%{version}.tar.gz.sha1
Source4:        http://www.prelude-ids.org/download/releases/prelude-lml-%{version}.txt
Source5:        prelude-lml.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:  chrpath
BuildRequires:  libfam-devel
BuildRequires:  libgnutls-devel
BuildRequires:  libpcre-devel
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
%setup -q
%{__perl} -pi -e 's|/var/log/apache2|%{_logdir}/httpd|g' prelude-lml.conf.in

%build
%{configure2_5x} \
    --bindir=%{_sbindir} \
    --enable-shared \
    --enable-static \
    --enable-unsupported-rulesets \
    --enable-fam \
    --with-libprelude-prefix=%{_prefix} \
    --with-fam=%{_prefix}                                            
%{make}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_localstatedir}/%{name}

%{makeinstall_std}

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{name}

%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} -a %{SOURCE5} %{buildroot}%{_initrddir}/%{name}

%{_bindir}/chrpath -d %{buildroot}%{_sbindir}/prelude-lml

%clean
%{__rm} -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(0644,root,root,0755)
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
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/*.a
%attr(0755,root,root) %{_libdir}/%{name}/*.la
