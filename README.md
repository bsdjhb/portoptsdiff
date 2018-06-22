# portoptsdiff

The portoptsdiff.py tool can be used to provide a summary of the non-default
settings in a port options database.

Usage: portoptsdiff.py [portsdir [dbdir]]

The default ports directory is ```/usr/ports```.

The default database directory is determined by requesting the value of
the ```PORT_DBDIR``` value from the ports tree (e.g. ```/var/db/ports```).

An example of comparing the summary of options against a poudriere
option database:

```
> poudriere ports -l
PORTSTREE METHOD TIMESTAMP           PATH
ports     -                          /usr/ports
> python portoptsdiff.py /usr/ports /usr/local/etc/poudriere.d/ports-options
```
