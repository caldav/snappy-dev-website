# Basic instructions for snappy as a developer

Let's dive into your Ubuntu Core system and see how it feels to get things done the Snappy way!

You need to be logged in to your Ubuntu Core instance to try these commands, they won't work on a traditional apt-get or
deb-based Ubuntu system!

## Differences with a traditional Ubuntu distribution

### Read-only system

Let's check that most of system files (apart from user and snaps data) are read-only, which is what ensure integrity on your system.

```sh
$ sudo touch /foo
touch: cannot touch '/foo': Read-only file system
```

-> we couldn't write in **/** even as root (sudo)!

### No apt-get or debs installs

Ubuntu Core is based on the traditional Ubuntu system, deb-based. However, we don't let in the main partition apt and debs
mixed with snaps, as this will break our transaction and updates story.
```sh
$ apt-get update
Ubuntu Core does not use apt-get, see 'snappy --help'!
$ dpkg -l
dpkg: error: unable to execute dpkg-query (dpkg-query): No such file or directory
```

## Version, channels and default installed snaps

We interact with Ubuntu Core via the **snappy** command. Let's check which version of Ubuntu Core we are on:
```sh
$ snappy info
release: core/16.04/stable
architecture: amd64
apps: snake
```

This is a pristine system, freshly installed with only the snake apps installed. The "release" tells you that you are running
the latest Ubuntu Core's stable release, which is the recommended [image channel](https://developer.ubuntu.com/en/snappy/guides/channels/)
for starting with Snappy.

Let's see which snaps are installed:
```sh
$ snappy list
Name                 Date       Version      Developer
canonical-pc         2016-02-02 3.0          canonical
canonical-pc-linux   2016-02-22 4.4.0-6-1    canonical
ubuntu-core          2016-03-08 16.04.0-24   canonical
snake                2016-02-17 1.0          mectors
```

Each systems have at least 3 snaps installed (the first 3 in our list):
* The base system layer (ubuntu-core)
* The kernel snap (canonical-pc-linux)
* The gadget snap, with some specific configuration to your device (canonical-pc)

## Updating your system

The good news is that the system will update in the background and reboot automatically! You can easily see if updates
are available via:
```sh
$ snappy list -u
Name                 Date       Version
canonical-pc         2016-02-02 3.0
ubuntu-core*         2016-03-08 16.04.0-24
snake                2016-02-17 1.0          mectors
```

Do you note (*) next to ubuntu-core? This means a new update is available and that the kernel is probably already downloading on your system!

You will simply run it once it's downloaded (the message `Reboot to use ubuntu-core version 16.04.0-25` would appear on
any `snappy list` command) and after performing a reboot (`sudo reboot`). You can check using the verbose list mode that
two base system snaps are present on the system:
```sh
$ snappy list -v
Name                 Date       Version      Developer
canonical-pc         2016-02-02 3.0          canonical*
canonical-pc-linux   2016-02-22 4.4.0-6-1    canonical*
ubuntu-core          2016-03-08 16.04.0-24   canonical
ubuntu-core          2016-03-09 16.04.0-25   canonical*
snake                2016-02-17 1.0          mectors*
```

The active flag (*) tells you that this version of the component is what is currently running. Here ubuntu-core 16.04.0-25. Only one snap of a given name can be active at a time. Older snap versions are garbage collected after a while.

## Installing a package from the store

It's time to search and install a second app snaps from the store!
```sh
$ snap find hello
Name           Version   Summary
hello-dbus-app.canonical 1.0.2   hello-dbus-app
hello-dbus-fwk.canonical 1.0.2   hello-dbus-fwk
hello-world.canonical    16.04-3 hello-world
hello-world.elopio       1.0.20  hello-world
hello-world.mvo          2.0     hello-world
```

Let's install the canonical one:
```sh
$ sudo snap install hello-world.canonical
```

The **hello-world** snap is now part of this system!

## Running snap-provided command on your system

Contrary to the **snake** snap, which provided a service app activated at boot, the **hello-world** snap provides multiple commands. Those are available under the *<snap_package>.<command_name>* scheme.

For instance, let's run the *echo* command:
```sh
$ hello-world.echo
Hello World!
```

It works! Remember that one of the key concepts of Snappy Ubuntu Core is security, and that snaps can't have access to the whole system and perform evil actions:
```sh
$ hello-world.evil
Hello Evil World!
This example demonstrates the app confinement
You should see a permission denied error next
/snaps/hello-world.canonical/5.0/bin/evil: 9: /snaps/hello-world.canonical/5.0/bin/evil: cannot create /var/tmp/myevil.txt: Permission denied
```

Phew, that was close! Finally, let's check which environments variables are accessible to our snap commands:
```sh
$ hello-world.env | grep SNAP
SNAP_APP_PATH=/snaps/hello-world.canonical/5.0
SNAP_ORIGIN=canonical
SNAP_APP_USER_DATA_PATH=/home/ubuntu/snaps/hello-world.canonical/5.0
SNAP_FULLNAME=hello-world.canonical
SNAP_USER_DATA=/home/ubuntu/snaps/hello-world.canonical/5.0
SNAP_DATA=/var/lib/snaps/hello-world.canonical/5.0
SNAPP_APP_TMPDIR=/tmp
SNAP_NAME=hello-world
SNAP_APP_TMPDIR=/tmp
SNAP_OLD_PWD=/home/ubuntu
SNAP_ARCH=amd64
SNAP_VERSION=5.0
SNAP=/snaps/hello-world.canonical/5.0
SNAP_DATA=/var/lib/snaps/hello-world.canonical/5.0
```

**SNAP_DATA** and **SNAP_USER_DATA** are the writable directories for your snaps. Your application and services will always start with **SNAP_DATA** as your current directory.

> Note that those variables are versioned. When you update your snap, the content will be **copied** under a new directory. This is what enables the `snap rollback` functionality, ensuring that you get back to an older version without having to care about data format compatibility!

## Uninstalling an snap

Unsurprisingly, removing a snap is just:
```sh
$ sudo snap remove hello-world.canonical
```

This removes this snap and all older snaps

> Note that this doesn't remove snap associated data that we previously mentioned. It means you can reinstall your snap and get access to the same data! `sudo snap purge hello-world.canonical` will though.
