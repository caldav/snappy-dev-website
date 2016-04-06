# Building our first snap!

It's quite often we have to share for demonstrations some command line typing to an audience group. It would be awesome
to have a shell that can record the exact output on multiple terminals, and be able to broadcast that to an audience.
It would be even more exciting if that recording is available for copy and paste so that people can simply reproduce
the exercise locally!

This is exactly what I'm proposing for us to do together without writing any code! We are going to reuse existing pieces
of infrastructures, mainly:
* *asciicinema*, a terminal recorder, that we are going to pull directly from this golang upstream github project and
build!
* *qrencode* and *byobu*, 2 debian packages directly coming from the ubuntu distribution. This will enable us to print
a qr code referencing directly a particular recording. byobu is going to enable us to have multiple tabs and split
sharing inside the terminal.
* a webserver, also published on github and written in nodejs, referencing all found asciinema files on the system and
be able to play it. Some websocket tech enables a live view from it and also to directly reference from some url a particular recording.
* a little bit of glue code to start asciicinema, launch byobu and print the qrcode, also published on github.

Finally, once installed, people just have to head over to http://<ip_address>:8080, dim down the light, bring popcorn
and enjoy the show!

![Terminal Recorder web](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/terminal-recorder-web.png)

If you want to play with it right away, just install *terminal-recoder-demo.didrocks* from the Store! Head over to
http://webdm.local:8080 to get to the web interface! (Note: not available yet on the store, coming soon.)

## Snapcraft quick overview

Snapcraft is a build and packaging tool which helps you package your software as a snap. It makes it easy to incorporate
components from different sources and build technologies or solutions. Those sources are named **parts** and enable you
to turn any source repository like [github](https://github.com/) or [launchpad](https://launchpad.net/) into a real
opensource store!

We are going to create a **snapcraft.yaml** file to declare the package name, the different **parts** we are assembling, and
which commands app or services app we are going to ship in our package unit, named **snaps**. The **parts** can be some
local source (and so, our snapcraft.yaml file lives along the source), or can be remote
The **.snap** we are going
to build locally will contain the binaries and metadata from our app. This one is unsigned and can be installed locally.

Once we are confident enough with it, we can upload it to the Snappy Ubuntu Core Store, where it gets digital signature
and can be distributed to our users.

![Snapcraft diagram](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/snapcraft-diagram.svg)

## Creating our snapcraft.yaml

Let's create and file the base info in our snapcraft.yaml!

```sh
$ mkdir terminal-recorder
$ cd terminal-recorder
$ snapcraft init
```

-> This created in this aas directory a `snapcraft.yaml` file, containing:
```
name: # the name of the snap
version: # the version of the snap
summary: # 79 char long summary
description: # A longer description for the snap
icon: # A path to an icon for the package - this is optional.
```

Let's fire up your preferred editor (I'm using `vi` which is installed by default, but you can `sudo apt install nano`,
ed, emacs… Remember, you are in a classic ubuntu environment here!). Let's file with this content

```
name: terminal-recorder-demo
version: 0.42
summary: Record your terminal to replay them later!
description: This demo intend to show how to assemble different pieces, some coming from ubuntu, other coming from
 a git repo to create an amazing user experience by recording your terminal input and outputs and provide a webserver
 to replay those.
 This one is part of the demo tour at https://developer.ubuntu.com/snappy/get-started/as-dev
```

> Note that we didn't provide an icon here, but you should if you intend to upload to the store, as you should put great
> care to your summary and description as your future users will base their decision on this to install or not your snap!

## Creating our webserver

### The parts

Let's first create our service which is taking some nodejs webserver code (built using [express.js](http://expressjs.com))
from a git repository and exposing it as a service. Let's append to our file (you can put a line break in this yaml
file to make the different sections clearer):

```
parts:
  webserver:
    plugin: nodejs
    source: https://github.com/didrocks/asciinema-local-server.git
    source-type: git
```

We are creating here a **webserver** part, referencing a git repository. The repository will be cloned into
`parts/webserver` after installing git on the system. You have now access to the widest library store in the world,
few characters away!

