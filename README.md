### pkgkeeper
This Python script can be used to add or remove packages from the 'hold' state in the Advanced Package Tool on Debian-based systems.

For example, it could be assigned to a different Puppet/Ansible class level in order to keep track of packages that should not be updated.
```
class { "pkgkeeper":
  keep_packages => ['nginx','openssl']
}
```
