### SSH configuration

SSH is disabled by default on snappy systems, for enhanced security. You can turn it on by providing some configuration
when you launch the instance, and for that you will need to create a cloud-init configuration file that will turn on SSH
so you can login to play with Ubuntu Core.

Create a file called `cloud.cfg` with the exact lines of text you see below:
```
# cloud-config
snappy:
    ssh_enabled: True
```
