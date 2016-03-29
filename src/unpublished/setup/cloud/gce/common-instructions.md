### Setup your account and configuration

Now that you have a Google Compute Engine account setup and the cli tools installed, you'll need to configure the tools.

1. The Google Cloud SDK uses OAuth2 to authenticate the CLI commands.
```sh
$ gcloud auth login
<follow the on-screen instructions>
```

1. To make CLI use easier, let's set a couple of things up as default. First let's set a default project.
```sh
$ gcloud config set project <ID OF PROJECT>
```

1. Let's set default zone and region. Before you set default zone and region, you'll need to figure out what are
available. To get a list of the zones run:

```sh
$ gcloud compute zones list
NAME           REGION       STATUS          NEXT_MAINTENANCE TURNDOWN_DATE
asia-east1-b   asia-east1   UP
asia-east1-c   asia-east1   UP
asia-east1-a   asia-east1   UP
europe-west1-c europe-west1 UP
europe-west1-b europe-west1 UP
europe-west1-a europe-west1 UP (DEPRECATED)
us-central1-f  us-central1  UP
us-central1-b  us-central1  UP
us-central1-a  us-central1  UP
```

In our example, we'll pick **us-central1-f** as our default:
```sh
$ gcloud config set compute/zone us-central1-f
$ gcloud config set compute/region us-central1
```

1. It's now time to get SSH keys setup and Google Compute Engine configured to use them. If you already have an SSH key, you ca
 skip creating an SSH key. Otherwise, create an SSH key for login in:
```sh
$ ssh-keygen -t ecdsa -b 521 -f ~/.ssh/google-ecdsa
```

Let's pass the SSH key information to the Compute Engine. The following command will add the SSH key to every instance launched
```sh
$ gcloud compute project-info add-metadata --metadata-from-file sshKeys=~/.ssh/google-ecdsa.pub
```

##IMPORT ../ssh-enable.md

### Available Images
Here's how you can find the list of available snappy images on GCE:
```sh
$ gcloud compute images list --no-standard-images --project ubuntu-snappy
NAME                                       PROJECT       ALIAS DEPRECATED STATUS
[[IMAGE_ID]] ubuntu-snappy                  READY
```

In this example, we are going to use [[IMAGE_ID]] as the image name.

### First Ubuntu Core instance

 The following command will create and launch an instance. It will return when the instance has launched and is available.
 ```sh
$ gcloud compute instances create \
snappy-test \
--image-project ubuntu-snappy \
--image [[IMAGE_ID]] \
--metadata-from-file user-data=cloud.cfg
```

That's it. Your instance is ready to login to now via ssh using the external IP address returned from the successful instance creation.

### Check that the instance is running

Typically you would use gcloud compute ssh <name> at this point for a regular Ubuntu instance. However, at this time,
Ubuntu Core does not have event-based user creation. So you will need to manually SSH in as the Ubuntu user:
```sh
$ ssh -i ~/.ssh/google-ecdsa ubuntu@<EXTERNAL IP ADDRESS>
```
