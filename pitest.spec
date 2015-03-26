# 2015 : This pitest.spec file is authored by Aric LeDell and is granted to the public domain
Name:           pitest
Version:        1.1.4
Release:        2%{?dist}
Summary:        A state of the art mutation testing system for Java (also known as PIT)
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://pitest.org/
Source0:        https://github.com/hcoles/pitest/archive/pitest-parent-%{version}.tar.gz

Patch0:         pitest.remove-SNAPSHOT-for-1.1.4.patch

BuildArch:      noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: maven-local
BuildRequires: maven-jar-plugin
BuildRequires: maven-shade-plugin
Requires:      java-headless
Requires:      ant

%description
Real world mutation testing - PIT is a state of the art mutation testing system,
providing gold standard test coverage for Java.  It is fast, scalable and
integrates with modern test and build tooling.

%package javadoc
Summary:        javadoc for %{name}
%description javadoc
javadoc for %{name}.

%package ant
Summary:        ant bindings for %{name}
Requires: pitest-command-line
Requires: pitest
# Test-only requires
#BuildRequires: xmlunit
#BuildRequires: ant-testutil
#BuildRequires: ?maven-ant-tasks
%description ant
Ant task for %{name}.

%package command-line
Summary:        command-line usage for %{name}
Requires: jopt-simple
Requires: pitest-html-report
Requires: pitest
%description command-line
Command-line tool for %{name}.

%package groovy-verification
Summary:        groovy verification for %{name}
BuildRequires: maven-compiler-plugin
#BuildRequires: ?groovy-eclipse-compiler
#BuildRequires: ?groovy-eclipse-batch
#BuildRequires: ?build-helper-maven-plugin
Requires: junit
Requires: groovy
Requires: spock-core
%description groovy-verification
Tests for groovy integration with %{name}.

%package html-report
Summary:        html reporting for %{name} results
BuildRequires: antlr3-tool
Requires: antlr3-tool
Requires: pitest
Requires: stringtemplate
Requires: pitest
%description html-report
Plugin providing html reporting for %{name} results.

%package java8-verification
Summary:        java8 verification for %{name}
BuildRequires: maven-failsafe-plugin
BuildRequires: maven-surefire-provider-junit
Requires: junit
Requires: pitest
%description java8-verification
Checks %{name} against Java8 features (%{name} project is itself Java5-based only).

%package maven
Summary:        maven bindings for %{name}
BuildRequires: maven-failsafe-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-plugin-plugin
Requires: maven-plugin-api maven-project maven-scm-api maven-scm-manager-plexus maven-scm-providers-standard surefirew-booter maven-surefire-common maven-artifact maven-toolchain
# Test deps
#BuildRequires: maven-plugin-testing-harness maven-verifier
Requires: pitest-html-report
Requires: pitest
%description maven
Maven Mojo for %{name}.

%package maven-verification
Summary:        maven-verification for %{name}
BuildRequires: maven-deploy-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-failsafe-plugin
Requires: maven-plugin-api
Requires: pitest-maven
Requires: maven-project maven-artifact maven-toolchain
#Test deps
#BuildRequires: maven-plugin-testing-harness maven-verifier
%description maven-verification
Maven Mojo integration tests for %{name}.

%prep
find . -name "*.jar" | xargs rm
%autosetup -n %{name}-%{name}-parent-%{version} -p0

%mvn_package :%{name}-parent __noinstall
%mvn_package :%{name}
%mvn_package :%{name}-ant
%mvn_package :%{name}-command-line
%mvn_package :%{name}-groovy-verification
%mvn_package :%{name}-html-report
%mvn_package :%{name}-java8-verification
%mvn_package :%{name}-maven
%mvn_package :%{name}-maven-verification

%build
%mvn_build -f -s

%install

# jars
install -Dm 644 %{name}/target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}.jar
install -Dm 644 %{name}-ant/target/%{name}-ant-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/ant.jar
install -Dm 644 %{name}-command-line/target/%{name}-command-line-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/command-line.jar
install -Dm 644 %{name}-groovy-verification/target/%{name}-groovy-verification-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/groovy-verification.jar
install -Dm 644 %{name}-html-report/target/%{name}-html-report-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/html-report.jar
install -Dm 644 %{name}-java8-verification/target/%{name}-java8-verification-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/java8-verification.jar
install -Dm 644 %{name}-maven/target/%{name}-maven-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/maven.jar
install -Dm 644 %{name}-maven-verification/target/%{name}-maven-verification-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/maven-verification.jar

# poms
mkdir -p %{buildroot}%{_datadir}/maven-poms/
install -Dpm 644 %{name}/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}.pom
install -Dpm 644 %{name}-ant/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-ant.pom
install -Dpm 644 %{name}-command-line/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-command-line.pom
install -Dpm 644 %{name}-groovy-verification/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-groovy-verification.pom
install -Dpm 644 %{name}-html-report/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-html-report.pom
install -Dpm 644 %{name}-java8-verification/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-java8-verification.pom
install -Dpm 644 %{name}-maven/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-maven.pom
install -Dpm 644 %{name}-maven-verification/pom.xml %{buildroot}%{_datadir}/maven-poms/%{name}-maven-verification.pom

# fragments
%add_maven_depmap %{name}.pom %{name}/%{name}.jar
%add_maven_depmap %{name}-ant.pom %{name}/ant.jar -f "ant"
%add_maven_depmap %{name}-command-line.pom %{name}/command-line.jar -f "command-line"
%add_maven_depmap %{name}-groovy-verification.pom %{name}/groovy-verification.jar -f "groovy-verification"
%add_maven_depmap %{name}-html-report.pom %{name}/html-report.jar -f "html-report" -a "org.pitest:%{name}-html-report"
%add_maven_depmap %{name}-java8-verification.pom %{name}/java8-verification.jar -f "java8-verification"
%add_maven_depmap %{name}-maven.pom %{name}/maven.jar -f "maven"
%add_maven_depmap %{name}-maven-verification.pom %{name}/maven-verification.jar -f "maven-verification"


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{name}/target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf %{name}/apidocs

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files ant -f .mfiles-ant
%files command-line -f .mfiles-command-line
%files groovy-verification -f .mfiles-groovy-verification
%files html-report -f .mfiles-html-report
%files java8-verification -f .mfiles-java8-verification
%files maven -f .mfiles-maven
%files maven-verification -f .mfiles-maven-verification

%changelog
* Thu Feb 12 2015 Aric LeDell <aric@hiragana.ledell.net> - 1.1.4-2
- Made dependencies explicit by examining pom files

* Wed Feb 11 2015 Aric LeDell <aric@hiragana.ledell.net> - 1.1.4-1
- Initial fedora implementation
