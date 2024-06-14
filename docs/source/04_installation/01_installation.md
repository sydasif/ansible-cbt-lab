## Installing Ansible

Ansible can be installed on most Unix systems, with the only requirement being Python 2.7 or Python 3.5. Unfortunately, Windows is not officially supported as a control machine. For detailed installation instructions, refer to the Ansible documentation [**website**](https://docs.ansible.com/ansible/2.9/installation_guide/index.html). Below, we outline the steps to install Ansible on an Ubuntu machine:

1. **Update your system:**

```bash
sudo apt update
```

2. **Install necessary software properties:**

```bash
sudo apt install software-properties-common
```

3. **Add the Ansible repository:**

```bash
sudo apt-add-repository ppa:ansible/ansible
```

4. **Install Ansible:**

```bash
sudo apt install ansible
```

These commands will update your system, install required software properties, add the Ansible repository, and then install Ansible.

### Using a Virtual Environment

Ansible is updated every six months, so it's recommended to install it in a virtual environment:

1. **Create a virtual environment:**

```bash
virtualenv .venv
```

2. **Activate the virtual environment:**

```bash
source .venv/bin/activate
```

3. **Install Ansible:**

```bash
python3 -m pip install ansible
```

4. **To exit the virtual environment:**

```bash
deactivate
```

### Verifying Ansible Installation

To ensure that Ansible is installed correctly, you can check its version:

```bash
ansible --version
```

You should see output similar to this:

```plaintext
ansible [core 2.16.7]
config file = /etc/ansible/ansible.cfg
configured module search path = ['/home/user/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
ansible python module location = /usr/lib/python3/dist-packages/ansible
ansible collection location = /home/user/.ansible/collections:/usr/share/ansible/collections
executable location = /usr/bin/ansible
python version = 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] (/usr/bin/python3)
jinja version = 3.0.3
libyaml = True
```

To test Ansible’s connectivity, run a simple ping command:

```bash
ansible localhost -m ping
```

The output should be:

```plaintext
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
