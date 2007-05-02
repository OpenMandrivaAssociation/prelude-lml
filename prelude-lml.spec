%define _localstatedir %{_var}

Name:           prelude-lml
Version:        0.9.9
Release:        %mkrel 1
Summary:        Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
License:        GPL
Group:          Networking/Other
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
Source1:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz.sig
Source2:        prelude-lml.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:  automake1.8
BuildRequires:  autoconf2.5
BuildRequires:  libprelude-devel => 0.9.3
BuildRequires:  libpcre-devel
BuildRequires:  libfam-devel
BuildRequires:  libgnutls-devel
Provides:       prelude-nids
Obsoletes:      prelude-nids
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%{__rm} -f configure
%{_bindir}/libtoolize --copy --force; aclocal-1.8 -I m4 -I libmissing/m4; automake-1.8 --add-missing --copy --foreign; autoconf

%{configure2_5x} \
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
%{__cp} -a %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/ruleset
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.rules
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/ruleset/*.rules
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_localstatedir}/lib/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}

%files devel
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog HACKING.README NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/*.a
%{_libdir}/%{name}/*.la


