# TODO
# - pldize initscript
%include	/usr/lib/rpm/macros.perl
Summary:	Downloads Certificate Revocation Lists
Name:		fetch-crl
Version:	3.0.7
Release:	1
License:	ASL 2.0
Group:		Applications/System
URL:		http://www.nikhef.nl/grid/gridwiki/index.php/FetchCRL3
Source0:	http://dist.eugridpma.info/distribution/util/fetch-crl3/%{name}-%{version}.tar.gz
# Source0-md5:	d15773dd28110214f7d5302f073e97c1
BuildRequires:	rpm-perlprov >= 4.1-13
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

install -p fetch-crl-cron.init $RPM_BUILD_ROOT%{_initrddir}/%{name}-cron
install -p fetch-crl-boot.init $RPM_BUILD_ROOT%{_initrddir}/%{name}-boot
cp -p fetch-crl-cron.cron $RPM_BUILD_ROOT/etc/cron.d/%{name}

# Remove some files that have been duplicated as docs.
rm -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}-cron
/sbin/chkconfig --add %{name}-boot

%preun
if [ $1 = 0 ]; then
	%service %{name}-cron stop
	%service %{name}-boot stop
	/sbin/chkconfig --del %{name}-cron
	/sbin/chkconfig --del %{name}-boot
fi

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README fetch-crl.cnf.example
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/fetch-crl-boot
%attr(754,root,root) /etc/rc.d/init.d/fetch-crl-cron
%{_mandir}/man8/%{name}.8*
%dir %{_var}/cache/%{name}
