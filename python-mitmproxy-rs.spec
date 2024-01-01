# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: python-mitmproxy-rs
Epoch: 100
Version: 0.3.10
Release: 1%{?dist}
Summary: The Rust bits in mitmproxy
License: MIT
URL: https://github.com/mitmproxy/mitmproxy_rs/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: cargo
BuildRequires: fdupes
BuildRequires: python-rpm-macros
BuildRequires: python3-Cython3
BuildRequires: python3-devel
BuildRequires: python3-maturin >= 0.14
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: rust >= 1.64.0

%description
This repository contains mitmproxy's Rust bits, most notably:
-   WireGuard Mode: The ability to proxy any device that can be
    configured as a WireGuard client.
-   Windows OS Proxy Mode: The ability to proxy arbitrary Windows
    applications by name or pid.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
pushd mitmproxy-rs && \
    maturin build --offline --sdist && \
    popd

%install
pip install \
    --no-deps \
    --ignore-installed \
    --root=%{buildroot} \
    --prefix=%{_prefix} \
    target/wheels/*.whl
find %{buildroot}%{python3_sitearch} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitearch}

%check

%if 0%{?suse_version} > 1500
%package -n python%{python3_version_nodots}-mitmproxy-rs
Summary: The Rust bits in mitmproxy
Requires: python3
Provides: python3-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python3dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-mitmproxy-rs
This repository contains mitmproxy's Rust bits, most notably:
-   WireGuard Mode: The ability to proxy any device that can be
    configured as a WireGuard client.
-   Windows OS Proxy Mode: The ability to proxy arbitrary Windows
    applications by name or pid.

%files -n python%{python3_version_nodots}-mitmproxy-rs
%license LICENSE
%{python3_sitearch}/*
%endif

%if !(0%{?suse_version} > 1500)
%package -n python3-mitmproxy-rs
Summary: The Rust bits in mitmproxy
Requires: python3
Provides: python3-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python3dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-mitmproxy-rs = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(mitmproxy-rs) = %{epoch}:%{version}-%{release}

%description -n python3-mitmproxy-rs
This repository contains mitmproxy's Rust bits, most notably:
-   WireGuard Mode: The ability to proxy any device that can be
    configured as a WireGuard client.
-   Windows OS Proxy Mode: The ability to proxy arbitrary Windows
    applications by name or pid.

%files -n python3-mitmproxy-rs
%license LICENSE
%{python3_sitearch}/*
%endif

%changelog
