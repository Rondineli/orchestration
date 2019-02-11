# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # May be required if vagrant not provisioning on MacOS
  # Uncomment it if necessary
  # config.ssh.insert_key = false


  config.vm.define "mir", primary: true do |mir|
    mir.vm.box = "envimation/ubuntu-xenial"
    #mir.vm.network "public_network"
    mir.vm.hostname = 'mir'
    mir.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 1000 ]
    end

  end
end

