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
Custom options:
        accessibility/redshift: +GUI, +VIDMODE
        devel/aarch64-binutils: -STATIC
        devel/cscope: +XCSCOPE
        editors/emacs: -MAILUTILS
        graphics/libpotrace: -A4
        math/gmp: +CPU_OPTS
        math/openblas: +DYNAMIC_ARCH
        net/wireshark: -GTK3, +QT5
        security/pinentry: +QT5, -TTY
        security/vpnc: +SSL
        sysutils/apcupsd: +CGI
        x11-drivers/xorg-drivers: +INTEL, +NV
        x11-fonts/webfonts: +CLEARTYPE, +EXTRAFONTS
        x11/kde4-workspace -> x11/kde-workspace-kde4: -GLES, -GPS, -KACTIVITY, -UPOWER, -VLC, -WALLPAPERS
        x11/kdelibs4 -> x11/kdelibs-kde4: -AVAHI
        x11/xterm: +DABBREV
```
