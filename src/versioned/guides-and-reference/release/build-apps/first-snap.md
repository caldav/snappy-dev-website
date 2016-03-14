# Building our first snap!

It's time to invent a new business model, let's create the first world ever video streaming to ascii art output service!
AAS (Ascii As a Service) will publish a small webserver which

And you are going to do all this without writing any code! We are going to reuse existing pieces of infrastructures, mainly:
* *vlc* and *netcat*, directly coming from the ubuntu distribution
* the webserver in go publishing a simple web page to take the stream url and restart vlc when a new link is given. This
  code is published on github.
* a little bit of glue code, also published on github, as a wrapper to start vlc and netcat and read the new link url from
  a file.

Finally, once installed, we will read can just use the ascii video viewer of the future: *telnet*!

<IMGGGGGGGG>

If you want to play with it right away, just install *ascii-as-a-service.didrocks* from the Store! Head over to
http://webdm.local:8042 to get to the web interface!

## Snapcraft quick overview

Snapcraft is a build and packaging tool which helps you package your software as a snap. It makes it easy to incorporate
components from different sources and build technologies or solutions. Those sources are named **parts** and enable you
to turn any source repository like [github](https://github.com/) or [launchpad](https://launchpad.net/) as a real
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
$ mkdir aas
$ cd aas
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
name: ascii-as-a-service-demo
version: 0.42
summary: Convert live streams to ascii output!
description: This demo intend to show how to assemble different pieces, some coming from ubuntu, other coming from
 a git repo to create an amazing user experience on converting content to ascii output.
 This one is part of the demo tour at https://developer.ubuntu.com/snappy/get-started/as-dev
```

> Note that we didn't provide an icon here, but you should if you intend to upload to the store, as you should put great
> care to your summary and description as your future users will base their decision on this to install or not your snap!

## Creating our video-stream-service

### The parts

Let's create our service which is taking some glue code from a git repository and exposing it as a service. Append to
our file (you can give a line break in this yaml file to make the different sections clearer):

```
parts:
  video-stream:
    plugin: nil
    source: https://github.com/didrocks/vlc-netcat-service
    source-type: git
    stage-packages: [vlc]
```

We are creating here a **video-stream** part, referencing a git repository. The repository will be cloned into
`parts/video-stream` after installing git on the system. You have now access to the widest library store in the world,
directly characters away!

> Note that this repository could also be in the same directory than our `snapcraft.yaml` file
(we would then just set `source: .`).

**stage-packages** instructs the *video-stream* part to download and install the **vlc** package and all
its dependencies which aren't part of ubuntu-core snap into `parts/video-stream`. Reusing one of the 58k `.deb` packages
that traditional ubuntu provides is that easy, just name the packages you need to embeeded them in your snap!

Finally, you will notice that we are using the **nil** plugin, which, as the name infers, do nothing. It will simply
ship all files that are present in this part to the final snap by a direct copy to the `stage/` directory at snap build
time.

### The service declaration

Shipping an executable file (here `vlc-netcat-streamer` from our git repository) isn't enough for our ubuntu core system
or users to get access to it! We need to declare it, declares its types and the capabilities it needs to access.

> Note: I tend to put those 2 stenzas before the "parts" one, as it's what the snap is exposing to users and system.

```
apps:
  video-stream-service:
    command: vlc-netcat-streamer
    daemon: simple
    plugs: [unconfined-plug]

plugs:
  unconfined-plug:
    interface: old-security
    security-template: unconfined
```

Here, we declare a "video-stream-service" app, of type daemon (a service which starts at boot and keeps running). This
one is executing the `vlc-netcat-streamer` script located at the root of the snap (we can use a relative path). It
uses a **plug** that we named "unconfined-plug". This plug is then declared and is using the "unconfined" security
template.

We will add security later on, but it's always a good idea to perform those steps:
- start with some unconfined profile, get your snap working on the system. You can them move security permission issues
  away that way.
- then confined your application adding the necessary security permissions. This is required to be available in the
  store.

And we are done with our first service! Let's get to the second one which is a webserver exposing the stream selection
interface.

## Creating our streamchooser-webserver

We are going to extend our `snapcraft.yaml` now to reference our webserver, written in go, append to the existing
stenzas:
```
apps:
  […]
  streamchooser-webserver:
    command: stream-selection-server
    daemon: simple
    plugs: [unconfined-plug]

plugs:
  […]

parts:
  […]
  webserver:
    plugin: go
    source: https://github.com/wisnij/gopaste.git
    source-type: git
```

The "webserver" part is referencing the **go** plugin will install golang on the system, fetch its dependencies,
build and install into `parts/webserver` subdirectory. It is that easy!

Similar than before, we are exposing the "stream-selection-server" executable (coming this build) via the
"streamchooser-webserver" application service. We are reusing the same "unconfined-plug" for the moment.

You should have a resulting file similar to this:
```
name: ascii-as-a-service-demo
version: 0.42
summary: Convert live streams to ascii output!
description: This demo intend to show how to assemble different pieces, some coming from ubuntu, other coming from
 a git repo to create an amazing user experience on converting content to ascii output.
 This one is part of the demo tour at https://developer.ubuntu.com/snappy/get-started/as-dev

apps:
  video-stream-service:
    command: vlc-netcat-streamer
    daemon: simple
    plugs: [unconfined-plug]
  streamchooser-webserver:
    command: stream-selection-server
    daemon: simple
    plugs: [unconfined-plug]

plugs:
  unconfined-plug:
    interface: old-security
    security-template: unconfined

parts:
  video-stream:
    plugin: nil
    source: https://github.com/didrocks/vlc-netcat-service
    source-type: git
    stage-packages: [vlc]
  webserver:
    plugin: go
    source: https://github.com/wisnij/gopaste.git
    source-type: git
```

And that's all we need!

## Building it!

It's high time to perform our first snap build! Just run:
```sh
snapcraft
```

> Note that vlc has a lot of dependency and this can take some download time.

What's happening there is that all parts are fetched in parallel in their `parts/<part_name>/src`, built in
`parts/<part_name>/build` and installed in `parts/<part_name>/install`. Then, the install products are assembled in
`stage/`. We finally copy the whole content to the `snap/` directory, in addition some metadata, and wrapper service
scripts. This directory is then compressed into a single .snap file, ascii-as-a-service-demo_0.42_amd64.snap, ready to
install!

> You will probably notice that the .snap file is quite sizeable. This is because we ship vlc and all its dependencies
> inside it. In a real world product, we would take the time to strip it down by filtering the files required by our
> snap. This is possible via the *snap:* and *filesets:* stenzas filtering the `stage/` to `snap/` copy.
> More information on this is available on the snapcraft documentation.

## Time for testing
