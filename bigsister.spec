%include	/usr/lib/rpm/macros.perl
Summary:	The Big Sister Network and System Monitor
Summary(pl):	Wielka Siostra - monitor sieci i system�w
Name:		bigsister
Version:	0.98c8
Release:	0.4
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/%{name}/big-sister-%{version}.tar.gz
# Source0-md5:	44b1dfed1f4ce8029fec2ffe16002c68
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch1:		%{name}-memory.patch
Patch2:		%{name}-logfile-notranslated.patch
Patch3:		%{name}-dubleinstall.patch
Patch4:		%{name}-not_user_check.patch
URL:		http://bigsister.graeff.com/
BuildRequires:	perl-libnet
BuildRequires:	perl-libwww
BuildRequires:	rpm-perlprov >= 4.0.2-104
BuildRequires:	rpmbuild(macros) >= 1.159
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,preun):	/sbin/chkconfig
Provides:	group(bs)
Provides:	user(bs)
Provides:	perl(Monitor::uxmon)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# 'common' and 'parse' are files provided with bigsister
# perl-GD is optional (for generating maps)
# perl-FCGI is recommended, but not required
# perl-SNMP_Session is requires only for SNMP checks, but snmp.pm module
# (which tests if SNMP_Session exists) must be present in base package
%define		_noautoreq	'perl(common)' 'perl(parse)' 'perl(GD)' 'perl(FCGI)' 'perl(SNMP_Session)' 'perl(SNMP_util)' 'perl(BER)'

%description
Big Sister - a Big Brother clone.

%description -l pl
Wielka Siostra - klon Wielkiego Brata.

%package server
Summary:	Big Sister server
Summary(pl):	Serwer Big Sister
Group:		Networking
Requires(post,postun):	%{name} = %{version}
Requires:	%{name} = %{version}

%description server
Big Sister server part: display, status collector, alarm generator.

%description server -l pl
Cz�� serwerowa Big Sister: wy�wietlaj�ca, zbieraj�ca dane i
generuj�ca alarmy.

%package ldap
Summary:	Big Sister plugin for monitoring LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP
Group:		Networking
Requires:	%{name} = %{version}

%description ldap
Big Sister plugin for monitoring LDAP.

%description ldap -l pl
Wtyczka Big Sister do monitorowania LDAP.

%package ldap_mozilla
Summary:	Big Sister plugin for minitoring LDAP using Mozilla::LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP przy u�yciu Mozilla::LDAP
Group:		Networking
Requires:	%{name} = %{version}

%description ldap_mozilla
Big Sister plugin for monitoring LDAP using Mozilla::LDAP.

%description ldap_mozilla -l pl
Wtyczka Big Sister do monitorowania LDAP przy u�yciu Mozilla::LDAP.

%package oracle
Summary:	Big Sister plugin for monitoring Oracle
Summary(pl):	Wtyczka Big Sister do monitorowania Oracle
Group:		Networking
Requires:	%{name} = %{version}
Requires:	perl-DBD-Oracle

%description oracle
Big Sister plugin for monitoring Oracle.

%description oracle -l pl
Wtyczka Big Sister do monitorowania Oracle.

%package radius
Summary:	Big Sister plugin for monitoring radius server
Summary(pl):	Wtyczka Big Sister do monitorowania serwera radius
Group:		Networking
Requires:	%{name} = %{version}
Requires:	perl-Authen-Radius

%description radius
Big Sister plugin for monitoring radius server.

%description radius -l pl
Wtyczka Big Sister do monitorowania serwera radius.

%package snmp
Summary:	Big Sister plugin for monitoring using SNMP
Summary(pl):	Wtyczka Big Sister do monitorowania z u�yciem SNMP
Group:		Networking
Requires:	%{name} = %{version}

%description snmp
Big Sister plugin for monitoring using SNMP.

%description snmp -l pl
Wtyczka Big Sister do monitorowania z u�yciem SNMP.

%prep
%setup -q -n bs-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
./configure \
	--with-user=bs \
	--enable-FHS 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}{/rc.d/init.d,/sysconfig,/httpd/httpd.conf}

%{__make} install-server install-client install-reporting install-modules install-doc \
	DESTDIR=$RPM_BUILD_ROOT
#TODO
# - change path (FHS) in makefile or configure
#/TODO
mv -f	$RPM_BUILD_ROOT%{_var}/lib/bigsister/www \
	$RPM_BUILD_ROOT%{_usr}/share/bigsister/www
ln -sf	%{_usr}/share/bigsister/www \
	$RPM_BUILD_ROOT%{_var}/lib/bigsister/www


mv -f	$RPM_BUILD_ROOT%{_usr}/share/bigsister/etc \
	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/adm
ln -sf	%{_sysconfdir}/bigsister/adm \
	$RPM_BUILD_ROOT%{_usr}/share/bigsister/etc

