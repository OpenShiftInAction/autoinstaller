# OpenShift in Action Autoinstaller

The `autoinstaller` application automates the deployment of an OpenShift cluster that's an analogue to Appendix A in _OpenShift in Action_. It also helps you complete the tasks for each chapter quickly if you break your system and want to quickly catch up.

<!-- TOC START min:1 max:3 link:true update:true -->
- [OpenShift in Action Autoinstaller](#openshift-in-action-autoinstaller)
  - [Prerequisites for using autoinstaller](#prerequisites-for-using-autoinstaller)
  - [Testing Matrix](#testing-matrix)
  - [AWS Quickstart](#aws-quickstart)
  - [Getting started and configuration](#getting-started-and-configuration)
    - [Global configurations](#global-configurations)
    - [AWS Provider](#aws-provider)
    - [KVM Provider](#kvm-provider)
    - [Openstack Provider](#openstack-provider)
    - [Other provider](#other-provider)
    - [Debug](#debug)
    - [Sample autoinstaller.conf](#sample-autoinstallerconf)
  - [Usage](#usage)
    - [Options](#options)
    - [Multiple providers in a single configuration](#multiple-providers-in-a-single-configuration)
  - [Advanced Usage](#advanced-usage)
    - [Ansible Roles](#ansible-roles)
  - [Contributing](#contributing)

<!-- TOC END -->

## Prerequisites for using autoinstaller

* Ansible on a linux system (tested using Ansible 2.2.2.0+)
* git, to clone this repository
* Some sort of platform to deploy OpenShift on. Currently supported platforms:
  * AWS (EC2)
  * OpenStack
  * Linux (kvm/libvirt)
  * Other (virtual machines or bare metal systems already running CentOS 7)
* Any special prerequisites for a given provider will be spelled out in its own section.

## Testing Matrix

Providers and OpenShift versions that have been tested to date. Feel free to help!

| Provider | Origin 3.6 | Origin 3.7 | OCP 3.6 | OCP 3.7 |
|----------|------------|------------|---------|---------|
| AWS      |   :heavy_check_mark:        |    :heavy_check_mark:       |    :heavy_check_mark:    |         |
| KVM      |   :heavy_check_mark:        |    :x:       |    :x:     |    :x:     |
| OpenStack|            |            |         |         |
| Other    |            |            |         |         |

The KVM provider is currently blocked from deploying OCP by issue https://github.com/OpenShiftInAction/autoinstaller/issues/4

## AWS Quickstart

* Clone this repository on to a Linux server (Fedora is preffered)
* Set up your environment variables for [your AWS API secret and key](#access-environment-variables).
* Set up your `autoinstaller.conf` as follows (NOTE: `ssh_key_file` must [already be created](#ssh-key-file)).:
```
[global]
openshift_version = 3.6
openshift_type = origin
deployment = aws
ssh_key_file = /home/<YOUR_USER>/.ssh/id_rsa
deploy_catalog = true

[aws]
region = us-east-1
sec_group = openshift
flavor = m4.xlarge
ssh_key_name = oia_key
```
* run the following command:
`$ ./autoinstaller.py`

That's it. This will create 2 instances in AWS and deploy an OpenShift cluster for you.

## Getting started and configuration

Autoinstaller uses an [ini configuration file](https://wiki.python.org/moin/ConfigParserExamples). This is the only configuration you have to make to deploy OpenShift with the autoinstaller.

### Global configurations

The config file starts with a section named `[global]`. This is where you'll define a few global parameters for your cluster.

#### openshift_version

The version of OpenShift you'd like to deploy. _OpenShift In Action_ is written using version 3.6, but testing with 3.7 is in progress, and autoinstaller will be updated as new versions are released.

#### openshift_type

The type of OpenShift to deploy. For _OpenShift In Action_ this value should be `origin`. The other possible option is `openshift-enterprise`, which deploys [Red Hat OpenShift Container Platform](https://www.redhat.com/en/technologies/cloud-computing/openshift).
You must set your RHN credentials and the appropriate RHN pool ID in order to install `openshift-enterprise`:
```
export RHN_USERNAME=<your RHN user ID>
export RHN_PASSWORD=<your RHN password>
export RHN_POOL_ID=<A pool ID with Openshift Enterprise subscription>
```


#### ssh_key_file

The SSH key your OpenShift cluster will use. For cloud providers, the public key will be uploaded and the private key placed on the master. For traditional virtualization platforms and bare metal systems, the public keys are distributed to all nodes and the private key on the master.

Autoinstaller assumes the following:

1. `ssh_key_file` is a path to an SSH private key on the Linux system autoinstaller is running on.
1. The corresponding public key is in the same directory, with the same file name, and containing the `.pub` file extension.

On Linux, ssh keys can be generated using the `ssh-keygen` utility. If you need to generate your ssh key on Windows, [this link](https://docs.joyent.com/public-cloud/getting-started/ssh-keys/generating-an-ssh-key-manually/manually-generating-your-ssh-key-in-windows) should be helpful.

#### deployment

The provider to use for your OpenShift cluster. This parameter is used to reference the provider-specific parameters in the next section. Current options are:

##### Current providers

* aws
* kvm
* openstack
* other

Each provider has its own section. You only need to have a single provider defined, but you can define multiple platforms. The `deployment` parameter in `[global]` tells which provider to use for a given deployment.

### AWS Provider

The AWS provider comes complete with a list of CentOS and RHEL 7.4 AMIs for each EC2 region. You don't have to specify them. It just works.

#### Prerequisites

We assume you have used, are using, or are comfortable with using AWS (Amazon Web Services) and its EC2 service. If you're new to AWS, their [_Getting Started with Amazon EC2_](https://aws.amazon.com/ec2/getting-started/) is a great first step.

##### Access environment variables

Everything in AWS requires authentication. Autoinstallers uses environment variables for your AWS secret key and access key set in accordance with [their documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html). The following environment variables need to be set:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

If these variables aren't set on the autoinstaller host, the provider can't function.

##### IAM role to create VPC and Security Group

The API key you use also needs to have the proper permissions to create a VPC, Security Group, and EC2 instances. If managing AWS permissions is new to you, they have [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html) for that, too! It's a solid platform with a pretty low learning curve to get it set up for this purpose.

#### Parameters

##### region

The region where you want to deploy OpenShift

##### sec_group

By default, autoinstaller creates a security group for public access to OpenShift.  

##### flavor

The instance flavor for your instance. `m4.xlarge` matches the OpenShift recommendations. We've tested with `m4.large` instances as well.

##### ssh_key_name

The name on the provider for your ssh key. If it's not already uploaded, autoinstaller will upload your specified key to your cloud provider using this name. This is the key name that will be referenced when instances are created.

### KVM Provider

The KVM provider automatically downloads the proper [CentOS7 cloud image](https://cloud.centos.org/centos/7/images/) to your KVM host and uses that to deploy your OpenShift cluster.

By default, no parameters need to be set.

### Openstack Provider

[OpenStack](https://www.openstack.org) is an industry-leading on-premises cloud platform. It's a lot like having all of AWS' services inside your own datacenter.

Unlike AWS, each OpenStack deployment has a unique image ID that references. You need to tell autoinstaller that information, along with the same information used for EC2.

#### Prerequisites

##### Access environment variables

Like the AWS provider, authentication environment variables are needed to access your OpenStack APIs. Your OpenStack username and passwords need to be available in the following variables on your autoinstaller host:

* `OS_USERNAME`
* `OS_PASSWORD`

If these variables aren't set, this provider can't work.

#### Parameters

##### image

The image ID for your OpenStack cloud that is a CentOS 7 image. This value is a long hash, for example `7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e`, and will be unique to each OpenStack environment.

##### project

The OpenStack project where you want to deploy OpenShift

##### auth_url

The keystone API URL for your OpenStack cluster, for example `http://172.16.0.20:5000/v2.0`.

##### sec_group

By default, autoinstaller creates a security group for public access to OpenShift.  

##### flavor

The instance flavor for your instance. `m4.xlarge` matches the OpenShift recommendations. We've tested with `m4.large` instances as well.

##### ssh_key_name

The name on the provider for your ssh key. If it's not already uploaded, autoinstaller will upload your specified key to your cloud provider using this name. This is the key name that will be referenced when instances are created.

### Other provider

This provider is the monkey wrench for autoinstaller. It doesn't provision your cluster instances. Instead it takes existing instances and deploys OpenShift on them for you.

#### Assumptions

1. You have two CentOS 7 systems (physical or virtual) built out. This can be on any platform (Virtualbox, VMWare, etc.), assuming the rest of the assumptions are met.
1. You have root access to both systems
1. Both systems can communicate with each other freely via a TCP/IP network
1. Both systems can access the internet
1. Both systems have the CentOS 7 installed on one disk, and a second unformatted disk attached to the system.
1. Both systems have at least two CPUs (or VCPUs), 4 GB of RAM, and 10GB of space on the second disk.

#### Parameters

##### master

The IP address or hostname of the system that will be your master server.

##### node

The IP address or hostname of the system that will be your application node.

##### docker_vol

There are two many different physical and virtual systems to account for all possible disk-naming conventions out there. This value is configured for the other providers, and defaults to `/dev/sdb` for this provider. If your servers have a different name for its second disk, you can override that default value with this parameter.

### Debug

The OpenShift deployment process takes 30-45 minutes on average. If you run into issues, you can set the `deploy_openshift` value to `false`. This will deploy your infrastructure and go all the way up to the point OpenShift is actually deployed and stop. This lets you investigate your cluster and

### Sample autoinstaller.conf

```
[global]
openshift_version = 3.6
openshift_type = origin
deployment = kvm
ssh_key_file = /home/jduncan/.ssh/id_rsa
deploy_catalog = true

[aws]
region = us-east-1
sec_group = openshift
flavor = m4.xlarge
ssh_key_name = jduncan_key

[kvm]
install_host = 127.0.0.1

[openstack]
image = 7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e
region = us-east-1
sec_group = openshift
flavor = m4.xlarge
ssh_key_name = jduncan_key

[other]
master = 192.168.122.105
node = 192.168.122.106
docker_vol = /dev/sdb

[debug]
deploy_openshift = true
```

## Usage

To use autoinstaller:

1. Clone this repository on to a Linux system running a RHEL-family version of Linux ([Fedora](https://getfedora.org), [RHEL](https://www.redhat.com), [CentOS](https://www.centos.org)). Currently, we haven't tested autoinstaller on Ubuntu or other Linux distributions. The requirements are minor. If you'd like to help in that regard, please let us know!
```
$ git clone https://github.com/OpenShiftInAction/autoinstaller.git
```
1. Fill our your configuration file. This document should help, and we provide a [sample file](https://raw.githubusercontent.com/OpenShiftInAction/autoinstaller/master/autoinstaller.conf) as well.
1. Run the autoinstaller:
```
$ cd autoinstaller
$ ./autoinstaller
```

Depending on your desired provider and internet connection speed, the entire process could take a while. You are building out an entire OpenShift cluster, after all.

### Options

```
usage: autoinstaller.py [-h] [-c CHAPTER] [--config CONF_FILE] [-p DEPLOYMENT]
                        [-d]

Autoinstaller for OpenShift in Action

optional arguments:
  -h, --help            show this help message and exit
  -c CHAPTER, --chapter CHAPTER
                        chapter you would like to provision through
  --config CONF_FILE    autoinstaller config file, default is
                        autoinstaller.conf
  -p DEPLOYMENT, --provider DEPLOYMENT
                        the deployment provider you'd like to use from your
                        configuration file
  -d, --dry-run         use this option to output the installation command but
                        not launch the installer
```

### Multiple providers in a single configuration

You can have multiple providers in a single `autoinstaller.conf`. To specify a provider or override what is defined in your `[global]` configuration, use the `-p` or `--provider` parameter to specify the provider you want to use.

## Advanced Usage

The goal of autoinstaller is to make it as simple as possible to deploy a multi-node OpenShift cluster. However, there are a ton of additional options you can manipulate beyond this documentation.

The autoinstaller application takes the options in your configuration file and passes them into a collection of Ansible playbooks that provision then your cluster. All variables that are read in are passed to the playbooks as [extra_vars](http://docs.ansible.com/ansible/latest/playbooks_variables.html), the highest level in Ansible's order of precedence.

### Ansible Roles

This project contains two primary types of roles, [_intrastructure_](#infrastructure-roles) and [_OpenShift_](#openshift-roles). The infrastructure roles are designed to build out infrastructure for your cluster on different platforms. OpenShift roles are designed to take those newly created instances and deploy OpenShift.

Each type of supported hypervisor, along with 'other' infrastructure role, has a corresponding Ansible role. Additional roles for other platforms will be added as time and community desires allow. The OpenShift roles shouldn't need too much work, outside of bug fixes and feature requests.

If you'd like to contribute a new infrastructure role, please see the [Contributing](#contributing) section.

#### Infrastructure Roles


#### OpenShift Roles

The OpenShift roles typically don't require a lot of tweaking to work, assuming the provider role has done its job correctly.

##### openshift-common

This role does the preperation steps common to both master and application nodes. There are no options required for this role.

##### openshfit-node

This role sets up your OpenShift nodes, including configuring docker and storage.

##### openshift-master

This role configures your OpenShift master, and performs the actual OpenShift deployment.

## Contributing

If you are an Ansible user and want to add general improvements, or especially addtional hypervisor platforms, PRs and Issues are _most definitely_ welcome!
