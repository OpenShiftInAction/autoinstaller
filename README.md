# OpenShift in Action Autoinstaller

This collection of Ansible (www.ansible.com) roles and playbooks is designed to implement the same configuration for a system that is in Appendix A of _OpenShift in Action_.

Currently, these are optimized for _OpenShift Origin 3.6_ and _CentOS 7.3.1611_. Future versions will handle RHEL and OpenShift Container Platform.

## Prerequisites

* Ansible on a linux system (tested using Ansible 2.2.2.0)
* git, to clone this repository
* A supported infrastructure platform, currently KVM.

## Required parameters

There are several required, and more optional, parameters that you need to set to deploy OpenShift. They are outlined in the roles below. You need to create a variables file that customizes them to fit your needs and desires.

## Roles

This project contains two primary types of roles, intrastructure and OpenShift. The infrastructure roles are designed to build out infrastructure for your cluster on different platforms. OpenShift roles are designed to take those newly created instances and deploy OpenShift on top of them.

### Infrastructure Roles

#### kvm-hypervisor

This role takes a Linux hypervisor and creates your cluster on top of it. It is tested on Fedora, and possibly on later ones down the road.

##### Required parameters

* ssh_key - SSH key to use to configure on the virtual machines. For the KVM hypervisor role, this is a file on the system you're running the playbook on.
* ssh_key_pub - the public SSH key that corresponds to ssh_key
* ssh_known_hosts_file - the location to add your node's ssh key fingerprints to. defaults to `/etc/ssh/ssh_known_hosts`.
* kvm_disk_dir - the location to store your cluster's virtual disks. defaults to `/var/lib/libvirt/images`.
* disk_image - the CentOS 7 or RHEL 7 qcow2 cloud image that will be used to create your virtual machines. This needs to be on the system you are launching the playbook from. It will be copied to your hypervisor.
* data_disk_size - Size, in GB, for the data disk. On the nodes, this is used for docker storage. On the masters, this is used for NFS volumes. Defaults to `20` (20GB)

### OpenShift Roles

#### openshift-common

This role does the preperation steps common to both master and application nodes. There are no options required for this role.

#### openshfit-node

This role sets up your OpenShift nodes, including configuring docker and storage.

##### Required parameters

* docker_dev - Block device to use for container storage. Defaults to `/dev/vdb`.
* docker_vg - Volume group name to use for docker storage. Defaults to `docker_vg`.

#### openshift-master

This role configures your OpenShift masters, and performs the actual OpenShift deployment.

##### Required parameters

* virt_type - the virtualization type you're using. Defaults to `kvm`. This is used to make sure the installation inventory is created correctly for your platform.
* deploy_openshift - Defaults to `true`. If you set it to `false`, it will configure your systems, but not actually deploy OpenShift.
* apps_domain: Wilcard domain to use for your application domain. Defaults to `apps.192.168.122.101.nip.io`.
* openshift_type: Which deployment to create. Defaults to `origin`.
* ssh_key - SSH key to use to perform the OpenShift deployment. It will be added to the root user's identity.
* ssh_key_pub - the public SSH key that corresponds to ssh_key. This will hopefully be improved down the road.

Note:
If you're using KVM, you only have to set `ssh_key` and `ssh_key_pub` once in your variables file.

## Inventory

The default inventory file is:

```
[install-hosts]
192.168.122.1 ansible_connection=local

[openshift:children]
openshift-masters
openshift-nodes

[openshift-masters]
ocp1 ip=192.168.122.100 vcpus=2 ram=4096 mac=00:1c:c4:00:00:14 hostname=ocp1.192.168.122.100.nip.io

[openshift-nodes]
ocp2 ip=192.168.122.101 vcpus=2 ram=4096 mac=00:1c:c4:00:00:15 hostname=ocp2.192.168.122.101.nip.io
```

The design is to create essentially as large a cluster as you desire. If you want an HA master control plane, add 3 nodes to the `openshift-masters` group. If you want a larger cluster, add more nodes to the `openshift-nodes` group.

The `install-hosts` group is the system you're installing your cluster on. For KVM, it is your kvm host. For OpenStack, etc, it would be `localhost`.

The node variables set by default are required for KVM to work properly. For other infrastructures, we'll document whether or not you need them.

## Installation and Deployment

Once you have your extra-vars.yaml file created, you can start the deployment process with the following command from the directory you cloned or downloaded the repository into:

```
$ ansible-playbook -i inventory -e @/path/to/extra-vars.yaml site.yaml
```

Depending on your internet connection speed, and how many nodes you decide to build out, the entire processs could take 30-60 minutes.

## Chapters

Inside the chapters directory, there are smaller playbooks and templates to quickly perform the tasks for each book chapter that are used to build on top of each other to configure your environment.

These can be useful if you, like us, often break things through experimentation. They aren't a substitute for the additional knowledge in each chapter, but are great if you need to quickly get up and running after a failed 'experiment'.

To run a chapter playbook, be sure to reference the same inventory file:

```
$ ansible-playbook -i inventory chapters/chapterX.yaml
```

The autointaller automatically pulls the repository down on to your master server in the `/root` directory. You may find it helpful there if you need to quickly get back up and running.

## Contributing

If you are an Ansible user and want to add general improvements, or especially addtional hypervisor platforms, PRs are _most definitely_ welcome!
