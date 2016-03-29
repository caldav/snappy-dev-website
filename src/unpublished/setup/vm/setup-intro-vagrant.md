##IMPORT setup-intro.md

For our Vagrant users, we are now publishing Snappy Images for Vagrant. These images are bit-for-bit the same as the KVM images,
but packaged for Vagrant. A special "cloud-config" drive is included that enables SSH.

> Note: Ubuntu core does not support DKMS modules at this time. This means that the shared /vagrant file system is not
supported, but we anticipate supporting shared file systems in the future.
