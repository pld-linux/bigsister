%include /usr/lib/rpm/macros.perl
Summary:	The Big Sister Network and System Monitor
Summary(pl):	Wielka Siostra - monitor sieci i systemów
Name:		bigsister
Version:	0.98c8
Release:	0.4
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/%{name}/big-sister-%{version}.tar.gz
# Source0-md5:	44b1dfed1f4ce8029fec2ffe16002c68
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-memory.patch
Patch2:		%{name}-logfile-notranslated.patch
Patch3:		%{name}-dubleinstall.patch
URL:		http://bigsister.graeff.com/
BuildRequires:	fhs-compliance
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

%define		_prefix		/usr/lib/bs
%define		_htmldir	/srv/httpd/html
%define		_htmlsubdir	%{_htmldir}/bs
%define		_cgidir		/srv/httpd/cgi-bin
%define		_vardir		/var/lib/bs
%define		_etcdir		%{_sysconfdir}/bs

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
Czê¶æ serwerowa Big Sister: wy¶wietlaj±ca, zbieraj±ca dane i
generuj±ca alarmy.

%package ldap
Summary:	Big Sister plugin for minitoring LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP
Group:		Networking
Requires:	%{name} = %{version}

%description ldap
Big Sister plugin for monitoring LDAP.

%description ldap -l pl
Wtyczka Big Sister do monitorowania LDAP.

%package ldap_mozilla
Summary:	Big Sister plugin for minitoring LDAP using Mozilla::LDAP
Summary(pl):	Wtyczka Big Sister do monitorowania LDAP przy u¿yciu Mozilla::LDAP
Group:		Networking
Requires:	%{name} = %{version}

%description ldap_mozilla
Big Sister plugin for monitoring LDAP using Mozilla::LDAP.

%description ldap_mozilla -l pl
Wtyczka Big Sister do monitorowania LDAP przy u¿yciu Mozilla::LDAP.

%package oracle
Summary:	Big Sister plugin for minitoring Oracle
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
Summary(pl):	Wtyczka Big Sister do monitorowania z u¿yciem SNMP
Group:		Networking
Requires:	%{name} = %{version}

%description snmp
Big Sister plugin for monitoring using SNMP.

%description snmp -l pl
Wtyczka Big Sister do monitorowania z u¿yciem SNMP.

%prep
%setup -q -n bs-0.98c8
%patch0 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --with-user=bs \
	--prefix=/usr/lib/bs \
	--with-cgi=../cgi-bin
#%{__make}

#%{__perl} -pi -e 's/^(bin:.*)check/$1/;s/^(install-.*) bin/$1/' Makefile
#%{__make} bin \
#	USER=bs \
#	DEST=%{_libdir}/bs \
#	CGIPATH=/cgi-bin \
#	WEBROOT=/bs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_cgidir},%{_htmldir},%{_etcdir},/etc/sysconfig,%{_vardir}}

#install -d $RPM_BUILD_ROOT{%{_htmldir},%{_cgidir},%{_vardir},%{_etcdir}} \
#	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install-server install-client install-reporting install-modules install-doc \
	DESTDIR=$RPM_BUILD_ROOT
#	USER=`id -nu` \
#	DEST=$RPM_BUILD_ROOT%{_libdir}/bs \

%define         _prefix         /usr

install -d $RPM_BUILD_ROOT%{_mandir}
mv -f $RPM_BUILD_ROOT%{_libdir}/bs/www $RPM_BUILD_ROOT%{_htmlsubdir}
ln -sf %{_htmlsubdir} $RPM_BUILD_ROOT%{_libdir}/bs/www
rmdir $RPM_BUILD_ROOT%{_libdir}/bs/var
ln -sf %{_vardir} $RPM_BUILD_ROOT%{_libdir}/bs/var
mv -f $RPM_BUILD_ROOT%{_libdir}/bs/{etc,adm} $RPM_BUILD_ROOT%{_etcdir}
ln -sf %{_etcdir}/adm $RPM_BUILD_ROOT%{_libdir}/bs/adm
ln -sf %{_etcdir}/etc $RPM_BUILD_ROOT%{_libdir}/bs/etc
#
mv -f $RPM_BUILD_ROOT%{_libdir}/bs/cgi/{bsgraph,bshistory,bsweb*} \
	$RPM_BUILD_ROOT%{_cgidir}