You will notice that we are using the **nodejs** plugin, which, as the name infers, is specialized for nodejs projects.
It will take all *npm* dependencies referenced in *package.json* and install, alongside to this source code. If we
wanted to specify dependencies manually, we would have used `node-packages: [list of modules]` instead. Once installed,
it will  simply ship all files that are present in this part to the final snap by a direct copy to the `stage/`
directory at snap build time.

### The service declaration

Shipping an executable file (here `bin/asciinema-local-server` from our git repository) isn't enough for our ubuntu core system
or users to get access to it! We need to declare it, declares its types and the capabilities it needs to access.

> Note: I tend to put those 2 stenzas before the "parts" one, as it's what the snap is exposing to users and system.

```
apps:
  asciinema-service:
    command: bin/asciinema-local-server
    daemon: simple
    plugs: [unconfined-plug]

plugs:
  unconfined-plug:
    interface: old-security
    security-template: unconfined
```

Here, we declare a **asciinema-service** app, of type **daemon** (a service which starts at boot and keeps running).
This one is executing the `bin/asciinema-local-server` script relative to the root of the snap. It uses a **plug** that
we named **unconfined-plug**. This plug is then declared and is using the "unconfined" security template.

We will add security later on, but it's always a good idea to perform those steps:
- start with some unconfined profile, get your snap working on the system. You can them move security permission issues
  away that way.
- then confine your application adding the necessary security permissions. This is required to be available in the
  store.

And we are done with our first service! Let's create now the recording command line tools so that we have something to
feed our service with!

## Creating our record-terminal application

We are going to extend our `snapcraft.yaml` now to reference our record-terminal, which will consists of two parts:
- the **asciinema** upstream code, which we need to build and install
- some glue code, bringing together **asciicinema**, **byobu** and **qrencode**.
Append to the existing stenzas:

```
apps:
  […]
  record-terminal:
    command: record-terminal.limited
    plugs: [unconfined-plug]

plugs:
  […]

parts:
  […]
  asciinema:
    plugin: go
    source: https://github.com/asciinema/asciinema.git
    source-type: git
  recorder-command-glue:
    plugin: copy
    source: https://github.com/didrocks/recorder-command.git
    source-type: git
    files:
      'record-terminal*': '.'
    stage-packages: [qrencode, byobu]
```

The **asciinema** part is referencing the **go** plugin will install golang on the system, fetch its dependencies,
build and install into `parts/asciinema` subdirectory. It is that easy!

We are also adding another **recorder-command-glue** part, referencing as well another source which is a couple of shell
scripts calling as told previously **asciinema**, **qrencode**, **byobu**. We are asking the **copy** plugin to copy
all certain file pattern from the **source** to the destination root (`'record-terminal*': '.'`). We couldn't tell it
to copy everything (`'*': '.`) from source as both **recorder-command-glue** and **webserver** parts are copying the
same file name `README.md` with different content to the same destination.

> Note that those scripts could also be in the same directory than our `snapcraft.yaml` file (we would then just set
`source: .`). This is available with any of the plugins, but for the sake of easiness of this tutorial, we only wanted
you to write this snapcraft.yaml file!

**stage-packages** instructs the *recorder-command-glue* part to download and install the **qrencode** and **byobu**
packages and all their dependencies which aren't part of ubuntu-core snap into `parts/recorder-command-glue`. This
simly mean that this way, you are able to reuse any  of the 58k `.deb` packages that traditional ubuntu provides!
This is that easy, just name the packages you need to embedded them in your snap!

Similar than before, we are exposing an **record-terminal** command, pointing to **record-terminal.limited** (coming
from the recorder-command-glue part). This command will be exposed as **<package_name>.<binary_name>**, and so in our
case `terminal-recorder-demo.record-terminal`.

We can note this isn't a service but a command as we didn't mention `daemon: simple`. We are reusing the same
**unconfined-plug** for the moment.

## Snapcraft.yaml at this step

