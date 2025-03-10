#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python tools for communicating with WBEM servers
Summary(pl.UTF-8):	Pythonowe narzędzia do komunikacji z serwerami WBEM
Name:		python-pywbemtools
Version:	1.2.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pywbemtools/
Source0:	https://files.pythonhosted.org/packages/source/p/pywbemtools/pywbemtools-%{version}.tar.gz
# Source0-md5:	d1e935be11eb2e9b24b2509663c114f5
URL:		https://pypi.org/project/pywbemtools/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pywbemtools is a collection of command line tools that communicate
with WBEM servers:
- pywbemcli: a command line utility that uses the pywbem package to
  issue operations to a WBEM server using the CIM/WBEM standards
  defined by the DMTF to perform system management tasks.
- pywbemlistener: a command line utility that manages WBEM indication
  listeners running as background processes on the local system. These
  listeners use the pywbem package to receive indications sent by a
  WBEM server using the CIM/WBEM standards defined by the DMTF.

%description -l pl.UTF-8
Pywbemtools to zbiór narzędzi linii poleceń, komunikujących się z
serwerami WBEM:
- pywbemcli to narzędzie wykorzystujące pakiet pywbem do wysyłania
  operacji do serwera WBEM przy użyciu standardów CIM/WBEM,
  zdefiniowanych przez DMTF, w celu wykonania zadań związanych z
  zarządzeniem systemem.
- pywbemlistener to narzędzie zarządzające działającymi w tle na
  lokalnym systemie usługami identyfikacji WBEM. Usługi te
  wykorzystują pakiet pywbem do odbierania informacji wysyłanych przez
  serwery WBEM przy użyciu standardów CIM/WBEM, zdefiniowanych przez
  DMTF.

%package -n python3-pywbemtools
Summary:	Python tools for communicating with WBEM servers
Summary(pl.UTF-8):	Pythonowe narzędzia do komunikacji z serwerami WBEM
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-pywbemtools
Pywbemtools is a collection of command line tools that communicate
with WBEM servers:
- pywbemcli: a command line utility that uses the pywbem package to
  issue operations to a WBEM server using the CIM/WBEM standards
  defined by the DMTF to perform system management tasks.
- pywbemlistener: a command line utility that manages WBEM indication
  listeners running as background processes on the local system. These
  listeners use the pywbem package to receive indications sent by a
  WBEM server using the CIM/WBEM standards defined by the DMTF.

%description -n python3-pywbemtools -l pl.UTF-8
Pywbemtools to zbiór narzędzi linii poleceń, komunikujących się z
serwerami WBEM:
- pywbemcli to narzędzie wykorzystujące pakiet pywbem do wysyłania
  operacji do serwera WBEM przy użyciu standardów CIM/WBEM,
  zdefiniowanych przez DMTF, w celu wykonania zadań związanych z
  zarządzeniem systemem.
- pywbemlistener to narzędzie zarządzające działającymi w tle na
  lokalnym systemie usługami identyfikacji WBEM. Usługi te
  wykorzystują pakiet pywbem do odbierania informacji wysyłanych przez
  serwery WBEM przy użyciu standardów CIM/WBEM, zdefiniowanych przez
  DMTF.

%package apidocs
Summary:	API documentation for Python pywbemtools module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pywbemtools
Group:		Documentation

%description apidocs
API documentation for Python pywbemtools module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pywbemtools.

%prep
%setup -q -n pywbemtools-%{version}

# we don't ship click-repl 0.2.0, so allow 0.3
# (although there is issue with repl mode:
#  https://github.com/pywbem/pywbemtools/issues/1312
# )
%{__sed} -i -e '/^click-repl/ s/,<0\.3\.0//' requirements.txt

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

for f in pywbemcli pywbemlistener ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

for f in pywbemcli pywbemlistener ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/pywbemcli-2
%attr(755,root,root) %{_bindir}/pywbemlistener-2
%{py_sitescriptdir}/pywbemtools
%{py_sitescriptdir}/pywbemtools-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pywbemtools
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/pywbemcli
%attr(755,root,root) %{_bindir}/pywbemcli-3
%attr(755,root,root) %{_bindir}/pywbemlistener
%attr(755,root,root) %{_bindir}/pywbemlistener-3
%{py3_sitescriptdir}/pywbemtools
%{py3_sitescriptdir}/pywbemtools-%{version}-py*.egg-info
%endif
