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

### Privilege Escalation

From Ansible 2.6 onward, you can use `become: yes` and `become_method: enable` to run tasks with escalated privileges on network devices that support this feature.

### Establishing a Manual Connection

Before running Ansible commands or playbooks, establish a manual SSH connection to the managed nodes to confirm your credentials and add the device’s RSA key fingerprint to your list of known hosts. For example, to connect to a router:

```bash
ssh admin@172.16.10.11
```

After entering your password, you can run a command like `show ip int bri` to check the device's interfaces:

```plaintext
r1#sh ip int bri
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            172.16.10.11    YES NVRAM  up                    up      
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
FastEthernet1/0            unassigned      YES unset  administratively down down    
r1#exit
```

### Running Your First Ansible Command

Instead of manually connecting to the device, you can retrieve its configuration with an Ansible command:

```bash
ansible all -i 172.16.10.12, -c network_cli -u admin -k -m ios_facts -e ansible_network_os=ios
```

This command:

- **Targets all hosts** defined in the inventory (`-i 172.16.10.12,`).
- **Uses `network_cli`** as the connection type (`-c network_cli`).
- **Authenticates with the username `admin`** (`-u admin`).
- **Prompts for a password** (`-k`).
- **Executes the `ios_facts` module** to gather information about IOS devices (`-m ios_facts`).
- **Specifies the network platform** as `ios` (`-e ansible_network_os=ios`).

The output will show facts about the device, confirming that Ansible can successfully gather information from it.

#### Key Parameters

- `-i`: Specifies the list of managed nodes.
- `-c`: Defines the connection type.
- `-u`: Specifies the username for authentication.
- `-k`: Prompts for a password.
- `-m`: Specifies the module name.
- `-e`: Defines additional variables, such as the network platform.

Ansible provides a powerful, flexible tool for automating IT infrastructure management, extending into network automation with broad device and protocol support. The installation process is straightforward, and Ansible's features for privilege escalation and network-specific tasks further enhance its utility.
