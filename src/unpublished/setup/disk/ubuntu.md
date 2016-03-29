##IMPORT setup-intro.md

## Downloading and installing

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your current folder.
```sh
wget [[IMAGE_URL]]
```
Once the download is finished, you’ll have a zip file named [[IMAGE_FILENAME]].

1. **Insert your SD card, USB card or external disk**. Ensure there is no data you care about on this disk or card before running the commands below.

1. **Unmount it**: if your SD/USB card or external disk is mounted when you insert it into your computer (you will know it if the file manager automatically opens a window showing the disk's contents), you must manually unmount it before writing the snappy image to it. Either eject your SD/USB card or external disk from the file manager, or from the command line: `sudo umount /media/$USER/`

1. **Copy your downloaded image to the SD/USB card or external disk**. You must specify the path to the disk device representing your destination disk in the dd command below. Common device paths for those are either of the form **/dev/sdX** (such as **/dev/sdb**, not /dev/sdb1!) or **/dev/mmcblk0** (not /dev/mmcblk0p1!)
```sh
xzcat [[IMAGE_FILENAME]] | sudo dd of=/dev/sdX bs=32M
sync
```
 You will be prompted to enter your password after this command.

 > Note that this operation length can vary depending on your destination disk speed. There is no progress displayed unless you send SIGINFO signal pressing Ctrl+T.

1. **Eject** the SD card physically from your PC and **insert it** in your [[DEVICE_NAME]].

##IMPORT ../first_boot.md

##IMPORT ../setup-outro.md
