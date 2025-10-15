#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		kframever	6.8
%define		qtver		6.6
%define		kaname		keysmith
Summary:	Program to generate 2FA tokens
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	0ee5d61ddb2322a7854b419c6e24ccd4
URL:		http://www.kde.org/
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qtver}}
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kirigami-devel >= %{kframever}
BuildRequires:	kf6-kirigami-addons-devel >= 1.7.0
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-prison
BuildRequires:	kf6-qqc2-desktop-style-devel >= %{kframever}
BuildRequires:	libsodium-devel >= 1.0.16
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	openssl-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Keysmith is an application to generate two-factor authentication (2FA)
tokens when logging in to your (online) accounts. Currently it
supports both HOTP and TOTP tokens.

%description -l pl.UTF-8
Keysmith jest aplikacją do generowania tokenów dwuskładnikowego
uwierzytelniania (2FA) gdy logujesz się do twoich kont online. Obecnie
wspiera tokeny HOTP i TOTP.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/keysmith
%{_desktopdir}/org.kde.keysmith.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.keysmith.svg
%{_datadir}/metainfo/org.kde.keysmith.appdata.xml
