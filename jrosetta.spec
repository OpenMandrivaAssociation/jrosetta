Summary:	JRosetta provides a common base for graphical component
Name:		jrosetta
Version:	1.0.2
Release:	%mkrel 0.0.1
Group:		Development/Java
License:	GPLv2+
URL:		http://dev.artenum.com/projects/JRosetta
Source0:	jrosetta-%{version}-GPL.zip
BuildRequires:	java-rpmbuild
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	ant
Requires:	java >= 1.5
Requires:	jpackage-utils >= 1.5
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
JRosetta provides a common base for graphical component that could be used
to build a graphical console in Swing with the latest requirements, such as
command history, completion and so on for instance for scripting language
or command line.


%prep
%setup -q -n %{name}-%{version}-gpl

#wrong-file-end-of-line-encoding
cp -p CHANGE.txt CHANGE.txt.CRLF
sed -i -e 's/\r//' CHANGE.txt
touch -r CHANGE.txt.CRLF CHANGE.txt
rm CHANGE.txt.CRLF

%build
%ant make


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_javadir}

for j in jrosetta-API jrosetta-engine ; do
  install -pm 0644 dist/${j}.jar %{buildroot}%{_javadir}/${j}-%{version}.jar
  ln -fs ${j}-%{version}.jar %{buildroot}%{_javadir}/${j}.jar
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGE.txt COPYRIGHT LICENSE.txt
%{_javadir}/jrosetta*.jar
