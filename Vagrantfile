Vagrant.configure(2) do |config|
  config.vm.post_up_message = "Thanks for using the OpenShift In Action autoinstaller!"
  config.vm.box = "OpenShiftInAction/autoinstaller"
  config.vm.box_version = "0.2"
  config.ssh.username = 'vagrant'
  config.ssh.password = 'vagrant'
  config.ssh.insert_key = false

  config.vm.provider :virtualbox do |v|
      v.cpus = 2
      v.memory = 4096
  end

  config.vm.provider :libvirt do |libvirt|
    libvirt.cpus = 2
    libvirt.memory = 4096
  end

  config.vm.define "ansible" do |ansi|
    ansi.vm.network "private_network", ip: "192.168.120.99"
    ansi.vm.hostname = "ansible.192.168.120.99.nip.io"
    ansi.vm.provision "shell", path: "bin/ansible_setup.sh"
  end

  config.vm.define "ocp1" do |ocp1|
    ocp1.vm.network "private_network", ip: "192.168.120.100"
    ocp1.vm.hostname = "ocp1.192.168.120.100.nip.io"
  end

  config.vm.define "ocp2" do |ocp2|
    ocp2.vm.network "private_network", ip: "192.168.120.101"
    ocp2.vm.hostname = "ocp2.192.168.120.101.nip.io"
  end
end
