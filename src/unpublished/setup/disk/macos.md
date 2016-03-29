##IMPORT setup-intro.md

## Downloading and installing

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your current folder.
```sh
curl -O [[IMAGE_URL]]
```

1. **Extract** the downloaded zip file into your Downloads folder by double clicking on it. You should now have an uncompressed file named [[IMAGE_UNCOMPRESSED_FILENAME]].
> You might have to install archive extractor software, like [The Unarchiver](https://itunes.apple.com/gb/app/the-unarchiver/id425424353?mt=12) or similar as the standard tools do not support xz

1. **Insert your SD card, USB card or external disk**. Ensure there is no data you care about on this disk or card before running the commands below.

1. **Determine which disk to write to and mount it**.
 * Run
```sh
diskutil list
```
 In the results identify your SD/USB card, or external disk, it will probably an entry like the one below:
```sh
/dev/disk0
  #:                       TYPE NAME                    SIZE       IDENTIFIER
  0:      GUID_partition_scheme                        *500.3 GB   disk0
/dev/disk2
  #:                       TYPE NAME                    SIZE       IDENTIFIER
  0:                  Apple_HFS Macintosh HD           *428.8 GB   disk1
                                Logical Volume on disk0s2
                                E2E7C215-99E4-486D-B3CC-DAB8DF9E9C67
                                Unlocked Encrypted
/dev/disk3
  #:                       TYPE NAME                    SIZE       IDENTIFIER
  0:     FDisk_partition_scheme                        *7.9 GB     disk3
  1:                 DOS_FAT_32 NO NAME                 7.9 GB     disk3s1
```

 Write down the number after /dev/disk that is associated with your disk, in this case 3.

 * Unmount your SD/USB card or external disk by entering the command:
 `diskutil unmountDisk /dev/diskX` where X is the number you just wrote down. When successful you should see a message similar to this one: *Unmount of all volumes on diskX was successful*.

1. **Copy your downloaded image to the SD/USB card or external disk**. Note that you need to specify the path to the disk device with the number you just wrote down in previous step.
```sh
sudo dd if=~/Downloads/[[IMAGE_UNCOMPRESSED_FILENAME]] of=/dev/diskX bs=32MB
sync
```
You will be prompted to enter your Apple password after this command.

 > Note that this operation length can vary depending on your destination disk speed. There is no progress displayed unless you send SIGINFO signal pressing Ctrl+T.

1. **Eject** the SD/USB card or external disk physically from your Mac and **insert or attach it** in your [[DEVICE_NAME]].

##IMPORT ../first_boot.md

##IMPORT ../setup-outro.md
