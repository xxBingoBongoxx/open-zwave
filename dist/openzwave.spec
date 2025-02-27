%if 0%{?is_opensuse} 
%define __global_ldflags %{nil}
%endif

Name:     openzwave
Version:  1.6.944
Release:  1.0%{?dist}
Summary:  Sample Executables for OpenZWave
URL:      http://www.openzwave.net
%if 0%{?suse_version} > 0
License: LGPL-3.0+
%else 
License: LGPLv3+
%endif
Source0:  http://old.openzwave.com/downloads/openzwave-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: tinyxml-devel
%if 0%{?fedora}
BuildRequires: systemd-devel pkgconfig
%endif
%if 0%{?is_opensuse}
BuildRequires: systemd-devel pkg-config
%endif

%description
OpenZWave is an open-source, cross-platform library designed to enable anyone to
add support for Z-Wave home-automation devices to their applications, without
requiring any in depth knowledge of the Z-Wave protocol.


%package -n libopenzwave
Summary: Library to access Z-Wave interfaces
%if 0%{?is_opensuse} 
Requires(pre): shadow
%else
Requires(pre): shadow-utils
%endif


%description -n libopenzwave
OpenZWave is an open-source, cross-platform library designed to enable anyone to
add support for Z-Wave home-automation devices to their applications, without
requiring any in depth knowledge of the Z-Wave protocol.


%package -n libopenzwave-devel
Summary: Open-ZWave header files
Requires: libopenzwave%{?_isa} = %{version}-%{release}


%description -n libopenzwave-devel
Header files needed when you want to compile your own
applications using openzwave


%package -n libopenzwave-devel-doc
Summary: Open-ZWave API documentation files
Requires: libopenzwave-devel%{?_isa} = %{version}-%{release}


%description -n libopenzwave-devel-doc
API documentation files needed when you want to compile your own
applications using openzwave


%prep
%setup -q -n openzwave-%{version}


%build
major_ver=$(echo %{version} | awk -F \. {'print $1'})
minor_ver=$(echo %{version} | awk -F \. {'print $2'})
revision=$(echo %{version} | awk -F \. {'print $3'})
CPPFLAGS="%{optflags} -Wformat" LDFLAGS="%{__global_ldflags}" USE_HID=0 USE_BI_TXML=0 VERSION_MAJ=$major_ver VERSION_MIN=$minor_ver VERSION_REV=$revision PREFIX=/usr sysconfdir=%{_sysconfdir}/openzwave/ includedir=%{_includedir} docdir=%{_defaultdocdir}/openzwave-%{version} instlibdir=%{_libdir} make %{?_smp_mflags}


%install
rm -rf %{buildroot}/*
major_ver=$(echo %{version} | awk -F \. {'print $1'})
minor_ver=$(echo %{version} | awk -F \. {'print $2'})
revision=$(echo %{version} | awk -F \. {'print $3'})
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_defaultdocdir}/openzwave-%{version}/
mkdir -p %{buildroot}/%{_sysconfdir}/
mkdir -p %{buildroot}/%{_includedir}/openzwave/
DESTDIR=%{buildroot} USE_HID=0 USE_BI_TXML=0 VERSION_MAJ=$major_ver VERSION_MIN=$minor_ver VERSION_REV=$revision PREFIX=/usr sysconfdir=%{_sysconfdir}/openzwave/ includedir=%{_includedir}/openzwave/ docdir=%{_defaultdocdir}/openzwave-%{version} instlibdir=%{_libdir} make install
rm %{buildroot}%{_defaultdocdir}/openzwave-%{version}/Doxyfile.in
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/ChangeLog.old
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/html/
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/default.htm
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/general/
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/images+css/
rm -rf %{buildroot}%{_defaultdocdir}/openzwave-%{version}/api/


%files
%{_bindir}/MinOZW


%files -n libopenzwave
%license LICENSE
%doc docs/default.htm docs/general/ docs/images+css/
%{_libdir}/libopenzwave.so.*
%defattr(664, root, zwave, 775)
%dir %{_sysconfdir}/openzwave/
%config(noreplace) %{_sysconfdir}/openzwave/*


%files -n libopenzwave-devel
%{_bindir}/ozw_config
%{_includedir}/openzwave/
%{_libdir}/libopenzwave.so
%{_libdir}/pkgconfig/libopenzwave.pc


%files -n libopenzwave-devel-doc
%doc docs/api/


%post -n libopenzwave
/sbin/ldconfig 

%post -n libopenzwave-devel
/sbin/ldconfig 

%postun -n libopenzwave
/sbin/ldconfig 

%pre -n libopenzwave
getent group zwave >/dev/null || groupadd -f -r zwave


%changelog
* Wed May 08 2019 Justin Hammond <justin@dynam.ac> - 1.6.944
- Update to new release of OpenZwave - 1.6

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.20180624git1e36dcc.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Michael Cronenworth <mike@cchtml.com> - 1.5.0-0.20180623git1e36dcc.0
- Update to 20180623 git checkout to fix FTBFS
- Drop patches that revert BARRIER_OPERATOR support and use newer version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.20171212gitc3b0e31.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Michael Cronenworth <mike@cchtml.com> - 1.5.0-0.20171211gitc3b0e31.0
- Update to 20171211 git checkout
- Revert new BARRIER_OPERATOR support and use older version

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-0.20170725gitde1c0e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jul 31 2017 Michael Cronenworth <mike@cchtml.com> - 1.5.0-0.20170724gitde1c0e6
- Update to a git checkout, execeptions patch is upstream
- Fixes crashing issues with domoticz

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.164-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Michael Cronenworth <mike@cchtml.com> - 1.4.164-1
- Initial spec
