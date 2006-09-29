# TODO
# - correct path for files and directory in /etc/bigsister/etc/* - Patch5 (FHS)
# - security for webpage and admin page
# - subpackages for skins??????
# - add patch and e-mail to author
# - correct directory in /etc/bigsister/etc (some files to /usr/share, /var/lib)
# - check all patches, remove old
# - todo webapps (sigh)
# - uxmon to -agent (as done in spec in distro)

%include	/usr/lib/rpm/macros.perl
Summary:	The Big Sister Network and System Monitor
Summary(pl):	Wielka Siostra - monitor sieci i systemów - klon komercyjnego BigBrother
Name:		bigsister
Version:	1.02
Release:	4
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/bigsister/big-sister-%{version}.tar.gz
# Source0-md5:	2516b00134465952982c234b4c91c350
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.bsmon.cfg
Source4:	%{name}.uxmon-net
Source6:	%{name}.uxmon-asroot
Source7:	%{name}.httpd_conf
Source8:	%{name}.mibs.txt
Patch1:		%{name}-memory.patch
Patch2:		%{name}-logfile-notranslated.patch
Patch3:		%{name}-dubleinstall.patch
Patch4:		%{name}-not_user_check.patch
Patch5:		%{name}-ac.patch
#Patch5:	%{name}-lang_lcmessages.patch
#Patch6:	%{name}-path_to_adm.patch
URL:		http://bigsister.graeff.com/
BuildRequires:	perl-libnet
BuildRequires:	perl-libwww
#BuildRequires:	post-server-is-broken
BuildRequires:	rpm-perlprov >= 4.0.2-104
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
#Requires:	nscd
Requires:	sysstat
Provides:	group(bs)
Provides:	perl(Monitor::uxmon)
Provides:	user(bs)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# 'common' and 'parse' are files provided with bigsister
# perl-GD is optional (for generating maps)
# perl-FCGI is recommended, but not required
# perl-SNMP_Session is requires only for SNMP checks, but snmp.pm module
# (which tests if SNMP_Session exists) must be present in base package
%define		_noautoreq	'perl(common)' 'perl(parse)' 'perl(GD)' 'perl(FCGI)' 'perl(SNMP_Session)' 'perl(SNMP_util)' 'perl(BER)' 'perl(Monitor::Monitor)' 'perl(Monitor::Tester)' 'perl(Monitor::bb)'

%define		_webapps	/etc/webapps
%define		_webapp		%{name}

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
Requires:	perl-FCGI
Requires:	perl-GD-Graph-Map
Requires:	perl-Net-SMTP-Receive
Requires:	perl-Net-SNMP
Requires:	perl-libwww
Requires:	rrdtool
Requires:	webapps

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
Requires:	apache(mod_perl)
Requires:	webserver

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
%setup -q -n big-sister-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__autoconf}
./configure \
	--enable-FHS \
	--with-user=bs \
	--with-cgi=/bigsis/cgi \
	--with-url=/bigsis \
	--with-crondir=/etc/cron.weekly

# --with-systype	the target system type (e.g. sunos, windows, linux, etc.)
# --with-speedy		the CGI accelerators (e.g. speedy) path
# --with-cgi		the CGI path we should use
# --with-group		the group that will own your installed files
# --with-url		the URL at which we will find the web pages
# --with-perlext	the file extension perl scripts (CGIs) should get
# --with-rpmdir		the RPM build area

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_var}/lib/bigsister/{graphs,www/graphs,logs}} \
	$RPM_BUILD_ROOT%{_webapps}/%{_webapp}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/etc/init.d
mv -f $RPM_BUILD_ROOT%{_datadir}/bigsister/etc $RPM_BUILD_ROOT%{_sysconfdir}/bigsister
rm -rf	$RPM_BUILD_ROOT%{_datadir}/bigsister/etc

cd $RPM_BUILD_ROOT%{_datadir}/bigsister
ln -sf %{_var}/lib/bigsister/www www
ln -sf %{_var}/lib/bigsister var
ln -sf %{_sysconfdir}/bigsister/etc etc

# correct path in files
sed -i -e "
	s#$RPM_BUILD_ROOT##g
	s#%{_datadir}/bigsister/etc#%{_sysconfdir}/bigsister/etc#g
" $RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/moduleinfo/files

sed -i -e '
	s#%{_datadir}/bigsister/etc#%{_sysconfdir}/bigsister/etc#g
' $RPM_BUILD_ROOT%{_sysconfdir}/bigsister/etc/resources

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# basic config file
rm -f $RPM_BUILD_ROOT/etc/bigsister/uxmon-net
rm -f $RPM_BUILD_ROOT/etc/bigsister/etc/bsmon.cfg
rm -f $RPM_BUILD_ROOT/etc/bigsister/httpd.conf
rm -f $RPM_BUILD_ROOT/etc/bigsister/etc/mibs.txt

install %{SOURCE3} $RPM_BUILD_ROOT/etc/bigsister/etc/bsmon.cfg
install %{SOURCE4} $RPM_BUILD_ROOT/etc/bigsister/uxmon-net
install %{SOURCE6} $RPM_BUILD_ROOT/etc/bigsister/uxmon-asroot
install %{SOURCE7} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
install %{SOURCE8} $RPM_BUILD_ROOT/etc/bigsister/etc/mibs.txt

touch $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/htpasswd

