Summary:	Downloads Certificate Revocation Lists
Name:		fetch-crl
Version:	3.0.8
Release:	1
License:	ASL 2.0
Group:		Applications/System
URL:		http://www.nikhef.nl/grid/gridwiki/index.php/FetchCRL3
Source0:	http://dist.eugridpma.info/distribution/util/fetch-crl3/%{name}-%{version}.tar.gz
# Source0-md5:	0c255931d05d46ed444d76438df29dd5
Source1:	%{name}.crontab
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	crondaemon
Requires:	openssl
Obsoletes:	fetch-crl3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This tool and associated cron entry ensure that Certificate Revocation
Lists (CRLs) are periodically retrieved from the web sites of the
respective Certification Authorities. It assumes that the installed CA
files follow the hash.crl_url convention.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}.d,/etc/{cron.d,rc.d/init.d}}
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_usr} \
	ETC=$RPM_BUILD_ROOT%{_sysconfdir} \
	CACHE=$RPM_BUILD_ROOT%{_var}/cache

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

# Remove some files that have been duplicated as docs.
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README fetch-crl.cnf.example
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%dir %{_var}/cache/%{name}
