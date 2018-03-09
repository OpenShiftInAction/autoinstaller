# OpenShift in Action Autoinstaller

The `autoinstaller` application leverages Ansible (www.ansible.com) roles and playbooks, along with a little Python, to automate the deployment of an OpenShift cluster that's an analogue to Appendix A in _OpenShift in Action_. It also helps you complete the tasks for each chapter quickly if you break your system and want to quickly catch up.

<!-- TOC START min:1 max:4 link:true update:true -->
- [OpenShift in Action Autoinstaller](#openshift-in-action-autoinstaller)
  - [Getting started](#getting-started)
  - [Autoinstaller configuration](#autoinstaller-configuration)
    - [Global configurations](#global-configurations)
      - [openshift_version](#openshift_version)
      - [openshift_type](#openshift_type)
      - [ssh_key_file](#ssh_key_file)
      - [deployment](#deployment)
    - [Providers](#providers)
      - [AWS](#aws)
      - [KVM](#kvm)
      - [Openstack](#openstack)
    - [Other](#other)
    - [Experiemental](#experiemental)
      - [deploy_metrics](#deploy_metrics)
      - [deploy_cns](#deploy_cns)
      - [deploy_httpd_auth](#deploy_httpd_auth)
  - [Usage](#usage)
    - [Options](#options-2)
    - [Advanced Usage](#advanced-usage)
  - [Application design](#application-design)
    - [Ansible Roles](#ansible-roles)
      - [Infrastructure Roles](#infrastructure-roles)
      - [OpenShift Roles](#openshift-roles)
  - [Contributing](#contributing)

<!-- TOC END -->

* Ansible on a linux system (tested using Ansible 2.2.2.0+)
* git, to clone this repository
* Some sort of platform to deploy OpenShift on. Currently supported platforms:
  * AWS (EC2)
  * OpenStack
  * Linux (kvm/libvirt)
  * Other (virtual machines or bare metal systems already running CentOS 7)
* Any special prerequisites for a given platform will be spelled out in its own section.

## Getting started

Autoinstaller uses an [ini configuration file](https://wiki.python.org/moin/ConfigParserExamples). This is the only configuration you have to make to deploy OpenShift with the autoinstaller.

## Autoinstaller configuration

### Global configurations

The config file starts with a section named `[global]`. This is where you'll define a few global parameters for your cluster.

#### openshift_version

The version of OpenShift you'd like to deploy. _OpenShift In Action_ is written using version 3.6, but testing with 3.7 is in progress, and autoinstaller will be updated as new versions are released.

#### openshift_type

The type of OpenShift to deploy. For _OpenShift In Action_ this value should be `origin`. The other possible option is `openshift-enterprise`, which deploys [Red Hat OpenShift Container Platform](https://www.redhat.com/en/technologies/cloud-computing/openshift).

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

These are outlined in the next section.

### Providers  

Each provider has its own section. You only need to have a single provider defined, but you can define multiple platforms. The `deployment` parameter in `[global]` tells which provider to use for a given deployment.

#### AWS

The AWS provider comes complete with a list of CentOS and RHEL 7.4 AMIs for each EC2 region. You don't have to specify them. It just works.

##### Prerequisites

We assume you have used, are using, or are comfortable with using AWS (Amazon Web Services) and its EC2 service. If you're new to AWS, their [_Getting Started with Amazon EC2_](https://aws.amazon.com/ec2/getting-started/) is a great first step.

###### Access environment variables

Everything in AWS requires authentication. Autoinstallers uses environment variables for your AWS secret key and access key set in accordance with [their documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html). The following environment variables need to be set:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

If these variables aren't set on the autoinstaller host, the provider can't function.

###### IAM role to create VPC and Security Group

The API key you use also needs to have the proper permissions to create a VPC, Security Group, and EC2 instances. If managing AWS permissions is new to you, they have [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html) for that, too! It's a solid platform with a pretty low learning curve to get it set up for this purpose.

##### Options

###### region

The region where you want to deploy OpenShift

###### sec_group

By default, autoinstaller creates a security group for public access to OpenShift.  

###### flavor

The instance flavor for your instance. `m4.xlarge` matches the OpenShift recommendations. We've tested with `m4.large` instances as well.

###### ssh_key_name

The name on the provider for your ssh key. If it's not already uploaded, autoinstaller will upload your specified key to your cloud provider using this name. This is the key name that will be referenced when instances are created.

#### KVM

The KVM provider automatically downloads the proper [CentOS7 cloud image](https://cloud.centos.org/centos/7/images/) to your KVM host and uses that to deploy your OpenShift cluster.

By default, no parameters need to be set.

#### Openstack

[OpenStack](https://www.openstack.org) is an industry-leading on-premises cloud platform. It's a lot like having all of AWS' services inside your own datacenter.

Unlike AWS, each OpenStack deployment has a unique image ID that references. You need to tell autoinstaller that information, along with the same information used for EC2.

##### Prerequisites

###### Access environment variables

Like the AWS provider, authentication environment variables are needed to access your OpenStack APIs. Your OpenStack username and passwords need to be available in the following variables on your autoinstaller host:

* `OS_USERNAME`
* `OS_PASSWORD`

If these variables aren't set, this provider can't work.

##### Options

###### image

The image ID for your OpenStack cloud that is a CentOS 7 image. This value is a long hash, for example `7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e7e9fb03c-734b-4ad2-9244-df8b9c2e2b6e`, and will be unique to each OpenStack environment.

###### project

The OpenStack project where you want to deploy OpenShift

###### auth_url

The keystone API URL for your OpenStack cluster, for example `http://172.16.0.20:5000/v2.0`.

###### sec_group

By default, autoinstaller creates a security group for public access to OpenShift.  

###### flavor

The instance flavor for your instance. `m4.xlarge` matches the OpenShift recommendations. We've tested with `m4.large` instances as well.

###### ssh_key_name

The name on the provider for your ssh key. If it's not already uploaded, autoinstaller will upload your specified key to your cloud provider using this name. This is the key name that will be referenced when instances are created.

### Other



### Experiemental

There are several experimental options in autoinstaller. These may or may not work from one git commit to another. As they are tested and stabilized, they'll become global options.

####  deploy_metrics

If set to `true`, this option deploys the [OpenShift metrics](https://github.com/openshift/origin-metrics) stack at deploy time.

#### deploy_cns

If set to `true`, this option deploys [Container Native Storage](https://access.redhat.com/documentation/en-us/red_hat_gluster_storage/3.3/html/container-native_storage_for_openshift_container_platform/) in your OpenShift cluster.

#### deploy_httpd_auth

If set to `true`, this option configures OpenShift to use an http authentication provider for your cluster (Note: this is done automatically if you're deploying OpenShift on Red Hat Enterprise Linux).

## Usage

To use autoinstaller:

1. Check out this repository on to a Linux system running a RHEL-family version of Linux ([Fedora](https://getfedora.org), [RHEL](https://www.redhat.com), [CentOS](https://www.centos.org)). Currently, we haven't tested autoinstaller on Ubuntu or other Linux distributions. The requirements are minor. If you'd like to help in that regard, please let us know!
1. Fill our your configuration file. This document should help, and we provide a sample file as well.
1. Run the autoinstaller:
```
$ cd autoinstaller
$ ./autoinstaller
```

Depending on your desired provider and internet connection speed, the entire process could take a while. You are building out an entire OpenShift cluster, after all.



### Options

### Advanced Usage


## Application design

### Ansible Roles

This project contains two primary types of roles, [_intrastructure_](#infrastructure-roles) and [_OpenShift_](#openshift-roles). The infrastructure roles are designed to build out infrastructure for your cluster on different platforms. OpenShift roles are designed to take those newly created instances and deploy OpenShift.

Each type of supported hypervisor, along with 'other' infrastructure role, has a corresponding Ansible role. Additional roles for other platforms will be added as time and community desires allow. The OpenShift roles shouldn't need too much work, outside of bug fixes and feature requests.

If you'd like to contribute a new infrastructure role, please see the [Contributing](#contributing) section.

#### Infrastructure Roles

##### kvm-hypervisor

This role takes a Linux hypervisor and creates your cluster on top of it. It is tested on Fedora, and possibly on later ones down the road.

###### Required parameters

* ssh_key - SSH key to use to configure on the virtual machines. For the KVM hypervisor role, this is a file on the system you're running the playbook on.
* ssh_key_pub - the public SSH key that corresponds to ssh_key
* ssh_known_hosts_file - the location to add your node's ssh key fingerprints to. defaults to `/etc/ssh/ssh_known_hosts`.
* kvm_disk_dir - the location to store your cluster's virtual disks. defaults to `/var/lib/libvirt/images`.
* disk_image - the CentOS 7 or RHEL 7 qcow2 cloud image that will be used to create your virtual machines. This needs to be on the system you are launching the playbook from. It will be copied to your hypervisor.
* data_disk_size - Size, in GB, for the data disk. On the nodes, this is used for docker storage. On the masters, this is used for NFS volumes. Defaults to `20` (20GB)

#### OpenShift Roles

##### openshift-common

This role does the preperation steps common to both master and application nodes. There are no options required for this role.

##### openshfit-node

This role sets up your OpenShift nodes, including configuring docker and storage.

###### Required parameters

* docker_dev - Block device to use for container storage. Defaults to `/dev/vdb`.
* docker_vg - Volume group name to use for docker storage. Defaults to `docker_vg`.

##### openshift-master

This role configures your OpenShift masters, and performs the actual OpenShift deployment.

## Contributing

If you are an Ansible user and want to add general improvements, or especially addtional hypervisor platforms, PRs and Issues are _most definitely_ welcome!