# Dos/WinNT script
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/bigsister/expedap/myexpedap.cmd
rm -f $RPM_BUILD_ROOT%{_datadir}/bigsister/bin/{install32,perlsvc.pl}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 77 bs
%useradd -u 77 -d %{_var}/lib/bigsister/www -s /bin/false -c "Big Sister" -g bs bs

%post
/sbin/chkconfig --add bigsister
%service bigsister restart "Big Sister"

%preun
if [ "$1" = "0" ]; then
	%service bigsister stop
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
%service -q bigsister restart

%postun server
if [ "$1" = 0 ]; then
	%service -q bigsister restart
fi

%triggerin server -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun server -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin server -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun server -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun server -- %{name}-server < 1.02-2.4
# i don't even know why i wrote trigger, did package never ever worked?
if [ -f /etc/httpd/httpd.conf/92_%{name}.conf.rpmsave ]; then
	cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/httpd.conf/92_%{name}.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
fi

/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc %{_datadir}/doc/bigsister
%attr(755,root,root) /etc/cron.weekly/bigsister_logs
%attr(754,root,root) /etc/rc.d/init.d/bigsister
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bigsister
%attr(775,root,bs) %dir %{_sysconfdir}/bigsister
%dir %{_sysconfdir}/bigsister/expedap
%{_sysconfdir}/bigsister/expedap/myexpedap
%attr(775,root,bs) %dir %{_sysconfdir}/bigsister/etc
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/resources
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/OV
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/syslog
%attr(660,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/eventlog
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/tests.cfg
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/db.cfg
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/*.dbschema
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/version
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/mibsdef
%attr(664,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/etc/mondef
%attr(644,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/resources
%attr(640,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/uxmon-net
%attr(640,root,bs) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bigsister/uxmon-asroot
%attr(755,root,root) %{_sbindir}/bs*
%{_mandir}/man*/*
%dir %{_datadir}/bigsister
%{_datadir}/bigsister/etc
%{_datadir}/bigsister/var
%dir %{_datadir}/bigsister/bin
%dir %{_datadir}/bigsister/bin/Monitor
%dir %{_datadir}/bigsister/bin/Reader
%dir %{_datadir}/bigsister/bin/BigSister
%{_datadir}/bigsister/bin/BS_unix.pm
%{_datadir}/bigsister/bin/BigSister/common.pm
%{_datadir}/bigsister/bin/DBCapsulator
%{_datadir}/bigsister/bin/DBCapsulator.pm
%{_datadir}/bigsister/bin/[CHPRSTcp]*.pm
#%{_datadir}/bigsister/bin/Monitor/*.pm
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
#{_datadir}/bigsister/uxmon/Monitor/PerfLib.pm
#{_datadir}/bigsister/uxmon/Monitor/eventlog.pm
#{_datadir}/bigsister/uxmon/Monitor/[EMOTb-dfmpt-u]*
#{_datadir}/bigsister/uxmon/Monitor/l[ox]*
#{_datadir}/bigsister/uxmon/Monitor/r[ep]*
#{_datadir}/bigsister/uxmon/Monitor/s[aty]*
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

%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/htpasswd

%attr(755,root,root) %dir %{_datadir}/bigsister/cgi
%attr(755,root,root) %{_datadir}/bigsister/cgi/bs*
%attr(775,root,bs) %dir %{_var}/lib/bigsister
%attr(775,root,bs) %dir %{_var}/lib/bigsister/logs
%attr(775,root,bs) %dir %{_var}/lib/bigsister/graphs
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www
%attr(775,root,bs) %dir %{_var}/lib/bigsister/www/graphs
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
%{_var}/lib/bigsister/www/help/images/*.png
%{_var}/lib/bigsister/www/help/images/*.jpg
%{_datadir}/bigsister/www
%dir %{_datadir}/bigsister/bin/Statusmon
%{_datadir}/bigsister/bin/Statusmon/[BDGHRSTght]*.pm
%{_datadir}/bigsister/bin/Statusmon/bs_evgen.pm
%{_datadir}/bigsister/bin/access.pm
%{_datadir}/bigsister/bin/bbdisp.pm
%{_datadir}/bigsister/bin/bscgi.pm
%{_datadir}/bigsister/bin/display_map.pm
#te dwa tutaj powinny byc???
# and in english it means?
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
#%{_datadir}/bigsister/uxmon/Monitor/ldap.pm

%files ldap_mozilla
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/ldap_mozilla
#%{_datadir}/bigsister/uxmon/Monitor/ldap_mozilla.pm

%files oracle
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/oracle
#%{_datadir}/bigsister/uxmon/Monitor/oracle.pm

%files radius
%defattr(644,root,root,755)
%{_datadir}/bigsister/uxmon/Config/radius
#%{_datadir}/bigsister/uxmon/Monitor/radius.pm

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
#%{_datadir}/bigsister/uxmon/Monitor/atmport.pm
#%{_datadir}/bigsister/uxmon/Monitor/etherport.pm
#%{_datadir}/bigsister/uxmon/Monitor/snmp.pm
#%{_datadir}/bigsister/uxmon/Monitor/qmqueue.pm
#%{_datadir}/bigsister/uxmon/Monitor/sendmail.pm
#%{_datadir}/bigsister/uxmon/Monitor/snmp_trap.pm
%{_datadir}/bigsister/uxmon/Requester/snmp.pm
