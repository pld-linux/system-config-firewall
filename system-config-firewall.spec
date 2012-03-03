#
# Conditional build:
%bcond_with		usermode
%bcond_with		polkit0
%bcond_without	polkit1

Summary:	A graphical interface for basic firewall setup
Name:		system-config-firewall
Version:	1.2.29
Release:	5.5
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
Requires:	system-config-firewall-base = %{version}-%{release}
Requires:	system-config-firewall-tui = %{version}-%{release}
Provides:	system-config-securitylevel = 1.7.0
Obsoletes:	system-config-securitylevel
%if %{with usermode}
Requires:	usermode-gtk >= 1.94
%endif
%if %{with polkit0}
Requires:	python-slip-dbus >= 0.1.15
%endif
%if %{with polkit1}
Requires:	python-slip-dbus >= 0.2.7
%endif
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
%configure \
	%{?with_usermode: --enable-usermode} \
	%{?with_polkit0: --enable-policykit0} \
	%{!?with_polkit1: --disable-policykit1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor system --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/system-config-firewall.desktop

%find_lang %{name} --all-name

%py_postclean %{_datadir}/system-config-firewall

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 2 ]; then
	# kill the D-BUS mechanism on update
	killall -TERM system-config-firewall-mechanism.py >/dev/null 2>&1 || :
fi
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%triggerpostun -- %{name} < 1.1.0
%{_datadir}/system-config-firewall/convert-config

%triggerpostun -- system-config-securitylevel
%{_datadir}/system-config-firewall/convert-config

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-firewall
%if %{with usermode}
%{_datadir}/system-config-firewall/system-config-firewall
%endif
%defattr(0644,root,root)
/etc/dbus-1/system.d/org.fedoraproject.Config.Firewall.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.Config.Firewall.service
%if %{with polkit0}
%{_datadir}/PolicyKit/policy/org.fedoraproject.config.firewall.0.policy
%endif
%if %{with polkit1}
%{_datadir}/polkit-1/actions/org.fedoraproject.config.firewall.policy
%endif
%{_datadir}/system-config-firewall/fw_gui.*
%{_datadir}/system-config-firewall/fw_dbus.*
%{_datadir}/system-config-firewall/fw_nm.*
%{_datadir}/system-config-firewall/gtk_*
%{_datadir}/system-config-firewall/*.glade
%attr(755,root,root) %{_datadir}/system-config-firewall/system-config-firewall-mechanism.*
%{_desktopdir}/system-config-firewall.desktop
%{_iconsdir}/hicolor/*/apps/preferences-system-firewall*.*
%if %{with usermode}
%config /etc/security/console.apps/system-config-firewall
%config /etc/pam.d/system-config-firewall
%endif

%files base -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lokkit
%attr(755,root,root) %{_datadir}/system-config-firewall/convert-config
%dir %{_datadir}/system-config-firewall
%defattr(0644,root,root)
%{_datadir}/system-config-firewall/etc_services.*
%{_datadir}/system-config-firewall/fw_compat.*
%{_datadir}/system-config-firewall/fw_config.*
%{_datadir}/system-config-firewall/fw_firewalld.*
%{_datadir}/system-config-firewall/fw_functions.*
%{_datadir}/system-config-firewall/fw_icmp.*
%{_datadir}/system-config-firewall/fw_iptables.*
%{_datadir}/system-config-firewall/fw_lokkit.*
%{_datadir}/system-config-firewall/fw_parser.*
%{_datadir}/system-config-firewall/fw_selinux.*
%{_datadir}/system-config-firewall/fw_services.*
%{_datadir}/system-config-firewall/fw_sysconfig.*
%{_datadir}/system-config-firewall/fw_sysctl.*
%ghost %config(missingok,noreplace) %verify(not md5 mtime size) /etc/sysconfig/system-config-firewall

%files tui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-firewall-tui
%{_datadir}/system-config-firewall/fw_tui.*
