Summary:	A graphical interface for basic firewall setup
Name:		system-config-firewall
Version:	1.2.29
Release:	6
License:	GPL v2+
Group:		Base
URL:		http://fedorahosted.org/system-config-firewall
Source0:	https://fedorahosted.org/released/system-config-firewall/%{name}-%{version}.tar.bz2
# Source0-md5:	c4c9957218e95dad08fb307bf66fb60c
# replace pickle by json (CVE-2011-2520):
Patch0:		%{name}-1.2.27-rhbz#717985.patch
Patch1:		bashism.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
Requires:	gtk+2 >= 2:2.6
Requires:	hicolor-icon-theme
Requires:	python-dbus
Requires:	python-pygtk-glade
Requires:	python-pygtk-gtk
Requires:	python-slip-dbus >= 0.2.7
Requires:	system-config-firewall-base = %{version}-%{release}
Requires:	system-config-firewall-tui = %{version}-%{release}
Provides:	system-config-securitylevel = 1.7.0
Obsoletes:	system-config-securitylevel
ExclusiveOS:	Linux
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
system-config-firewall is a graphical user interface for basic
firewall setup.

%package base
Summary:	system-config-firewall base components and command line tool
Group:		Base
Requires:	iptables >= 1.2.8
#Requires:	libselinux-utils >= 1.19.1
Requires:	python
Provides:	lokkit = 1.7.0
Obsoletes:	lokkit

%description base
Base components of system-config-firewall with lokkit, the command
line tool for basic firewall setup.

%package tui
Summary:	A text interface for basic firewall setup
Group:		Base
Requires:	newt-python
Requires:	system-config-firewall-base = %{version}-%{release}
Provides:	system-config-securitylevel-tui = 1.7.0
Obsoletes:	system-config-securitylevel-tui

%description tui
system-config-firewall-tui is a text user interface for basic firewall
setup.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor system --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/system-config-firewall.desktop

%find_lang %{name} --all-name

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-mechanism.py{,.keep}
%py_postclean %{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-mechanism.py{.keep,}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 2 ]; then
	# kill the D-BUS mechanism on update
	pid=$(pidof -x system-config-firewall-mechanism.py)
	[ "$pid" ] && kill -TERM $pid || :
fi
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%triggerpostun -- %{name} < 1.1.0
%{_datadir}/%{name}/convert-config

%triggerpostun -- system-config-securitylevel
%{_datadir}/%{name}/convert-config

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-firewall
%defattr(0644,root,root)
/etc/dbus-1/system.d/org.fedoraproject.Config.Firewall.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.Config.Firewall.service
%{_datadir}/polkit-1/actions/org.fedoraproject.config.firewall.policy
%{_datadir}/%{name}/fw_gui.*
%{_datadir}/%{name}/fw_dbus.*
%{_datadir}/%{name}/fw_nm.*
%{_datadir}/%{name}/gtk_*
%{_datadir}/%{name}/*.glade
%attr(755,root,root) %{_datadir}/%{name}/system-config-firewall-mechanism.*
%{_desktopdir}/system-config-firewall.desktop
%{_iconsdir}/hicolor/*/apps/preferences-system-firewall*.*

%files base -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lokkit
%attr(755,root,root) %{_datadir}/%{name}/convert-config
%dir %{_datadir}/%{name}
%defattr(0644,root,root)
%{_datadir}/%{name}/etc_services.*
%{_datadir}/%{name}/fw_compat.*
%{_datadir}/%{name}/fw_config.*
%{_datadir}/%{name}/fw_firewalld.*
%{_datadir}/%{name}/fw_functions.*
%{_datadir}/%{name}/fw_icmp.*
%{_datadir}/%{name}/fw_iptables.*
%{_datadir}/%{name}/fw_lokkit.*
%{_datadir}/%{name}/fw_parser.*
%{_datadir}/%{name}/fw_selinux.*
%{_datadir}/%{name}/fw_services.*
%{_datadir}/%{name}/fw_sysconfig.*
%{_datadir}/%{name}/fw_sysctl.*
%ghost %config(missingok,noreplace) %verify(not md5 mtime size) /etc/sysconfig/system-config-firewall

%files tui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-firewall-tui
%{_datadir}/%{name}/fw_tui.*
