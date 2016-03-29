### Download your Ubuntu Core image

Simply run:

1. Go to a directory (vagrant workspace) which will contain this configuration for Ubuntu Core.
```sh
cd ubuntu-core
```
1. Now, **download and start the Ubuntu Core image** for [[DEVICE_NAME]].
```sh
vagrant init [[IMAGE_URL]]
vagrant up
```

> Note that only the first vagrant up will download the Ubuntu Core image before starting up. Further vagrant up
> will only spawn some Ubuntu Core instances.

### Ensure your vm is started

Once you see a message stating that the box is up and ready to go, you can login using vagrant ssh.
```sh
vagrant ssh
```

After you are done with the image, you can shut it down with `vagrant shutdown` or `vagrant destroy` to remove the image.
