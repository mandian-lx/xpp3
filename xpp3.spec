# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define oversion 1.1.3_8
%define jversion 1.4.3_8
%define gcj_support 1

Summary:        XML Pull Parser
Name:           xpp3
Version:        1.1.3.8
Release:        %mkrel 1.1
Epoch:          0
License:        Apache License
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Group:          Development/Java
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Patch0:         %{name}-link-docs-locally.patch
Requires:       jpackage-utils >= 0:1.6
BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  /usr/bin/perl
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull 
parsing engine that is based on ideas from XPP and in 
particular XPP2 but completely revised and rewritten to 
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser
Group:          Development/Java
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
Requires:       java

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oversion}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0

%{__perl} -pi -e 's/1\.[12]/1.4/g;' build.xml

%build
export CLASSPATH=$(build-classpath xerces-j2 xml-commons-apis junit)
%{ant} xpp3 junit apidoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}-%{jversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p build/%{name}_min-%{jversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-minimal-%{version}.jar
cp -p build/%{name}_xpath-%{jversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-xpath-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; \
  do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

rm -rf doc/{build.txt,api}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.html LICENSE.txt doc/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}-xpath.jar
%{_javadir}/%{name}-xpath-%{version}.jar
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files minimal
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/%{name}-minimal.jar
%{_javadir}/%{name}-minimal-%{version}.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*
