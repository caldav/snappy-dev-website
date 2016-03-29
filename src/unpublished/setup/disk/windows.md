##IMPORT setup-intro.md

## Downloading and installing

1. Start by **downloading the Ubuntu Core image** for [[DEVICE_NAME]] in your **Downloads** folder from [this link]([[IMAGE_URL]]).
Once the download is finished, you’ll have a zip file named [[IMAGE_FILENAME]].

1. **Extract** the downloaded zip file into your Downloads folder. You should now have an uncompressed file named [[IMAGE_UNCOMPRESSED_FILENAME]].
> You might have to install archive extractor software, like [7-zip](http://www.7-zip.org/) or similar as the standard tools do not support xz

1. **Insert your SD card, USB card or external disk**. Ensure there is no data you care about on this disk or card before performing the next steps below.

1. **Copy your downloaded image to the SD card or external disk**. Install and launch [Win32DiskImager](http://sourceforge.net/projects/win32diskimager/files/latest/download).
 > Find out where what drive your SD/USB card or external disk is mounted to. Open a File Explorer window to check which drive your didk is listed under.  Here is an example of a card listed under **E:** and the setup in Diskimager.

 ![Windows drives](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/setup/windows-drives.png)

  Win32DiskImager will need 2 elements:
   * *An Image File* which is the file you want to copy on your disk. Navigate to your *Downloads* folder and select the [[IMAGE_UNCOMPRESSED_FILENAME]] image you have just extracted.
   * *A Device* which is the location of your SD/USB card or external disk. Select the Drive in which it is mounted.

   ![Win32DiskImager image selection](https://raw.githubusercontent.com/ubuntu-core/snappy-dev-website/master/src/img/setup/windows-diskimager-setup.png)

  > To be safe, unplug every External USB Drive you may have connected to your PC.

  When ready click on Write and wait for the process to complete.

1. Exit from Win32DiskImager. **Eject** the SD/USB card or external disk from the File Explorer window and **insert or attach it** in your [[DEVICE_NAME]].

##IMPORT ../first_boot.md

##IMPORT ../setup-outro.md
