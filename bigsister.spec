#TODO
# - package bigsister --> bigsister-agent
#/TODO
%include	/usr/lib/rpm/macros.perl
Summary:	The Big Sister Network and System Monitor
Summary(pl):	Wielka Siostra - monitor sieci i systemów
Name:		bigsister
Version:	0.99b2
Release:	0.1
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/bigsister/big-sister-%{version}.tar.gz
# Source0-md5:	ef4bc0ccb9a8f91e13f40eaa198a37ca
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
Requires(post,postun):	%{name} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description server
Big Sister server part: display, status collector, alarm generator.

%description server -l pl
Czê¶æ serwerowa Big Sister: wy¶wietlaj±ca, zbieraj±ca dane i
generuj±ca alarmy.

%package ldap
Summary:	Big Sister plugin for monitoring LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP
Group:		Networking
Requires:	%{name} = %{version}-%{release}

%description ldap
Big Sister plugin for monitoring LDAP.

%description ldap -l pl
Wtyczka Big Sister do monitorowania LDAP.

%package ldap_mozilla
Summary:	Big Sister plugin for minitoring LDAP using Mozilla::LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP przy u¿yciu Mozilla::LDAP
Group:		Networking
Requires:	%{name} = %{version}-%{release}

%description ldap_mozilla
Big Sister plugin for monitoring LDAP using Mozilla::LDAP.

%description ldap_mozilla -l pl
Wtyczka Big Sister do monitorowania LDAP przy u¿yciu Mozilla::LDAP.

%package oracle
Summary:	Big Sister plugin for monitoring Oracle
Summary(pl):	Wtyczka Big Sister do monitorowania Oracle
Group:		Networking
Requires:	%{name} = %{version}-%{release}
Requires:	perl-DBD-Oracle

%description oracle
Big Sister plugin for monitoring Oracle.

%description oracle -l pl
Wtyczka Big Sister do monitorowania Oracle.

%package radius
Summary:	Big Sister plugin for monitoring radius server
Summary(pl):	Wtyczka Big Sister do monitorowania serwera radius
Group:		Networking
Requires:	%{name} = %{version}-%{release}
Requires:	perl-Authen-Radius

%description radius
Big Sister plugin for monitoring radius server.

%description radius -l pl
Wtyczka Big Sister do monitorowania serwera radius.

%package snmp
Summary:	Big Sister plugin for monitoring using SNMP
Summary(pl):	Wtyczka Big Sister do monitorowania z u¿yciem SNMP
Group:		Networking
Requires:	%{name} = %{version}-%{release}

%description snmp
Big Sister plugin for monitoring using SNMP.

%description snmp -l pl
Wtyczka Big Sister do monitorowania z u¿yciem SNMP.

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
	/usr/sbin/useradd -u 77 -d %{_var}/lib/bigsister/www \
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
%attr(755,root,root) %{_bindir}/bs*
%dir %{_usr}/share/doc/bigsister
%doc %{_usr}/share/doc/bigsister/*
%{_sysconfdir}/httpd/httpd.conf/92_bigsister.conf
%attr(755,root,root) %{_sysconfdir}/cron.weekly/bigsister_logs
%attr(750,root,bs) %{_sysconfdir}/rc.d/init.d/bigsister
%{_mandir}/man*/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/resources
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/uxmon-net
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/OV
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/syslog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/eventlog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/tests.cfg
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/bigsister
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/resources
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin/Monitor
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin/Reader
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin/BigSister
%{_usr}/share/bigsister/bin/BS_unix.pm
%{_usr}/share/bigsister/bin/BigSister/common.pm
%{_usr}/share/bigsister/bin/[CHPRSTcp]*.pm
%{_usr}/share/bigsister/bin/Monitor/*.pm
%{_usr}/share/bigsister/bin/MicroTime.pm
%{_usr}/share/bigsister/bin/Reader/*pm
%{_usr}/share/bigsister/bin/BS_win32.pm
%{_usr}/share/bigsister/bin/snmp.pm
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_start
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_start32
%attr(755,root,root) %{_usr}/share/bigsister/bin/bb_stop32
%attr(755,root,root) %{_usr}/share/bigsister/bin/report*
%attr(755,root,root) %{_usr}/share/bigsister/bin/smtpmail
%attr(755,root,root) %{_usr}/share/bigsister/bin/testers
%attr(755,root,root) %{_usr}/share/bigsister/bin/bbecho
%dir %{_usr}/share/bigsister
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

%files server
%defattr(644,root,root,755)
%dir %{_sysconfdir}/bigsister/
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bb-display.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bb_event_generator.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/bsmon_site.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/notify.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bigsister/permissions
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/reporting
%{_sysconfdir}/bigsister/reporting/*
%attr(770,root,bs) %dir %{_usr}/share/bigsister/etc
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/bsmon.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/graphtemplates
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_usr}/share/bigsister/etc/keys
%attr(750,root,bs) %dir %{_usr}/share/bigsister/etc/graphdef
%{_usr}/share/bigsister/etc/graphdef/*
%attr(750,root,bs) %dir %{_usr}/share/bigsister/etc/moduleinfo
%{_usr}/share/bigsister/etc/moduleinfo/*
%attr(750,root,bs) %dir %{_usr}/share/bigsister/etc/testdef
%{_usr}/share/bigsister/etc/testdef/*
%attr(755,root,root) %dir %{_usr}/share/bigsister/cgi
%attr(755,root,root) %{_usr}/share/bigsister/cgi/bs*
%attr(775,root,bs) %dir %{_var}/lib/bigsister
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/html
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/logs
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/logs/history
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/help
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/help/images
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/techie
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/techie/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/title_in_table
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/title_in_table/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/twocolumn
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/twocolumn/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/webadmin
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/webadmin/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/white_bg
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/white_bg/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/default
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/default/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/static_lamps
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/static_lamps/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/structured_bg
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/structured_bg/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/alt_contentsicons
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/alt_contentsicons/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/bigbro13
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/bigbro13/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/bsdoc
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/bsdoc/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/compactmenu
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/compactmenu/*
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins/frames
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/frames/*
%{_var}/lib/bigsister/www/help/*.html
%{_var}/lib/bigsister/www/help/*.jpg
%{_var}/lib/bigsister/www/help/images/*png
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin
%attr(775,root,bs) %dir %{_usr}/share/bigsister/bin/Statusmon
%{_usr}/share/bigsister/bin/Statusmon/[BDGHRSTght]*.pm
%{_usr}/share/bigsister/bin/Statusmon/bs_evgen.pm
%{_usr}/share/bigsister/bin/access.pm
%{_usr}/share/bigsister/bin/bbdisp.pm
%{_usr}/share/bigsister/bin/bscgi.pm
%{_usr}/share/bigsister/bin/display_map.pm
#te dwa tutaj powinny byc???
%{_usr}/share/bigsister/bin/BER.pm
%{_usr}/share/bigsister/bin/IPCFile.pm
#
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
%{_usr}/share/bigsister/etc/mibs.txt
%{_usr}/share/bigsister/etc/perf*
%{_usr}/share/bigsister/etc/snmp_trap
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
