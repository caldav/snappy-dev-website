# Setting up your [[DEVICE_NAME]]

![[[DEVICE_NAME]] image]([[DEVICE_IMG_URL]] "[[DEVICE_NAME]] image")

From your ubuntu desktop computer, you can download and install a pre-built Snappy Ubuntu Core [[RELEASE_VERSION]] image for your [[DEVICE_NAME]] and copy it to an SD card ready to boot.

> Make sure your board is connected to the same network as your computer to manage Ubuntu Core remotely via SSH, or has a screen and keyboard attached if you prefer managing Ubuntu Core directly on the board.

## Downloading and installing

1. Start by **downloading the Ubuntu Core image** for Raspberry Pi 2 in your current folder.
```sh
wget [[IMAGE_URL]]
```

1. **Insert your SD card**. Ensure there is no data you care about on the SD card before running the commands below.

1. **Unmount it**: if your SD card is mounted when you insert it into your computer (you will know it if the file manager automatically opens a window showing the card's contents), you must manually unmount it before writing the snappy image to it. Either eject your SD card from the file manager, or from the command line: `sudo umount /media/$USER/`

1. **Copy your downloaded image to the SD card**. You must specify the path to the disk device representing your SD card in the dd command below. Common device paths for the SD card disk device are either of the form **/dev/sdX** (such as **/dev/sdb**, not /dev/sdb1!) or **/dev/mmcblk0** (not /dev/mmcblk0p1!)
```sh
xzcat [[IMAGE_FILENAME]] | sudo dd of=/dev/sdX bs=32M
sync
```

1. **Eject** the SD card physically from your PC and **insert it** in your [[DEVICE_NAME]].

##IMPORT ../first_login.md
