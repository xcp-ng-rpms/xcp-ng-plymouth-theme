Summary:        A plymouth theme for XCP-ng
Name:           xcp-ng-plymouth-theme
Version:        1.1.0
Release:        5%{?dist}
License:        GPLv2+
Group:          System Environment/Base
URL:            https://github.com/xcp-ng/xcp-ng-plymouth-theme
Source0:        https://github.com/xcp-ng/xcp-ng-plymouth-theme/archive/v%{version}/xcp-ng-plymouth-theme-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:      noarch
Requires:       plymouth, plymouth-plugin-script, plymouth-graphics-libs
BuildRequires:  kernel-devel

# XCP-ng: plymouth-scripts should require fontconfig but doesn't
# As a consequence, when `/usr/libexec/plymouth/plymouth-populate-initrd` is called
# during initrd generation, this causes many (non fatal) errors.
# Add the dependency back here for now, despite we don't really use fonts.
Requires:       fontconfig
# Also require gnu-free-sans-fonts to ensure we come back to the previous list of installed packages,
# otherwise fontconfig will pull whatever provides what it needs, for example dejavu-sans-fonts.
Requires:       gnu-free-sans-fonts

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

%triggerpostun -- xcp-ng-plymouth-theme <= 1.0.0-2
# Workaround broken postun that would set theme to text when the package is updated
/usr/sbin/plymouth-set-default-theme xcp-ng

%files
%{themedir}/xcp-ng.plymouth
%{themedir}/xcp-ng.script
%{themedir}/background.png
%{themedir}/progress_bar.png
%{themedir}/progress_box.png

%changelog
* Wed Jul 10 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-5
- Fix typo in previous change: it's gnu-free-sans-fonts

* Wed Jul 10 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-4
- Also add back dependency to gnu-free-sans-font, for predictable dep solving

* Wed Jul 10 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-3
- Add dependency to fontconfig back, to compensate for missing dependency
  in plymouth-scripts.

* Thu Jun 20 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-2
- Remove unnecessary dependency to gnu-free-sans-font

* Mon Nov 14 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.1.0-1
- New theme

* Fri Sep 16 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-7
- Rebuild for XCP-ng 8.3

* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-6
- Rebuild for XCP-ng 8.2

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-5
- Rebuild for XCP-ng 8.1

* Thu May 02 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-4
- Rebuild for XCP-ng 8.0.0

* Mon Sep 24 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-3
- Fix upgrade issue: do not set theme back to text upon upgrade

* Thu Sep 13 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.0.0-2
- Rebuild for XCP-ng 7.6.0
