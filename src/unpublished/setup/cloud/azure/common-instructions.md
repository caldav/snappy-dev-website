### Setup your account

Just run:
```sh
$ azure account download
```
Then follow the instructions provided.

Next, prepare your SSH Keys for Azure. Snappy is secure by default; there is no default password. In order to login to
your Ubuntu Core instance on Azure you will need to supply an SSH key that will work with Microsoft Azure.

 * If you have an existing key, let's convert it:
```sh
$ openssl req -x509  -key ~/.ssh/id_rsa -nodes -days 365  \
-newkey rsa:2048 -out ~/.ssh/azure_pub.pem -subj "/CN=${USER}/"
```

 * If you don't have one, let's create a new key:
```sh
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout ~/.ssh/azure.key -out ~/.ssh/azure_pub.pem -subj "/CN=${USER}/"
```
After either of the above **openssl** commands, you'll want to copy the key and **azure_pub.pem** to `~/.ssh`

### Available Images
Here's how you can find the list of available snappy images on Azure:
```sh
$ azure vm image list | grep "Ubuntu-.*-Snappy"
data:    b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-15.04-Snappy-core-amd64-edge-201507020801-108-en-us-30GB
```
The naming convention is: `<publisher guuid>__Ubuntu-<version>-Snappy-<flavor>-<arch>-<publish_date>-<version>-<locale>-<disk_size>`.
Canonical's publisher GUUID on Microsoft Azure is **b39f27a8b8c64d52b05eac6a62ebad85**.

In our example, we'll use the latest image at the time of this writing, which is **[[IMAGE_ID]]**.
We suggest you to replace the tags for date and version to use the latest one available.

### First Ubuntu Core instance
SSH is disabled by default on snappy systems, for enhanced security. You can turn it on by providing some configuration
when you launch the instance, and for that you will need to create a cloud-init configuration file that will turn on SSH
so you can login to play with Ubuntu Core.

1. Create a file called `cloud.cfg` with the exact lines of text you see below:
```
# cloud-config
snappy:
    ssh_enabled: True
```

1. Now you are ready to launch the image on Azure. The general form of this command is:
```sh
$ azure vm create <NAME> <IMAGE> <USER> <PASSWORD> <flags>
```
The following is an example command. Remember to replace the image name by the latest available, and to replace {UNIQUE_ID} with something that uniquely identifies your machine, like snappy-test-{your_nickname} :

```sh
$ azure vm create {UNIQUE_ID} \
[[IMAGE_ID]] ubuntu \
--location "North Europe" --no-ssh-password \
--ssh-cert ~/.ssh/azure_pub.pem --custom-data ~/cloud.cfg -e
```

### Check that the instance is running

You will need to wait a minute or two while Azure provisions and launches the instance. It will show up in the list of your running instances:
```sh
$ azure vm list
info:    Executing command vm list
+ Getting virtual machines
data:    Name         Status     Location      DNS Name                  IP Address
data:    -----------  ---------  ------------  ------------------------  ----------
data:    snappy-test  ReadyRole  North Europe  snappy-test.cloudapp.net  <VARIABLE>
info:    vm list command OK
```

When the image state is **ReadyRole** you can make a note of the hostname from the listing above, and login with SSH to the instance (replace snappy-test.cloudapp.net with the DNS name from your azure vm list command):
```sh
$ ssh -i ~/.ssh/azure.key ubuntu@snappy-test.cloudapp.net
```
