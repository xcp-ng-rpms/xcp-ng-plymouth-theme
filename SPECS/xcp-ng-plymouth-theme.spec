Summary:        A plymouth theme for XCP-ng
Name:           xcp-ng-plymouth-theme
Version:        1.0.0
Release:        3
License:        GPLv2+
Group:          System Environment/Base
URL:            https://github.com/xcp-ng/xcp-ng-plymouth-theme
Source0:        https://github.com/xcp-ng/xcp-ng-plymouth-theme/archive/v%{version}/xcp-ng-plymouth-theme-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch
Requires:       plymouth, plymouth-plugin-script, plymouth-graphics-libs, gnu-free-sans-fonts
BuildRequires:  kernel-devel

%define themedir     %{_datadir}/plymouth/themes/xcp-ng
%define plymouthconf %{_sysconfdir}/plymouth/plymouthd.conf

%description
The %{name} package contains the XCP-ng theme for plymouth.

%prep
%autosetup -p1

%install

install -m 755 -d %{buildroot}/%{themedir}
install -m 755 -p -D xcp-ng.plymouth xcp-ng.script -t %{buildroot}/%{themedir}
install -m 755 -p -D background.png progress_bar.png progress_box.png -t %{buildroot}/%{themedir}

%post
/usr/sbin/plymouth-set-default-theme xcp-ng
%{regenerate_initrd_post}

%postun
if [ $1 -eq 0 ]; then
    if grep -q "^Theme *= *xcp-ng *$" "%{plymouthconf}"; then
        /usr/sbin/plymouth-set-default-theme text
    fi
fi
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%triggerin -- plymouth

if grep -q "^ShowDelay *=" "%{plymouthconf}"; then
    sed -i 's/^ShowDelay *=.*/ShowDelay = 0/' %{plymouthconf}
else
    echo ShowDelay = 0 >> %{plymouthconf}
fi

%files
%{themedir}/xcp-ng.plymouth
%{themedir}/xcp-ng.script
%{themedir}/background.png
%{themedir}/progress_bar.png
%{themedir}/progress_box.png

%changelog
* Mon Sep 24 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-3
- Fix upgrade issue: do not set theme back to text upon upgrade

* Thu Sep 13 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-2
- Rebuild for XCP-ng 7.6.0
