%{?_javapackages_macros:%_javapackages_macros}

Name:           jrosetta
Version:        1.0.4
Release:        1
Summary:        A common base to build a graphical console

Group:          Development/Java
License:        GPLv2
URL:            https://dev.artenum.com/projects/JRosetta
Source0:        http://maven.artenum.com/content/groups/public/com/artenum/%{name}/%{version}/%{name}-%{version}-sources.jar

BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  maven-local

BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4

Requires:       jpackage-utils
Requires:       java-headless

%description
JRosetta provides a common base for graphical component that could be used
to build a graphical console in Swing with the latest requirements, such as
command history, completion and so on for instance for scripting language
or command line.

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation

%description    javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
# remove jar format related directory
rm -fr ../META-INF
#wrong-file-end-of-line-encoding
cp -p CHANGE.txt CHANGE.txt.CRLF
sed -i -e 's/\r//' CHANGE.txt
touch -r CHANGE.txt.CRLF CHANGE.txt
rm CHANGE.txt.CRLF
# remove deployement dependency
%pom_xpath_remove "pom:build/pom:extensions" pom.xml

%build

%mvn_build

%install
mkdir -p %{buildroot}%{_javadir}

cp -p modules/%{name}-api/target/%{name}-api-%{version}.jar \
        %{buildroot}%{_javadir}/%{name}-api.jar
# for compatibility
ln -s %{name}-api.jar \
        %{buildroot}%{_javadir}/%{name}-API.jar
cp -p modules/%{name}-engine/target/%{name}-engine-%{version}.jar \
        %{buildroot}%{_javadir}/%{name}-engine.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp -t %{buildroot}%{_javadocdir}/%{name} target/site/apidocs/*

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml  \
        %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -pm 644 modules/%{name}-api/pom.xml  \
        %{buildroot}%{_mavenpomdir}/JPP-%{name}-API.pom
install -pm 644 modules/%{name}-engine/pom.xml  \
        %{buildroot}%{_mavenpomdir}/JPP-%{name}-engine.pom

%add_maven_depmap JPP-%{name}.pom
%add_maven_depmap JPP-%{name}-API.pom %{name}-API.jar
%add_maven_depmap JPP-%{name}-engine.pom %{name}-engine.jar

%files -f .mfiles
%{_javadir}/%{name}-api.jar
%doc LICENSE.txt COPYRIGHT.txt CHANGE.txt

%files javadoc
%{_javadocdir}/%{name}/
%doc LICENSE.txt
