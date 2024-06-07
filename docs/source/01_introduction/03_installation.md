## Installation of Ansible

Ansible can be installed on most Unix systems, with the only dependency being Python 2.7 or Python 3.5. Currently, the Windows operating system is not officially supported as a control machine. For detailed installation instructions, you can refer to the Ansible documentation [**website**](https://docs.ansible.com/ansible/2.9/installation_guide/index.html), which provides guidance for various platforms. In this guide, we will install Ansible on an Ubuntu machine using the following commands:

```console
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt install ansible
```

These steps ensure that your Ubuntu system is updated, necessary software properties are installed, the Ansible repository is added, and Ansible itself is installed, allowing you to start using Ansible for automation tasks.

Ansible is updated once every six months, so it's best to install it in a virtual environment.

```bash
virtualenv .venv
source .venv/bin/activate
python3 -m pip install ansible

# Use `deactivate` command to exit
```

To ensure that your Ansible installation is successful and operational, you can run the following commands in your terminal:

```bash
zolo@u22s:~$ ansible --version
ansible [core 2.16.7]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/zolo/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/zolo/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True
```

Executing this command will display information about the installed version of Ansible, confirming that it is correctly installed and ready for use.

Additionally, you can test Ansible's connectivity and functionality by running a simple ping command against the localhost:

```shell
zolo@u22s:~$ ansible localhost -m ping
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Running this command should result in a successful ping response from the localhost, indicating that Ansible can communicate with the target host and execute commands successfully.

### Privilege Escalation - Networking Device

As of Ansible 2.6, you can use the top-level Ansible parameter `become: yes` with `become_method: enable` to run a task, play, or playbook with escalated privileges on any network platform that supports privilege escalation.

### Establish a Manual Connection to a Managed Node

To run an ad-hoc command or Ansible playbook for the first time, it is mandatory to establish a manual SSH connection to the managed nodes to confirm your credentials. This involves connecting to a network device manually and retrieving its configuration. This manual connection also establishes the authenticity of the network device by adding its RSA key fingerprint to your list of known hosts.

Replace the sample user and device name with your real credentials. For example, for a router:

```bash
zolo@u22s:~$ ssh admin@172.16.10.11
(admin@172.16.10.11) Password: 

r1#sh ip int bri
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            172.16.10.11    YES NVRAM  up                    up      
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
FastEthernet1/0            unassigned      YES unset  administratively down down    
r1#exit
Connection to 172.16.10.11 closed.
```

### Run Your First Command

Instead of manually connecting and running a command on the network device, you can retrieve its configuration with a single, stripped-down Ansible command:

```bash
zolo@u22s:~$ ansible all -i 172.16.10.12, -c network_cli -u admin -k -m ios_facts -e ansible_network_os=ios
SSH password: 
172.16.10.12 | SUCCESS => {
    "ansible_facts": {
        "ansible_net_api": "cliconf",
        "ansible_net_gather_network_resources": [],
        "ansible_net_gather_subset": [
            "default"
        ],
        "ansible_net_hostname": "core-sw",
        "ansible_net_image": "tftp://255.255.255.255/unknown",
        "ansible_net_iostype": "IOS",
        "ansible_net_model": "3725",
        "ansible_net_operatingmode": "autonomous",
        "ansible_net_python_version": "3.10.12",
        "ansible_net_serialnum": "FTX0945W0MY",
        "ansible_net_system": "ios",
        "ansible_net_version": "12.4(15)T14",
        "ansible_network_resources": {}
    },
    "changed": false
}
```

In this example, Ansible targets all hosts defined in the inventory, specifying a custom inventory file with `-i`, connecting using `network_cli` as the connection type with `-c`, authenticating with the username `admin` using `-u`, prompting for a password with `-k`, executing the `ios_facts` module to gather facts about IOS devices, and specifying the network platform as `ios` using `-e`.

### Key Parameters

* `-i`: Specifies the list of managed nodes, separated by commas.
* `-c`: Defines the connection type.
* `-u`: Specifies the username for authentication.
* `-k`: Prompts for a password.
* `-m`: Specifies the module name.
* `-e`: Defines additional variables, such as the network platform.

These ad-hoc commands provide quick and efficient ways to perform specific tasks across your infrastructure using Ansible's versatile command-line interface.

Ansible is a robust and flexible tool for automating IT infrastructure management. Expanding into network automation, Ansible supports a wide range of network devices and protocols, ensuring comprehensive management capabilities. The installation process is straightforward, and Ansible's ability to handle privilege escalation and network-specific tasks further enhances its utility.
