# Getting a shell access to your board

You can then access your snappy Ubuntu Core system either directly with a keyboard and display connected, or through SSH:
```sh
ssh ubuntu@webdm.local
```
The default *password* is **ubuntu**.

As soon as you get a prompt similar to this, you are good to go!
```sh
ubuntu@webdm.local:~$
```

> Note that if you have multiple Ubuntu Core systems on the same network, the webdm.localo aliases can conflicts.
In that case, you need to retrieve the ip address of the machine by connecting the keyboard/display combo to it.
Once logged in, just use: `ifconfig` and note the ip address. You can then connect to your board via `sh ubuntu@<ip_address>`.
