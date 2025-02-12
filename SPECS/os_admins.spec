Name        : os_admins
Version     : 1
Release     : 1
BuildArch   : noarch
Group       : System Environment/Base
License     : MIT
Packager    : SYSOPS
Vendor      : SYSOPS
URL         : http://sysops.ru/pulp/repos/
#Summary     : SYSOPS
#Source0     : %{Name}-%{Version}.tar.gz

%description
SYSOPS OS admins

%prep

%build

%pre
getent group admins >/dev/null || /sbin/groupadd -g 100 -r admins
getent group user || /sbin/groupadd -g 101 -r user
getent passwd user >/dev/null || /sbin/useradd -u 101 -g 101 -G admins -c 'USER user' user
getent passwd user >/dev/null 2>&1 && chage -M -1 user >/dev/null


%install
# sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sudoers.d
install    -m 440 %{_sourcedir}/admins/etc/sudoers.d/admins %{buildroot}/%{_sysconfdir}/sudoers.d/admins

install -d -m 700 %{buildroot}/home/user/.ssh
install    -m 600 %{_sourcedir}/unix_admins/home/user/.ssh/authorized_keys %{buildroot}/home/user/.ssh/authorized_keys

%clean

%files
%attr(440,root,root) %{_sysconfdir}/sudoers.d/admins
%attr(700,user,user) /home/user/.ssh
%attr(600,user,user) /home/user/.ssh/authorized_keys

%post
printf 'user:$sha512password' | chpasswd -e