mv -f	$RPM_BUILD_ROOT%{_sbindir}/* \
	$RPM_BUILD_ROOT%{_bindir}
rm -rf	$RPM_BUILD_ROOT%{_sbindir}

rm -rf	$RPM_BUILD_ROOT%{_sysconfdir}/init.d

mv -f	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/httpd.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/92_bigsister.conf 

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid bs`" ]; then
	if [ "`/usr/bin/getgid bs`" != 77 ]; then
		echo "Error: group bs doesn't have gid=77. Correct this before installing bigsister." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 77 bs
fi
if [ -n "`/bin/id -u bs 2>/dev/null`" ]; then
	if [ "`/bin/id -u bs`" != "77" ]; then
		echo "Error: user bs doesn't have uid=77. Correct this before installing bigsister." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 77 -d %{_usr}/share/bigsister/www \
	-s /bin/false -c "Big Sister" -g bs bs 1>&2
fi

%post
/sbin/chkconfig --add bigsister
if [ -f /var/lock/subsys/bigsister ]; then
	/etc/rc.d/init.d/bigsister restart >&2
else
	echo "Run \"/etc/rc.d/init.d/bigsister start\" to start Big Sister." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/bigsister ]; then
		/etc/rc.d/init.d/bigsister stop >&2
	fi
	/sbin/chkconfig --del bigsister
fi

%postun
if [ "$1" = "0" ]; then
	%userremove bs
	%groupremove bs
fi

%post server
if [ -f /var/lock/subsys/bigsister ]; then
	/etc/rc.d/init.d/bigsister restart >&2
else
	echo "Run \"/etc/rc.d/init.d/bigsister start\" to start Big Sister." >&2
fi

%postun server
if [ -f /var/lock/subsys/bigsister ]; then
	/etc/rc.d/init.d/bigsister restart >&2
else
	echo "Run \"/etc/rc.d/init.d/bigsister start\" to start Big Sister." >&2
fi

%files
%defattr(644,root,root,755)
%dir %{_usr}/share/doc/bigsister
%doc %{_usr}/share/doc/bigsister/*
%{_sysconfdir}/httpd/httpd.conf/92_bigsister.conf
%{_sysconfdir}/cron.weekly/bigsister_logs
%attr(750,root,bs) %{_sysconfdir}/rc.d/init.d/bigsister
%{_mandir}/man*/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/resources
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/uxmon-net
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/OV
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/syslog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/eventlog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/tests.cfg
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/bigsister
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/resources
%dir %{_usr}/share/bigsister/bin
%{_usr}/share/bigsister/bin/BS_unix.pm
%{_usr}/share/bigsister/bin/BigSister/common.pm
%{_usr}/share/bigsister/bin/[CHPRSTcp]*.pm
%{_usr}/share/bigsister/bin/Monitor/*.pm
%{_usr}/share/bigsister/bin/MicroTime.pm
%{_usr}/share/bigsister/bin/Reader/*pm
%{_usr}/share/bigsister/bin/BS_win32.pm
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_start
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_start32
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_stop32
%attr(755,root,root) %{_bindir}/bsmodule
%attr(755,root,root) %{_usr}/share/bigsister/bin/report*
%attr(755,root,root) %{_usr}/share/bigsister/bin/smtpmail
%attr(755,root,root) %{_usr}/share/bigsister/bin/testers
%{_usr}/share/bigsister/bin/snmp.pm
%attr(755,root,root) %{_usr}/share/bigsister/bin/bbecho
%attr(775,root,bs) %{_bindir}/bsadmin
%dir %{_usr}/share/bigsister/uxmon
%dir %{_usr}/share/bigsister/uxmon/Config
%{_usr}/share/bigsister/uxmon/Config/_perflib
%{_usr}/share/bigsister/uxmon/Config/noFQDN
%{_usr}/share/bigsister/uxmon/Config/[FObdfimpty]*
%{_usr}/share/bigsister/uxmon/Config/_[ert]*
%{_usr}/share/bigsister/uxmon/Config/c[op]*
%{_usr}/share/bigsister/uxmon/Config/http
%{_usr}/share/bigsister/uxmon/Config/lo*
%{_usr}/share/bigsister/uxmon/Config/n[Fefln]*
%{_usr}/share/bigsister/uxmon/Config/ntp
%{_usr}/share/bigsister/uxmon/Config/r[ep]*
%{_usr}/share/bigsister/uxmon/Config/s[mty]*
%dir %{_usr}/share/bigsister/uxmon/Monitor
%{_usr}/share/bigsister/uxmon/Monitor/PerfLib.pm
%{_usr}/share/bigsister/uxmon/Monitor/eventlog.pm
%{_usr}/share/bigsister/uxmon/Monitor/[EMOTb-dfmpt-u]*
%{_usr}/share/bigsister/uxmon/Monitor/l[ox]*
%{_usr}/share/bigsister/uxmon/Monitor/r[ep]*
%{_usr}/share/bigsister/uxmon/Monitor/s[aty]*
%dir %{_usr}/share/bigsister/uxmon/Requester
%{_usr}/share/bigsister/uxmon/Requester/[A-Za-rt-z]*
%{_usr}/share/bigsister/uxmon/Requester/s[oy]*
%attr(755,root,root) %{_usr}/share/bigsister/uxmon/uxmon
%{_usr}/share/bigsister/uxmon/uxmon-rules.pl
%{_usr}/share/bigsister/www

%files server
%defattr(644,root,root,755)
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bb-display.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bb_event_generator.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bsmon_site.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/notify.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/permissions
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/reporting
%{_sysconfdir}/bigsister/reporting/*
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/bsmon.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/graphtemplates
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/adm/keys
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/adm/graphdef
%{_sysconfdir}/bigsister/adm/graphdef/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/adm/moduleinfo
%{_sysconfdir}/bigsister/adm/moduleinfo/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/adm/testdef
%{_sysconfdir}/bigsister/adm/testdef/*
%attr(755,root,root) %{_usr}/share/bigsister/cgi/bs*
%attr(775,root,bs) %dir %{_usr}/share/bigsister/www/html
%attr(775,root,bs) %dir %{_usr}/share/bigsister/www/logs
%attr(775,root,bs) %dir %{_usr}/share/bigsister/www/logs/history
%attr(775,root,bs) %dir %{_usr}/share/bigsister/www/help
%attr(775,root,bs) %dir %{_usr}/share/bigsister/www/help/images
%{_usr}/share/bigsister/www/skins
%{_usr}/share/bigsister/www/help/*.html
%{_usr}/share/bigsister/www/help/*.jpg
%{_usr}/share/bigsister/www/help/images/*png
%dir %{_usr}/share/bigsister/bin/Statusmon
%{_usr}/share/bigsister/bin/Statusmon/[BDGHRSTght]*.pm
%{_usr}/share/bigsister/bin/Statusmon/bs_evgen.pm
%{_usr}/share/bigsister/bin/access.pm
%{_usr}/share/bigsister/bin/bbdisp.pm
%{_usr}/share/bigsister/bin/bscgi.pm
%{_usr}/share/bigsister/bin/display_map.pm
%attr(755,root,root) %{_usr}/share/bigsister/bin/bbd
%attr(755,root,root) %{_usr}/share/bigsister/bin/bsmon
%attr(755,root,root) %{_usr}/share/bigsister/bin/log_mail
%attr(755,root,root) %{_usr}/share/bigsister/bin/notify
%attr(755,root,root) %{_usr}/share/bigsister/bin/compile_skin
%attr(755,root,root) %{_usr}/share/bigsister/bin/page_meridian

%files ldap
%defattr(644,root,root,755)
%{_usr}/share/bigsister/uxmon/Config/ldap
%{_usr}/share/bigsister/uxmon/Monitor/ldap.pm

%files ldap_mozilla
%defattr(644,root,root,755)
%{_usr}/share/bigsister/uxmon/Config/ldap_mozilla
%{_usr}/share/bigsister/uxmon/Monitor/ldap_mozilla.pm

%files oracle
%defattr(644,root,root,755)
%{_usr}/share/bigsister/uxmon/Config/oracle
%{_usr}/share/bigsister/uxmon/Monitor/oracle.pm

%files radius
%defattr(644,root,root,755)
%{_usr}/share/bigsister/uxmon/Config/radius
%{_usr}/share/bigsister/uxmon/Monitor/radius.pm

%files snmp
%defattr(644,root,root,755)
%{_sysconfdir}/bigsister/adm/mibs.txt
%{_sysconfdir}/bigsister/adm/perf*
%{_sysconfdir}/bigsister/adm/snmp_trap
%attr(755,root,root) %{_usr}/share/bigsister/bin/bstrapd
%{_usr}/share/bigsister/bin/snmp.pm
%{_usr}/share/bigsister/uxmon/Config/_snmp
%{_usr}/share/bigsister/uxmon/Config/_storage
%{_usr}/share/bigsister/uxmon/Config/atmport
%{_usr}/share/bigsister/uxmon/Config/caty
%{_usr}/share/bigsister/uxmon/Config/etherport
%{_usr}/share/bigsister/uxmon/Config/hub
%{_usr}/share/bigsister/uxmon/Config/novell
%{_usr}/share/bigsister/uxmon/Config/nt
%{_usr}/share/bigsister/uxmon/Config/snmp
%{_usr}/share/bigsister/uxmon/Config/snmp_trap
%{_usr}/share/bigsister/uxmon/Config/snmpvar
%{_usr}/share/bigsister/uxmon/Config/software
%{_usr}/share/bigsister/uxmon/Config/ups
%{_usr}/share/bigsister/uxmon/Config/qmqueue
%{_usr}/share/bigsister/uxmon/Config/sendmail
%{_usr}/share/bigsister/uxmon/Monitor/atmport.pm
%{_usr}/share/bigsister/uxmon/Monitor/etherport.pm
%{_usr}/share/bigsister/uxmon/Monitor/snmp.pm
%{_usr}/share/bigsister/uxmon/Monitor/qmqueue.pm
%{_usr}/share/bigsister/uxmon/Monitor/sendmail.pm
%{_usr}/share/bigsister/uxmon/Monitor/snmp_trap.pm
%{_usr}/share/bigsister/uxmon/Requester/snmp.pm
