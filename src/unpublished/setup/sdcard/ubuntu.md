##IMPORT setup-intro.md

## Downloading and installing

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your current folder.
```sh
wget [[IMAGE_URL]]
```
Once the download is finished, you’ll have a zip file named [[IMAGE_FILENAME]].

1. **Insert your SD card**. Ensure there is no data you care about on the SD card before performing next steps below.

1. **Unmount it**: if your SD card is mounted when you insert it into your computer (you will know it if the file manager automatically opens a window showing the card's contents), you must manually unmount it before writing the snappy image to it. Either eject your SD card from the file manager, or from the command line: `sudo umount /media/$USER/`

1. **Copy your downloaded image to the SD card**. You must specify the path to the disk device representing your SD card in the dd command below. Common device paths for the SD card disk device are either of the form **/dev/sdX** (such as **/dev/sdb**, not /dev/sdb1!) or **/dev/mmcblk0** (not /dev/mmcblk0p1!)
```sh
xzcat [[IMAGE_FILENAME]] | sudo dd of=/dev/sdX bs=32M
sync
```
 You will be prompted to enter your password after this command.

 > Note that this operation length can vary depending on your SD card speed. There is no progress displayed unless you send SIGINFO signal pressing Ctrl+T.

1. **Eject** the SD card physically from your PC and **insert it** in your [[DEVICE_NAME]].

##IMPORT ../first_boot.md

##IMPORT ../setup-outro.md
