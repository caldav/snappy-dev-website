## Installing from Live disk

Now that you have your Live Disk USB key, we will install the Ubuntu Core image after booting that Live Disk.

<<BIOS_INSTRUCTIONS>>

### Booting from the Live CD

1. Insert the USB key with the Ubuntu live distribution
1. Start you [[DEVICE_NAME]] and push **[[BOOT_SELECT_KEY]]** to enter the boot menu.
1. Select the USB key as boot option.
1. Choose **"Try Ubuntu without installing”**.

### Installing Ubuntu Core onto your [[DEVICE_NAME]]

Once the Live distro is running, open a terminal with the key combination Ctrl+Alt+t.

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your current folder.
```sh
wget [[IMAGE_URL]]
```
Once the download is finished, you’ll have a zip file named [[IMAGE_FILENAME]].

1. **Copy your downloaded image to the disk**. You must specify the path to the disk device representing your disk in the dd command below. Common device paths for the ssd disks are of the form **/dev/sdX** (such as **/dev/sda**, not /dev/sda1!). <<EMMC_DISK_INSTRUCTIONS>>
```sh
xzcat [[IMAGE_FILENAME]] | sudo dd of=/dev/sdX bs=32M
sync
```

 > Note that this operation length can vary depending on your disk speed. There is no progress displayed unless you send SIGINFO signal pressing Ctrl+T.

1. ​You can now **reboot** your [[DEVICE_NAME]]