You should have a resulting file similar to this:
```
name: terminal-recorder-demo
version: 0.42
summary: Record your terminal to replay them later!
description: This demo intend to show how to assemble different pieces, some coming from ubuntu, other coming from
 a git repo to create an amazing user experience by recording your terminal input and outputs and provide a webserver
 to replay those.
 This one is part of the demo tour at https://developer.ubuntu.com/snappy/get-started/as-dev

apps:
  asciinema-service:
    command: bin/asciinema-local-server
    daemon: simple
    plugs: [unconfined-plug]
  record-terminal:
    command: record-terminal.limited
    plugs: [unconfined-plug]

plugs:
  unconfined-plug:
    interface: old-security
    security-template: unconfined

parts:
  webserver:
    plugin: nodejs
    source: https://github.com/didrocks/asciinema-local-server.git
    source-type: git
  asciinema:
    plugin: go
    source: https://github.com/asciinema/asciinema.git
    source-type: git
  recorder-command-glue:
    plugin: copy
    source: https://github.com/didrocks/recorder-command.git
    source-type: git
    files:
      'record-terminal*': '.'
    stage-packages: [qrencode, byobu]
```

And that's all we need!

## Building it!

It's high time to perform our first snap build! Just run:
```sh
snapcraft
```

What's happening there is that all parts are fetched in parallel in their `parts/<part_name>/src`, built in
`parts/<part_name>/build` and installed in `parts/<part_name>/install`. Ubuntu packages are fetched under
`parts/<part_name>/ubuntu`. Then, the install products are assembled in `stage/`. We finally copy the whole content to
the `snap/` directory, in addition some metadata, and wrapper service scripts. This directory is then compressed into
a single **.snap** file, named `terminal-recorder-demo_0.42_amd64.snap` (if you built it on amd64), ready to install!

> In a real world product, it's possible to strip down files we don't necessarily need from the parts or ubuntu
> packages to trim down snap size. We can achieve this trimming down by filtering the files required by our
> snap. This is possible via the *snap:* and *stage:* stenzas filtering the `stage/` to `snap/` copy.
> More information on this is available on the snapcraft documentation.

## Time for testing

Exit the classic dimension (or open another ssh connexion to the board) and head over to the `terminal-recorder` directory.

Install it and play with it!
```sh
cd terminal-recorder
sudo snappy install terminal-recorder-demo_0.42_*.snap
```

Head your browser to http://webdm.local:8080, it will tell you to run `terminal-recorder-demo.record-terminal` on your
ubuntu core machine to start recording. Let's do this!

```sh
$ terminal-recorder-demo.record-terminal
/!\ You are running from a snappy wrapper command, you won't be able to run other snap commands here.
If you want to run other snaps app while still recording, please exit and use instead:
/snaps/terminal-recorder-demo.sideload/current/record-terminal

Enter title of your recording:
```

Feel free to enter now the title under which you are going to publish this recording. Then `byobu` is launched (after a warning if your terminal size may be too large for easy replay on smaller screen size).
Any command and output you enter here are recorded, try to type `ls`, `cd` and other Linux commands! You can open new
terminals with `<F2>`, and navigate between them through `<F3>/<F4>`.

![Terminal Recorder command](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/terminal-recorder-command.png)

Once you logout from the last terminal, you get a, ASCII QR code that can be scanned to have a direct reference url.
If you head again to your browser, you should see as well the page being refreshed automatically with your first
recording ready to be played, title being shown and a recording time. Awesome work!

> Note that as you application is running under a wrapper command, you won't be able to run other commands from it
> (you will get some exception). We are working on this right now. We still wanted to provide a way to record them
> though and that's why we publish the link to /snaps/terminal-recorder-demo.sideload/current/record-terminal, which
> has some logic to run outside of the wrapper command, and thus, this limitation. Note that you can also run
> commands as root using sudo!

## Enabling confinement

To finish our work, it's time to turn on confinement on our snap. Let's see together an effective way to deal with this.
Get back into your classic shell environment with `sudo snappy shell classic`

### Put confinement back

Let's only confine the **asciinema-service** webserver for now. We can't really confine the command as it needs to have
access to the whole file system as a shell, and create pseudo ttys. The Snappy team is currently working on bringing a
"shell" interface security policy for this, but it's not there yet, so we will just keep the **unconfined-plug** plug
for it!

So, let's remove remove the `plugs: [unconfined-plug]` from **asciicinema-service** in your `snapcraft.yaml`:
```
apps:
  asciinema-service:
    command: bin/asciinema-local-server
    daemon: simple
```

