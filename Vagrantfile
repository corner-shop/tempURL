# -*- mode: ruby -*-
# vi: set ft=ruby :
#
vbox_version = `VBoxManage --version`

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

   if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
   end

  config.vm.box_check_update = true
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |vb|
     vb.memory = "256"

     vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
     vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
     vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000 ]
     vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
     vb.customize ["modifyvm", :id, "--paravirtprovider", "kvm"] if vbox_version.to_f >= 5.0
     vb.customize ["storagectl", :id, "--name", "SATAController", "--hostiocache", "on"]
     vb.customize ["modifyvm", :id, "--ioapic", "on"]
     vb.customize ["modifyvm", :id, "--cpus", `#{RbConfig::CONFIG['host_os'] =~ /darwin/ ? 'sysctl -n hw.ncpu' : 'nproc'}`.chomp]

     vb.linked_clone = true if Vagrant::VERSION =~ /^1.8/
  end

  config.vm.provision "shell", inline: <<-SHELL
    if [ ! -e /etc/bootstrapped ]; then
      sudo apt-get update
      sudo apt-get install -y python-pip curl build-essential python-dev libsqlite3-dev
      which docker || (curl -fsSL https://get.docker.com/ | sh)
      sudo pip install docker-compose
      sudo touch /etc/bootstrapped
    fi

    cd /vagrant
    sudo pip install -r dev-requirements.txt
    sudo python tests.py
  SHELL
end
