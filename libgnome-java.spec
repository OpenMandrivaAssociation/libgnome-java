%define _disable_ld_no_undefined 1

Name:           libgnome-java
Version:        2.12.7
Release:        %mkrel 5.0.2
Epoch:          0
Summary:        Java bindings for libgnome
License:        LGPL
Group:          System/Libraries
URL:            http://java-gnome.sourceforge.net
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/libgnome-java/2.12/libgnome-java-%{version}.tar.bz2
Source1:        http://fr2.rpmfind.net/linux/gnome.org/sources/libgnome-java/2.12/libgnome-java-2.12.7.changes
Source2:        http://fr2.rpmfind.net/linux/gnome.org/sources/libgnome-java/2.12/libgnome-java-2.12.7.md5sum
Source3:        http://fr2.rpmfind.net/linux/gnome.org/sources/libgnome-java/2.12/libgnome-java-2.12.7.news
Source4:        java-gnome-macros.tar.bz2
BuildRequires:  docbook-utils
BuildRequires:  docbook-dtd30-sgml
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-rpmbuild
BuildRequires:  libgnome2-devel
BuildRequires:  java-gcj-compat-devel
BuildRequires:  libgnomecanvas2-devel
BuildRequires:  libgnomeui2-devel
BuildRequires:  libgtk-java-devel >= 0:2.10.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
libgnome-java is a language binding that allows developers to write
GNOME applications in Java.  It is part of Java-GNOME.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Conflicts:      libgnome-java < 2.12.7-2

%description    devel
Development files for %{name}.

%prep
%setup -q
%setup -q -T -D -a 4
%{__aclocal} -I macros --force
%{__autoconf} --force
%{__automake} --copy --force-missing
%{__libtoolize} --copy --force

%build
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAVAH=%{_jvmdir}/java-rpmbuild/bin/javah
export JAR=%{jar}
export JAVADOC=%{javadoc}
export GCJ=%{gcj}
export JAVAFLAGS=-Xmx360m
export CPPFLAGS="-I%{java_home}/include -I%{java_home}/include/linux"
%{configure2_5x} --with-jardir=%{_javadir}
%{make}

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
%{_bindir}/zip -9 -r $zipfile $(find -name \*.java)
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
%{__rm} -rf %{buildroot}/%{name}-%{version}

# install the src zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
%{__install} -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_javadir}/
pushd %{buildroot}%{_javadir}
%{__ln_s} $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libgnomejava-*.so
%{_libdir}/libgnomejni-*.so
%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%doc doc/api doc/tutorial
%{_javadir}/*.zip
%{_libdir}/libgnomejava.so
%{_libdir}/libgnomejni.so
%{_libdir}/*la
%{_libdir}/pkgconfig/*