And rebuild your snap via `snapcraft`. We can notice that only the last step (creating the snap file) is executed, as
nothing else changed. It will keep the previously built and cache content. If you want to restart from scratch, just run
`snapcraft clean`!

### Debugging the new snap

Before installing your new version, install first the snappy-debug package in your ubuntu core install and run a
security audit tool. We advise you to do it in a new terminal:
```sh
$ sudo snappy install snappy-debug
$ snappy-debug.security scanlog
```

This command will print the history audit logs and wait for new ones. This enables us to see new security denials live!

In another terminal (get out of the classic shell if you are still in it), we install the new snap:
```sh
$ sudo snappy install terminal-recorder-demo_0.42_*.snap
```

> Note that the version is still 0.42. However, if you `snappy list -v`, you will see that 2 versions of the
> **terminal-recorder-demo** is available, with generated version id to segregated data in different directories.

We can see that the service isn't started when trying to refresh http://webdm.local:8080. We can double check via:
```sh
$ sudo snappy service logs terminal-recorder-demo
2016-04-04T14:11:33.304529Z systemd terminal-recorder-demo_webserver_LVWRJdmdbBCp.service: Main process exited, code=killed, status=31/SYS
2016-04-04T14:11:33.305879Z systemd Stopped service webserver for package terminal-recorder-demo.
2016-04-04T14:11:33.306807Z systemd terminal-recorder-demo_webserver_LVWRJdmdbBCp.service: Unit entered failed state.
2016-04-04T14:11:33.307305Z systemd terminal-recorder-demo_webserver_LVWRJdmdbBCp.service: Failed with result 'signal'.
2016-04-04T14:11:33.331206Z systemd Started service webserver for package terminal-recorder-demo.
```

It seems that the service is trying to start and stop and fails. This `Unit entered failed state` and
`Failed with result 'signal'` is a clear indication of this.

If we look at the scanlog window, we can now see:
```sh
= Seccomp =
Time: Apr  4 14:08:59
Log: auid=4294967295 uid=0 gid=0 ses=4294967295 pid=1892 comm="node" exe="/snaps/terminal-recorder-demo.sideload/LVWRJdmdbBCp/bin/node" sig=31 arch=c000003e 55(getsockopt) compat=0 ip=0x7f38ea88de2a code=0x0
Syscall: getsockopt
Suggestions:
* add 'getsockopt' to 'syscalls' in security-override
* add one of 'firewall-management, network-client, network-listener, unix-listener' to 'caps'
```

So, this really means, there is no hope in trying any number of `sudo snappy service restart <snap>` (or stop/start)
to fix it!

### Fixing our snap and trying it

Let's follow what the audit logs says, and as we are listening on incoming requests on the network,
let's add a **network-listener** caps

Enter the classic mode and edit `snapcraft.yaml`:
```
```
apps:
  asciinema-service:
    command: bin/asciinema-local-server
    daemon: simple
    plugs: [listener]

plugs:
  listener:
    interface: old-security
    caps: [network-listener]
  […]
```

The **asciinema-service** is using the **listener** plug pointing to **network-listener** capability.

Rebuild your snap with `snapcraft`, exits the classic shell, install the new version via
`sudo snappy install terminal-recorder-demo_0.42_*.snap` and reload your webbrowser to now enjoy a confined, secured,
webservice!

> Pro tip! If your application service doesn't work at all, an easy way to debug it, instead of running
`sudo snappy service restart` and `sudo snappy service logs <name>` continuously, to get output infos, turn the daemon
temporary as a command. (remove `daemon: simple`). Then, you can use the command directly executing `<snapname>.<appname>`!
This makes iteration way easier!

## Summing it all up

In a very few declarative lines, we have been able to produce a tool recording a multiplexed terminal window, and
publish them through a confined webservice to users so that they can replay them. Note that we merged different
technologies like go, nodejs, scripts and even ubuntu packages to make this independant unit, now ready to be available
on millions of machines!

There are a lot of plugins in snapcraft for different use cases, do not hesitate to explore them via
`snappy help <plugin_name>`!

For reference, the final `snapcraft.yaml` should now look like [this](https://github.com/didrocks/ubuntu-core-exp/blob/master/terminal-recorder/snapcraft.yaml).
