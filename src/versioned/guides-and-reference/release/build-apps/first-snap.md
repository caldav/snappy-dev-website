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

![Snapcraft diagram](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/snapcraft-diagram.png)

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
    source: https://github.com/didrocks/asciinema-local-server
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
    source: https://github.com/asciinema/asciinema
    source-type: git
  recorder-command-glue:
    plugin: copy
    source: https://github.com/didrocks/recorder-command
    source-type: git
    stage-packages: [qrencode, byobu]
```

The **asciinema** part is referencing the **go** plugin will install golang on the system, fetch its dependencies,
build and install into `parts/asciinema` subdirectory. It is that easy!

We are also adding another **recorder-command-glue** part, referencing as well another source which is a couple of shell
scripts calling as told previously **asciinema**, **qrencode**, **byobu**

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

## The whole snapcraft.yaml

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
    source: https://github.com/didrocks/asciinema-local-server
    source-type: git
  asciinema:
    plugin: go
    source: https://github.com/asciinema/asciinema
    source-type: git
  recorder-command-glue:
    plugin: copy
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

Exit the classic dimension (or open another ssh connexion to the board) and head over to the `aas` directory.

Install it and check the vlc stream service:
```sh
sudo snappy install ascii-as-a-service-demo_0.42_amd64.snap
sudo snappy service logs ascii-as-a-service-demo
2016-03-14T07:55:51.026182Z ubuntu-core-launcher No file to read provided yet. Use http://<machine_ip>:8042 to provide the url you want to convert to ascii
```

-> It means the service is started! It's waiting to have a working file indicating what to install.

> Pro tip! If your application service doesn't work, an easy way to debug it, instead of running
`sudo snappy service restart` and `sudo snappy service logs <name>` continously, it to turn the daemon temporary as
a command. (remove `daemon: simple`). Then, you can use the command directly executing `<snapname>.<appname>`!
