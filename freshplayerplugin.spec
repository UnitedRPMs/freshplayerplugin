%define debug_package %{nil}

%global gitdate 20170519
%global commit0 963f43ee8f56d76fd16ae45759c383d15a8c5f6d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:    freshplayerplugin
Version: 0.3.6
Release: 2%{?gver}%{dist}
Summary: PPAPI-host NPAPI-plugin adapter
Group:   Applications/Internet
License: MIT
URL:     https://github.com/i-rinat/freshplayerplugin
Source0: https://github.com/i-rinat/freshplayerplugin/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
#-------------------------------------
BuildRequires: binutils 
BuildRequires: pkgconfig
BuildRequires: git 
BuildRequires: cmake 
BuildRequires: ragel 
BuildRequires: glib2-devel 
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel 
BuildRequires: pango-devel 
BuildRequires: xorg-x11-server-devel 
BuildRequires: mesa-libGL-devel 
BuildRequires: mesa-libGLES-devel 
BuildRequires: libconfig-devel
BuildRequires: libevent-devel 
BuildRequires: freetype 
BuildRequires: cairo-devel 
BuildRequires: gtk2-devel
BuildRequires: uriparser-devel
BuildRequires: openssl-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: ffmpeg-devel
BuildRequires: libv4l-devel
BuildRequires: git
#-------------------------------------
Recommends: chromium-pepper-flash 
Requires: ffmpeg
Requires: mozilla-filesystem
#-------------------------------------
Conflicts: flashplugin

%description
PPAPI or Pepper Plugin API is an interface promoted by Chromium/Chrome team 
for browser plugins. It's NPAPI-inspired yet significantly different API 
which have every concievable function plugin may want. Two-dimensional 
graphics, OpenGL ES, font rendering, network access, audio, and so on. 
It's huge, there are 107 groups of functions, called 
interfaces which todays Chromium browser offers to plugins. 
And specs are not final yet. 

%prep
%autosetup -n %{name}-%{commit0}  

sed -i 's|\(/chromium\)-browser\(/PepperFlash\)|\1\2|' src/config_pepperflash.c
sed -i 's|^\(pepperflash_path = \).*$|\1"%{_libdir}/chromium/PepperFlash/libpepflashplayer.so"|' data/freshwrapper.conf.example

# Disable 3D (because some intel graphics i915 and others display slow videos)
sed -i 's|enable_3d = 1|enable_3d = 0|g' data/freshwrapper.conf.example
sed -i 's|enable_3d           =      1,|enable_3d           =      0,|g' src/config.c

%build
%cmake -DCMAKE_SKIP_RPATH=1 -DWITH_GTK=2
make %{?_smp_mflags}


%install

install -Dm 0644 libfreshwrapper-flashplayer.so %{buildroot}/%{_libdir}/mozilla/plugins/libfreshwrapper-flashplayer.so
install -Dm 0644 data/freshwrapper.conf.example %{buildroot}/%{_sysconfdir}/freshwrapper.conf
install -Dm 0644 LICENSE %{buildroot}/%{_datadir}/licenses/freshplayerplugin/freshplayerplugin

%files
%doc README.md doc/*
%license LICENSE
%{_libdir}/mozilla/plugins/libfreshwrapper-flashplayer.so
%{_sysconfdir}/freshwrapper.conf
%{_datadir}/licenses/freshplayerplugin/freshplayerplugin
%config(noreplace) %{_sysconfdir}/freshwrapper.conf

%changelog

* Fri May 19 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.6-2.git963f43e
- Updated to 0.3.6-2.git963f43e

* Sat Jan 07 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.6-1-20170107gitdecacb2
- Updated to 0.3.6-20170107gitdecacb2

* Tue Jul 12 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.6-1-20160712gitc0510ba
- Updated to 0.3.6-20160712-c0510ba

* Tue Jul 12 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.5-7-20160712gitc0510ba
- Updated to 0.3.5-20160712-c0510ba

* Fri Jun 03 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.5-6-20160428git99c5aa1
- Forced gtk2
- solved slow videos

* Tue Apr 19 2016 Sérgio Basto <sergio@serjux.com> - 0.3.5-1
- Update to 0.3.5

* Tue Jan 05 2016 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.4-1
- Upgrade to 0.3.4

* Thu Nov 12 2015 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.3-1
- Update to 0.3.3
- Added install rule to cmake (patch from sergio@serjux.com)

* Tue Sep 29 2015 Sérgio Basto <sergio@serjux.com> - 0.3.2-2
- Removed Requires it is a shared library, so requires will be automatic.

* Tue Sep 22 2015 Sérgio Basto <sergio@serjux.com> - 0.3.2-1
- Some fixes and merged some of the work of postinstallerf.

* Mon Sep 21 2015 Mauricio Teixeira <mauricio.teixeira@gmail.com> - 0.3.2-0
- Initial RPM Fusion package based on retired 'dacr' package (Fedora Copr)

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-20150810-acb0ee4-1
- Updated to 0.3.1-20150810-acb0ee4
