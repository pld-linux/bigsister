#TODO
# - corect path for files and directory in /etc/bigsister/etc/* - Patch5 (FHS)
# - security for webpage and admin page
#/TODO
%include	/usr/lib/rpm/macros.perl
Summary:	The Big Sister Network and System Monitor
Summary(pl):	Wielka Siostra - monitor sieci i systemów
Name:		bigsister
Version:	0.99b2
Release:	0.2
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
#Patch5:		%{name}-path_to_adm.patch
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
Requires:	nscd
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
Requires:	perl-Net-SNMP
Requires:	perl-GD-Graph-Map
Requires:	perl-Net-SMTP-Receive
Requires:	perl-libwww
Requires:	rrdtool
Requires:	perl-FCGI

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
Requires:	apache
Requires:	apache-mod_perl


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
Requires:	perl-SNMP


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
#%patch5 -p1

%build
./configure \
	--with-user=bs \
	--enable-FHS
#	--with-url=/bs
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc{/rc.d/init.d,/sysconfig,/httpd/httpd.conf,/bigsister/etc},%{_var}/lib/bigsister/www/graphs}

%{__make} install-server install-client install-reporting \
	install-modules install-doc DESTDIR=$RPM_BUILD_ROOT
#install-win32
mv -f	$RPM_BUILD_ROOT%{_sbindir}/* \
	$RPM_BUILD_ROOT%{_bindir}
rm -rf	$RPM_BUILD_ROOT%{_sbindir}

rm -rf	$RPM_BUILD_ROOT/etc/init.d

mv -f	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/httpd.conf \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/92_bigsister.conf 

#TODO 
# -add patch and e-mail to author
# -corect directory in /etc/bigsister and /etc/bigsister/etc
# 

mv -f	$RPM_BUILD_ROOT%{_datadir}/bigsister/etc/* \
	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc
cd $RPM_BUILD_ROOT%{_datadir}/bigsister
#ln -sf	%{_sysconfdir}/bigsister/etc etc 
ln -sf	%{_var}/lib/bigsister/www www
ln -sf	%{_sysconfdir}/bigsister/etc etc
#cd $RPM_BUILD_ROOT%{_var}/lib/bigsister
#ln -sf	%{_var}/lib/bigsister/www www

#correct path in files
cat $RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files | sed -e "s#$RPM_BUILD_ROOT##g" | sed -e "s#%{_datadir}/bigsister/etc#%{_sysconfdir}/bigsister/etc#g" > $RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files.new
rm -rf	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files
mv -f	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files.new \
	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files

#sed -e "s/\$RPM_BUILD_ROOT//g" \
#	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/bsmon.cfg
#sed -e "s/\$RPM_BUILD_ROOT//g" \
#	$RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/resources

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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

%{_datadir}/bigsister/bin/compile_skin webadmin
%{_datadir}/bigsister/bin/compile_skin static_lamps
%{_datadir}/bigsister/bin/compile_skin structured_bg
%{_datadir}/bigsister/bin/compile_skin alt_contentsicons
%{_datadir}/bigsister/bin/compile_skin bigbro13
%{_datadir}/bigsister/bin/compile_skin bsdoc
%{_datadir}/bigsister/bin/compile_skin compactmenu
%{_datadir}/bigsister/bin/compile_skin frames
%{_datadir}/bigsister/bin/compile_skin techie
%{_datadir}/bigsister/bin/compile_skin title_in_table
%{_datadir}/bigsister/bin/compile_skin twocolumn
%{_datadir}/bigsister/bin/compile_skin default
%{_datadir}/bigsister/bin/compile_skin white_bg


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
%doc %{_datadir}/doc/bigsister 
%{_sysconfdir}/httpd/httpd.conf/92_bigsister.conf
%attr(755,root,root) /etc/cron.weekly/bigsister_logs
%attr(754,root,root) /etc/rc.d/init.d/bigsister
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bigsister
%{_mandir}/man*/*
%attr(775,root,bs) %dir %{_sysconfdir}/bigsister
%attr(775,root,bs) %dir %{_sysconfdir}/bigsister/etc
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/resources
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/OV
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/syslog
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/eventlog
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/tests.cfg
%attr(644,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/resources
%attr(640,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/uxmon-net
%dir %{_datadir}/bigsister
%{_datadir}/bigsister/etc
%dir %{_datadir}/bigsister/bin
%dir %{_datadir}/bigsister/bin/Monitor
%dir %{_datadir}/bigsister/bin/Reader
%dir %{_datadir}/bigsister/bin/BigSister
%{_datadir}/bigsister/bin/BS_unix.pm
%{_datadir}/bigsister/bin/BigSister/common.pm
%{_datadir}/bigsister/bin/[CHPRSTcp]*.pm
%{_datadir}/bigsister/bin/Monitor/*.pm
%{_datadir}/bigsister/bin/MicroTime.pm
%{_datadir}/bigsister/bin/Reader/*pm
%{_datadir}/bigsister/bin/BS_win32.pm
%attr(755,root,root) %{_datadir}/bigsister/bin/bb_start
%attr(755,root,root) %{_datadir}/bigsister/bin/bb_start32
%attr(755,root,root) %{_datadir}/bigsister/bin/bb_stop32
%attr(755,root,root) %{_datadir}/bigsister/bin/report*
%attr(755,root,root) %{_datadir}/bigsister/bin/smtpmail
%attr(755,root,root) %{_datadir}/bigsister/bin/testers
%attr(755,root,root) %{_datadir}/bigsister/bin/bbecho
%dir %{_datadir}/bigsister/uxmon
%dir %{_datadir}/bigsister/uxmon/Config
%{_datadir}/bigsister/uxmon/Config/_perflib
%{_datadir}/bigsister/uxmon/Config/noFQDN
%{_datadir}/bigsister/uxmon/Config/[FObdfimpty]*
%{_datadir}/bigsister/uxmon/Config/_[ert]*
%{_datadir}/bigsister/uxmon/Config/c[op]*
%{_datadir}/bigsister/uxmon/Config/http
%{_datadir}/bigsister/uxmon/Config/lo*
%{_datadir}/bigsister/uxmon/Config/n[Fefln]*
%{_datadir}/bigsister/uxmon/Config/ntp
%{_datadir}/bigsister/uxmon/Config/r[ep]*
%{_datadir}/bigsister/uxmon/Config/s[mty]*
%dir %{_datadir}/bigsister/uxmon/Monitor
%{_datadir}/bigsister/uxmon/Monitor/PerfLib.pm
%{_datadir}/bigsister/uxmon/Monitor/eventlog.pm
%{_datadir}/bigsister/uxmon/Monitor/[EMOTb-dfmpt-u]*
%{_datadir}/bigsister/uxmon/Monitor/l[ox]*
%{_datadir}/bigsister/uxmon/Monitor/r[ep]*
%{_datadir}/bigsister/uxmon/Monitor/s[aty]*
%dir %{_datadir}/bigsister/uxmon/Requester
%{_datadir}/bigsister/uxmon/Requester/[A-Za-rt-z]*
%{_datadir}/bigsister/uxmon/Requester/s[oy]*
%attr(755,root,root) %{_datadir}/bigsister/uxmon/uxmon
%{_datadir}/bigsister/uxmon/uxmon-rules.pl

%files server
%defattr(644,root,root,755)
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/bb-display.cfg
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/bb_event_generator.cfg
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/bsmon_site.cfg
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/notify.cfg
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/permissions
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/reporting
%{_sysconfdir}/bigsister/reporting/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/etc
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/bsmon.cfg
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/graphtemplates
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/keys
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/etc/graphdef
%{_sysconfdir}/bigsister/etc/graphdef/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/etc/moduleinfo
%{_sysconfdir}/bigsister/etc/moduleinfo/*
%attr(750,root,bs) %dir %{_sysconfdir}/bigsister/etc/testdef
%{_sysconfdir}/bigsister/etc/testdef/*
%attr(755,root,root) %dir %{_datadir}/bigsister/cgi
%attr(755,root,root) %{_datadir}/bigsister/cgi/bs*
%attr(775,root,bs) %dir %{_var}/lib/bigsister
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/graphs
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/html
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/logs
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/logs/history
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/help
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/help/images
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/skins
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/techie
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/title_in_table
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/twocolumn
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/webadmin
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/white_bg
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/default
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/static_lamps
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/structured_bg
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/alt_contentsicons
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/bigbro13
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/bsdoc
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/compactmenu
%attr(664,root,bs) %{_var}/lib/bigsister/www/skins/frames
%{_var}/lib/bigsister/www/help/*.html
%{_var}/lib/bigsister/www/help/*.jpg
%{_var}/lib/bigsister/www/help/images/*png
%{_datadir}/bigsister/www
%dir %{_datadir}/bigsister/bin/Statusmon
%{_datadir}/bigsister/bin/Statusmon/[BDGHRSTght]*.pm
%{_datadir}/bigsister/bin/Statusmon/bs_evgen.pm
%{_datadir}/bigsister/bin/access.pm
%{_datadir}/bigsister/bin/bbdisp.pm
%{_datadir}/bigsister/bin/bscgi.pm
%{_datadir}/bigsister/bin/display_map.pm
#te dwa tutaj powinny byc???
%{_datadir}/bigsister/bin/BER.pm
%{_datadir}/bigsister/bin/IPCFile.pm
#
%attr(755,root,root) %{_datadir}/bigsister/bin/bbd
%attr(755,root,root) %{_datadir}/bigsister/bin/bsmon
%attr(755,root,root) %{_datadir}/bigsister/bin/log_mail
%attr(755,root,root) %{_datadir}/bigsister/bin/notify
%attr(755,root,root) %{_datadir}/bigsister/bin/compile_skin
%attr(755,root,root) %{_datadir}/bigsister/bin/page_meridian

%files ldap
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/ldap
%{_datadir}/bigsister/uxmon/Monitor/ldap.pm

%files ldap_mozilla
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/ldap_mozilla
%{_datadir}/bigsister/uxmon/Monitor/ldap_mozilla.pm

%files oracle
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/oracle
%{_datadir}/bigsister/uxmon/Monitor/oracle.pm

%files radius
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/radius
%{_datadir}/bigsister/uxmon/Monitor/radius.pm

%files snmp
%defattr(644,root,root,755)
%{_sysconfdir}/bigsister/etc/mibs.txt
%{_sysconfdir}/bigsister/etc/perf*
%{_sysconfdir}/bigsister/etc/snmp_trap
%attr(755,root,root) %{_datadir}/bigsister/bin/bstrapd
%{_datadir}/bigsister/bin/snmp.pm
%{_datadir}/bigsister/uxmon/Config/_snmp
%{_datadir}/bigsister/uxmon/Config/_storage
%{_datadir}/bigsister/uxmon/Config/atmport
%{_datadir}/bigsister/uxmon/Config/caty
%{_datadir}/bigsister/uxmon/Config/etherport
%{_datadir}/bigsister/uxmon/Config/hub
%{_datadir}/bigsister/uxmon/Config/novell
%{_datadir}/bigsister/uxmon/Config/nt
%{_datadir}/bigsister/uxmon/Config/snmp
%{_datadir}/bigsister/uxmon/Config/snmp_trap
%{_datadir}/bigsister/uxmon/Config/snmpvar
%{_datadir}/bigsister/uxmon/Config/software
%{_datadir}/bigsister/uxmon/Config/ups
%{_datadir}/bigsister/uxmon/Config/qmqueue
%{_datadir}/bigsister/uxmon/Config/sendmail
%{_datadir}/bigsister/uxmon/Monitor/atmport.pm
%{_datadir}/bigsister/uxmon/Monitor/etherport.pm
%{_datadir}/bigsister/uxmon/Monitor/snmp.pm
%{_datadir}/bigsister/uxmon/Monitor/qmqueue.pm
%{_datadir}/bigsister/uxmon/Monitor/sendmail.pm
%{_datadir}/bigsister/uxmon/Monitor/snmp_trap.pm
%{_datadir}/bigsister/uxmon/Requester/snmp.pm
