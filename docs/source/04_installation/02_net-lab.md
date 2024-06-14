## Setting Up Network Devices in GNS3

In the previous chapter, we integrated Ubuntu and GNS3, creating a foundation for our network simulations. In this section, we will expand on that by adding network devices to our workspace and configuring them according to the lab topology provided.

### Lab Topology Overview

The lab topology for this section is depicted below:

```{figure} ../images/automation-lab.png
---
width: 75%
name: idle
---
Lab Topology
```

### Adding and Connecting Devices

1. **Add a Built-in Switch**:
   - Drag a built-in switch from the device list into your workspace.
   - Connect this switch to your Ubuntu machine.

2. **Add Routers and Switches**:
   - Add 2 routers and 2 switches to the workspace.
   - Connect the devices as shown in the lab topology image.

### Configuring IP Addresses

Assign the following IP addresses to the respective devices:

- `172.16.10.11`
- `172.16.10.12`
- `172.16.10.13`
- `172.16.10.14`

Ensure each device is configured with the correct IP address to match the topology requirements.

### Setting Up User Credentials

Configure usernames and passwords on all network devices. Use consistent credentials to streamline access and management.

### Enabling SSH

To manage the network devices remotely, we will set up SSH on each device. Follow these steps for each router and switch:

1. **Generate RSA Keys**:
   ```bash
   crypto key generate rsa
   ```

2. **Enable SSH**:
   ```bash
   ip ssh version 2
   ```

3. **Configure VTY Lines**:
   ```bash
   line vty 0 4
   transport input ssh
   login local
   ```

4. **Set User Credentials**:
   ```bash
   username <your-username> privilege 15 secret <your-password>
   ```

In this section, we successfully added network devices to our GNS3 workspace, connected them according to the specified lab topology, assigned IP addresses, set up user credentials, and enabled SSH access. This configuration forms the basis for more advanced network simulations and automation tasks.

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
