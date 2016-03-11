# This is how to setup your dev environment with snapcraft

Snappy Ubuntu Core is using snapcraft to assemble and package your great (or other's people) work in a single snap!

However, you might wonder how to develop and test it as Snappy Ubuntu Core is at the heart a read-only system! This is where enters the **classic mode**.

## Classic mode

The classic mode is simply a classic Ubuntu installation, which can live inside a secured container inside your Snappy Ubuntu Core system. In this one, you will find the traditional *apt* tools, be able to install *debs* and so on.

What about security and confinement then? This is actually easy: the classic mode is *only for developing* on your system. It *isn't started at boot time*, and so, can't contain services you would expect to run. Living in a container, it is *isolated* from the main system (so what you install there, won't be accessible to Ubuntu Core) and only have *few directories* like the user's home directory *in common* to share data.

## Enabling classic mode

You just need to download and enable classic mode once on your Snappy Ubuntu Core system. Once you are logged in it, run:
```sh
$ sudo snappy enable-classic
84.21 MB / 84.21 MB [======================================] 100.00 % 1.73 MB/s
Classic dimension enabled on this snappy system.
Use “snappy shell classic” to enter the classic dimension.
```

## Entering classic mode

Each time you want to have access to classic mode, run:
```sh
ubuntu@localhost$ sudo snappy shell classic
Entering classic dimension


The home directory is shared between snappy and the classic dimension.
Run "exit" to leave the classic shell.

(classic)ubuntu@localhost:~$
```

You will see that the prompt is changed to something similar than `(classic)ubuntu@localhost:~$`. You can here run the classic *apt* commands like `apt update && apt dist-upgrade` to upgrade your classic environment librairies, `apt install <package_name>` to install new package names.

As told, the home directory is shared and so you can share data with the base Snappy Ubuntu Core system this way.

## Installing snapcraft

Let's install snapcraft now!
```sh
$ sudo apt install snapcraft
```

Congrats! Your system in now setup for developing on Snappy Ubuntu Core!
