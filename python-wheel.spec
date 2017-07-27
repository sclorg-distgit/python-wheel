# Created by pyp2rpm-1.0.1
%{?scl:%scl_package python-setuptools}
%{!?scl:%global pkg_name %{name}}

%global pypi_name wheel

Name:           %{?scl_prefix}python-%{pypi_name}
Version:        0.30.0a0
Release:        1%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            https://bitbucket.org/pypa/wheel
Source0:        https://files.pythonhosted.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
 

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

%prep
%setup -q -n %{pypi_name}-%{version}

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py


%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python3} setup.py build
%{?scl:EOF}


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%{?scl:scl enable %{scl} - << \EOF}
%{__python3} setup.py install --skip-build --root %{buildroot}
%{?scl:EOF}


%check
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
#rm setup.cfg
#py.test --ignore build
# no test for Python 3, no python3-jsonschema yet
#%if 0
#pushd %{py3dir}
#rm setup.cfg
#py.test-%{python3_version} --ignore build
#popd
#%endif # with_python3


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/wheel
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/test


%changelog
* Wed Jun 14 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-1
- Update to 0.30.0a0 for rh-python36

* Mon Jan 19 2015 Matej Stuchlik <mstuchli@redhat.com> - 0.24.0-1
- Update to 0.24.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
