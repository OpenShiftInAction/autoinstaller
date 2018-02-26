#! /usr/bin/env bash
# executed on the ansible node to deploy OpenShift

sudo yum -y install ansible
ansible -i /vagrant/ansible/inventory-other /vagrant/ansible/site-vagrant.yaml
