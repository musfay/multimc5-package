#
# spec file for package multimc5
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global  _name          multimc
%global  quazip_commit  3691d57d3af13f49b2be2b62accddefee3c26b9c
%global  nbt_commit     dc72a20b7efd304d12af2025223fad07b4b78464
Name:           multimc5
Version:        0.6.12
Release:        0
Summary:        An open source launcher for Minecraft
License:        Apache-2.0
Group:          Amusements/Games/Other
URL:            https://multimc.org/
Source0:        https://github.com/MultiMC/MultiMC5/archive/%{version}/MultiMC5-%{version}.tar.gz
# MultiMC5 uses his own fork of quazip which has extra functions.
Source1:        https://github.com/MultiMC/quazip/archive/%{quazip_commit}/quazip-%{quazip_commit}.tar.gz
Source2:        https://github.com/MultiMC/libnbtplusplus/archive/%{nbt_commit}/libnbtplusplus-%{nbt_commit}.tar.gz
# PATCH-FIX-OPENSUSE fix warnings on older gcc
Patch0:         %{name}-quazip-fix-indentation.patch
# PATCH-FIX-OPENSUSE find other java binaries
Patch1:         %{name}-scan-lib64-jvm-for-java.patch
BuildRequires:  cmake >= 3.1
BuildRequires:  gcc-c++
BuildRequires:  hicolor-icon-theme
BuildRequires:  java-1.8.0-devel
BuildRequires:  update-desktop-files
BuildRequires:  zlib-devel
BuildRequires:  cmake(Qt5Concurrent) >= 5.6
BuildRequires:  cmake(Qt5Core) >= 5.6
BuildRequires:  cmake(Qt5Gui) >= 5.6
BuildRequires:  cmake(Qt5Network) >= 5.6
BuildRequires:  cmake(Qt5Test) >= 5.6
BuildRequires:  cmake(Qt5Widgets) >= 5.6
BuildRequires:  cmake(Qt5Xml) >= 5.6
Requires:       java
Provides:       %{_name}

%description
MultiMC is a free, open source launcher for Minecraft. It allows you  to  have  multiple,
separate instances  of  Minecraft (each with  their  own mods, texture packs, saves, etc)
and helps you manage them and their associated options with a simple interface.

%package runtime
Summary:        MultiMC5 runtime libraries
Group:          Amusements/Games/Other

%description runtime
MultiMC is a free, open source launcher for Minecraft. It allows you  to  have  multiple,
separate instances  of  Minecraft (each with  their  own mods, texture packs, saves, etc)
and helps you manage them and their associated options with a simple interface.

This package contains MultiMC5 runtime libraries.

%prep
%setup -q -n MultiMC5-%{version} -a 1 -a 2
# submodules
rm -rf libraries/quazip/* libraries/libnbtplusplus/*
mv quazip-%{quazip_commit}/* libraries/quazip/
mv libnbtplusplus-%{nbt_commit}/* libraries/libnbtplusplus/
rm -rf quazip-%{quazip_commit}/ libnbtplusplus-%{nbt_commit}/

%patch1 -p1
pushd libraries/quazip/
%patch0 -p1
popd

# create new .desktop file instead of patching upstream
cat >> %{name}.desktop << EOF
[Desktop Entry]
Version=%{version}
Name=MultiMC5
GenericName=Minecraft Launcher
Comment=Free, open source launcher and instance manager for Minecraft.
Type=Application
Terminal=false
Exec=%{_bindir}/%{name}
Icon=%{name}
Categories=Game;AdventureGame;
Keywords=game;minecraft;
EOF

## fix .desktop file
#pushd application/package/linux
#sed -i -E "s|Version=1.0.|Version=%%{version}|" %%{_name}.desktop
#sed -i -E "s|Exec=%%{_name}|Exec=%%{_bindir}/%%{name}|" %%{_name}.desktop
#sed -i -E "s|Icon=%%{_name}|Icon=%%{name}|" %%{_name}.desktop
#popd

%build
%cmake  -DCMAKE_BUILD_TYPE=Release \
	-DMultiMC_LAYOUT=lin-system \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DMultiMC_APP_BINARY_NAME="%{name}" \
	-DMultiMC_SHARE_DEST_DIR="share/%{name}" \
	-DMultiMC_UPDATER=off \
	%if 0%{?is_opensuse}
	-DMultiMC_BUILD_PLATFORM="openSUSE" 
	%else
	-DMultiMC_BUILD_PLATFORM="SUSE"
	%endif
%cmake_build

%install
%cmake_install
install -Dm644 application/resources/multimc/scalable/%{_name}.svg \
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dm644 %{name}.desktop \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md changelog.md
%license COPYING.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files runtime
%{_libdir}/libMultiMC*.so

%changelog
