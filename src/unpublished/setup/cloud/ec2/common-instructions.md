### Setup your account and configuration

When you sign up for EC2, you will be given a secret key and an access key. To use the ec2-* commands below, you with either need to export them to your environment. [See the AWS help for adding the commands](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html).

Alternatively you can use `-O <ACCESS_KEY> -W <SECRET_KEY>` for all ec2-* commands.

1. It's now time to get SSH keys setup and Google Compute Engine configured to use them. If you already have an SSH key, you can
 skip creating an SSH key. Otherwise, create an SSH key for login in:
```sh
$ ssh-keygen -t ecdsa -b 521 -f ~/.ssh/snappy-[[DEVICE_ID]]
```

1. Let's pass the SSH key information to EC2. The following command will import the key in to EC2, so we can specify it
whenever we launch an instance:
```sh
$ ec2-import-keypair -f ~/.ssh/snappy-[[DEVICE_ID]].pub snappy-[[DEVICE_ID]]
```

##IMPORT ../ssh-enable.md

### Available Images
Due to the unique way that Ubuntu Core is built, only HVM instances are available. We do not foresee making paravirtual
images available as Amazon is recommending HVM instance types.

Here's how you can find the list of available snappy images on EC2:
```sh
$ ec2-describe-images \
      -o 099720109477 \
      | grep ubuntu.*stable
```

**099720109477** is the Canonical Account ID. In the coming days, we will be adding indexing to make it easier to find the latest version of Ubuntu Core.

In this example, we are going to use [[IMAGE_ID]] as the image name.

### First Ubuntu Core instance

 The following command will create and launch an instance.
 ```sh
 $ ec2-run-instances <IMAGE_ID> \
  --region us-east-1 --key snappy-[[DEVICE_ID]] \
	--instance-type m3.medium \
	--user-data-file cloud.cfg
```

Which will output something quite a bit of instance details. Look for INSTANCE i-XXXXX. For example:

```
RESERVATION     r-3ad841d4     <TRUNCATED...>
INSTANCE        i-cd2cb333     <TRUNCATED...>
```

The **i-cd2cb333** is the instance ID. To find out what the public address is, run (replace **i-cd2cb333** with your instance ID):

```sh
$ ec2-describe-instances i-cd2cb333 | awk '/INSTANCE/{print$4}'
```

That's it. Your instance is ready to login to now via ssh using the external IP address returned from the successful instance creation.

### Check that the instance is running

Typically you would use gcloud compute ssh <name> at this point for a regular Ubuntu instance. However, at this time,
Ubuntu Core does not have event-based user creation. So you will need to manually SSH in as the Ubuntu user:
```sh
$ ssh -i ~/.ssh/snappy-[[DEVICE_ID]] ubuntu@<EXTERNAL IP ADDRESS>
```
