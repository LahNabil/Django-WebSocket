Vagrant.configure("2") do |config|
  # Configuration de la VM Ubuntu 18.04
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_version = "~> 20200304.0.0"

  config.vm.network "forwarded_port", guest: 8000, host: 8001

  config.vm.provision "shell", inline: <<-SHELL
    # Désactiver les mises à jour automatiques
    systemctl disable apt-daily.service
    systemctl disable apt-daily.timer

    # Mise à jour des paquets
    sudo apt-get update

    # Installer les outils nécessaires
    sudo apt-get install -y software-properties-common zip curl

    sudo apt-get install -y python3.8 python3.8-venv python3.8-dev

    # Ajouter le PPA pour Python 3.8
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update

    # Installer Python 3.8 et les outils de développement
    sudo apt-get install -y python3.8 python3.8-venv python3.8-dev

    # Installer pip pour Python 3.8
    curl -sS https://bootstrap.pypa.io/pip/3.8/get-pip.py | sudo python3.8

    sudo python3.8 -m pip install --upgrade pip

    # Créer les alias python/pip par défaut vers Python 3.8
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
    sudo update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 1

    # Ajouter les alias dans .bash_aliases (persistant)
    touch /home/vagrant/.bash_aliases
    if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
      echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
      echo "alias python='python3.8'" >> /home/vagrant/.bash_aliases
      echo "alias pip='pip3.8'" >> /home/vagrant/.bash_aliases
    fi
  SHELL
end
