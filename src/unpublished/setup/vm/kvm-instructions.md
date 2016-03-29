## Checking for KVM support

Now that you have your Ubuntu installation running, we will install KVM and check that your hardware has the support
enabled before downloading the Ubuntu Core image.

### KVM setup

1. Open a terminal with the key combination Ctrl+Alt+t.
1. Run
```sh
$ sudo apt install qemu-kvm
```
1. Once installed, check for the hardware acceleration support:
```sh
$ kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

This is the best outcome — it means that snappy will run fast on your system, taking advantage of hardware acceleration
in your CPU. If KVM is not supported on your system we recommend you try Ubuntu Core on a cloud instead.

### Download and preparing your Ubuntu Core image

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your current folder.
```sh
wget [[IMAGE_URL]]
```
Once the download is finished, you’ll have a zip file named [[IMAGE_FILENAME]].

1. **Unpack your downloaded image to the disk**.
```sh
unxz [[IMAGE_FILENAME]]
```

You should now have an uncompressed file named [[IMAGE_UNCOMPRESSED_FILENAME]].

 > Note that this operation length can vary depending on your disk speed. There is no progress displayed unless you send SIGINFO signal pressing Ctrl+T.

### Start your KVM instance

You can now launch this virtual machine with KVM:
```sh
$ kvm -m 512 -redir :8022::22 -redir :8080::80 -redir :8042::4200 [[IMAGE_UNCOMPRESSED_FILENAME]]
```

You should see a window pop up, with your Ubuntu Core virtual machine booting inside it.

 > Note that we redirect some ports from the guest Ubuntu Core image to the host. Here:
 > Port 22 (ssh) is redirected to 8022, port 80 to 8080 and port 4200 (webdm default port) to 8042.
 > When you get instructions to connect to some ports on the guests, you can replace with localhost:<host_port> instead.

Consequently, to connect to your VM, you will need to replace ```ssh ubuntu@webdm.local``` by
```ssh -p 8022 ubuntu@localhost```.