mv -f $RPM_BUILD_ROOT%{_libdir}/bs/man/man1 $RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bigsister
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/bigsister
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
	/usr/sbin/useradd -u 77 -d /var/lib/bs -s /bin/false \
		-c "Big Sister" -g bs bs 1>&2
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
%doc BUGS CHANGES.PLAINTEXT CONFIG HOWTO PROTOCOL Q+A README SNMP_AGENT TODO UPDATE
%{_mandir}/man*/*
%attr(750,root,bs) %dir %{_etcdir}
%attr(750,root,bs) %dir %{_etcdir}/adm
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/resources
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/uxmon-net
%attr(750,root,bs) %dir %{_etcdir}/etc
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/OV
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/resources
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/syslog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/eventlog
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/tests.cfg
%attr(754,root,root) /etc/rc.d/init.d/bigsister
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/bigsister
%attr(771,root,bs) %{_vardir}
%dir %{_libdir}/bs
%{_libdir}/bs/adm
%dir %{_libdir}/bs/bin
%{_libdir}/bs/bin/BS_unix.pm
%{_libdir}/bs/bin/BigSister/common.pm
%{_libdir}/bs/bin/[CHPRSTcp]*.pm
%{_libdir}/bs/bin/Monitor/*.pm
%{_libdir}/bs/bin/MicroTime.pm
%{_libdir}/bs/bin/Reader/*pm
%attr(755,root,root) %{_libdir}/bs/bin/bb_start
%attr(755,root,root) %{_libdir}/bs/bin/bsmodule
%attr(755,root,root) %{_libdir}/bs/bin/report*
%attr(755,root,root) %{_libdir}/bs/bin/smtpmail
%attr(755,root,root) %{_libdir}/bs/bin/testers
%{_libdir}/bs/bin/snmp.pm
%attr(755,root,root) %{_libdir}/bs/bin/bbecho
%attr(775,root,bs) %{_libdir}/bs/bin/bsadmin
%{_libdir}/bs/etc
%dir %{_libdir}/bs/uxmon
%dir %{_libdir}/bs/uxmon/Config
%{_libdir}/bs/uxmon/Config/_perflib
%{_libdir}/bs/uxmon/Config/noFQDN
%{_libdir}/bs/uxmon/Config/[FObdfimpty]*
%{_libdir}/bs/uxmon/Config/_[ert]*
%{_libdir}/bs/uxmon/Config/c[op]*
%{_libdir}/bs/uxmon/Config/http
%{_libdir}/bs/uxmon/Config/lo*
%{_libdir}/bs/uxmon/Config/n[Fefln]*
%{_libdir}/bs/uxmon/Config/ntp
%{_libdir}/bs/uxmon/Config/r[ep]*
%{_libdir}/bs/uxmon/Config/s[mty]*
%dir %{_libdir}/bs/uxmon/Monitor
%{_libdir}/bs/uxmon/Monitor/PerfLib.pm
%{_libdir}/bs/uxmon/Monitor/eventlog.pm
%{_libdir}/bs/uxmon/Monitor/[EMOTb-dfmpt-u]*
%{_libdir}/bs/uxmon/Monitor/l[ox]*
%{_libdir}/bs/uxmon/Monitor/r[ep]*
%{_libdir}/bs/uxmon/Monitor/s[aty]*
%dir %{_libdir}/bs/uxmon/Requester
%{_libdir}/bs/uxmon/Requester/Requester.pm
%{_libdir}/bs/uxmon/Requester/[A-Za-rt-z]*
%{_libdir}/bs/uxmon/Requester/s[oy]*
%attr(755,root,root) %{_libdir}/bs/uxmon/uxmon
%{_libdir}/bs/uxmon/uxmon-rules.pl
%{_libdir}/bs/var
%{_libdir}/bs/www


%files server
%defattr(644,root,root,755)
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/bb-display.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/bb_event_generator.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/bsmon_site.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/notify.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/adm/permissions
%attr(750,root,bs) %dir %{_etcdir}/adm/reporting
%{_etcdir}/adm/reporting/*
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/bsmon.cfg
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/graphtemplates
%attr(660,root,bs) %config(noreplace) %verify(not size mtime md5) %{_etcdir}/etc/keys
%attr(750,root,bs) %dir %{_etcdir}/etc/graphdef
%{_etcdir}/etc/graphdef/*
%attr(750,root,bs) %dir %{_etcdir}/etc/moduleinfo
%{_etcdir}/etc/moduleinfo/*
%attr(750,root,bs) %dir %{_etcdir}/etc/testdef
%{_etcdir}/etc/testdef/*
%attr(755,root,root) %{_cgidir}/bs*
%attr(775,root,bs) %dir %{_htmlsubdir}
%attr(775,root,bs) %dir %{_htmlsubdir}/html
%attr(775,root,bs) %dir %{_htmlsubdir}/logs
%attr(775,root,bs) %dir %{_htmlsubdir}/logs/history
%attr(775,root,bs) %dir %{_htmlsubdir}/help
%attr(775,root,bs) %dir %{_htmlsubdir}/help/images
%{_htmlsubdir}/skins
%{_htmlsubdir}/help/*.html
%{_htmlsubdir}/help/*.jpg
%{_htmlsubdir}/help/images/*png
%dir %{_libdir}/bs/bin/Statusmon
%{_libdir}/bs/bin/Statusmon/[BDGHRSTght]*.pm
%{_libdir}/bs/bin/Statusmon/bs_evgen.pm
%{_libdir}/bs/bin/access.pm
%{_libdir}/bs/bin/bbdisp.pm
%{_libdir}/bs/bin/bscgi.pm
%{_libdir}/bs/bin/display_map.pm
%attr(755,root,root) %{_libdir}/bs/bin/bbd
%attr(755,root,root) %{_libdir}/bs/bin/bsmon
%attr(755,root,root) %{_libdir}/bs/bin/log_mail
%attr(755,root,root) %{_libdir}/bs/bin/notify
%attr(755,root,root) %{_libdir}/bs/bin/compile_skin
%attr(755,root,root) %{_libdir}/bs/bin/page_meridian

%files ldap
%defattr(644,root,root,755)
%{_libdir}/bs/uxmon/Config/ldap
%{_libdir}/bs/uxmon/Monitor/ldap.pm

%files ldap_mozilla
%defattr(644,root,root,755)
%{_libdir}/bs/uxmon/Config/ldap_mozilla
%{_libdir}/bs/uxmon/Monitor/ldap_mozilla.pm

%files oracle
%defattr(644,root,root,755)
%{_libdir}/bs/uxmon/Config/oracle
%{_libdir}/bs/uxmon/Monitor/oracle.pm

%files radius
%defattr(644,root,root,755)
%{_libdir}/bs/uxmon/Config/radius
%{_libdir}/bs/uxmon/Monitor/radius.pm

%files snmp
%defattr(644,root,root,755)
%{_etcdir}/etc/mibs.txt
%{_etcdir}/etc/perf*
%{_etcdir}/etc/snmp_trap
%attr(755,root,root) %{_libdir}/bs/bin/bstrapd
%{_libdir}/bs/bin/snmp.pm
%{_libdir}/bs/uxmon/Config/_snmp
%{_libdir}/bs/uxmon/Config/_storage
%{_libdir}/bs/uxmon/Config/atmport
%{_libdir}/bs/uxmon/Config/caty
%{_libdir}/bs/uxmon/Config/etherport
%{_libdir}/bs/uxmon/Config/hub
%{_libdir}/bs/uxmon/Config/novell
%{_libdir}/bs/uxmon/Config/nt
%{_libdir}/bs/uxmon/Config/snmp
%{_libdir}/bs/uxmon/Config/snmp_trap
%{_libdir}/bs/uxmon/Config/snmpvar
%{_libdir}/bs/uxmon/Config/software
%{_libdir}/bs/uxmon/Config/ups
%{_libdir}/bs/uxmon/Config/qmqueue
%{_libdir}/bs/uxmon/Config/sendmail
%{_libdir}/bs/uxmon/Monitor/atmport.pm
%{_libdir}/bs/uxmon/Monitor/etherport.pm
%{_libdir}/bs/uxmon/Monitor/snmp.pm
%{_libdir}/bs/uxmon/Monitor/qmqueue.pm
%{_libdir}/bs/uxmon/Monitor/sendmail.pm
%{_libdir}/bs/uxmon/Monitor/snmp_trap.pm
%{_libdir}/bs/uxmon/Requester/snmp.pm
