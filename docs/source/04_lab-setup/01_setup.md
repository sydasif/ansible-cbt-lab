## Prerequisites

Before starting, make sure you have:

1. **Windows PC Requirements**: Ensure your PC has enough RAM, CPU, and disk space.
   * [Details are here](https://docs.gns3.com/docs/getting-started/installation/windows/#minimum-requirements).
2. **GNS3 and GNS3 VM**: Download and install GNS3 and its VM from the [**website**](https://www.gns3.com/).
   * Follow the [installation instructions](https://docs.gns3.com/docs/getting-started/installation/windows/#introduction).
   * Helpful videos: [Video 1](https://www.youtube.com/watch?v=x9pGYyEqLYs), [Video 2](https://www.youtube.com/watch?v=lFEDmM_lsxI).
3. **Ubuntu 22 Server**: Install Ubuntu 22 Server in VMware.
   * Helpful [Video](https://youtu.be/Lj5qHBjSfMo?si=I5YZmZqnNqUKGdoP)

### Starting the Lab Environment

1. Open GNS3 on your Windows PC and complete any setup wizards.
2. Ensure VMware is running, locate the GNS3 VM, verify the connection between GNS3 GUI and the virtual machine.

```{figure} ../images/gns3-vm.png
---
width: 50%
name: idle
---
GNS3 VM
```

### Configuring Ubuntu Server

Follow these steps to set up a second network adapter for Ubuntu Server in VMware:

#### Add Network Adapter

1. Open VMware and locate the Ubuntu Server virtual machine.
2. Ensure the VM is powered off.
3. Right-click the VM and select "Settings."
4. Navigate to the "Network Adapter" tab and add a second adapter.
5. Change the network connection mode to `Vmnet2`.
6. Click OK to save the changes.

```{figure} ../images/network-adopter.png
---
width: 50%
name: idle
---
Network Adopter
```

#### Start Ubuntu Server

1. Power on the Ubuntu Server virtual machine in VMware.
2. Log in using your credentials.

#### Verify Network Configuration

1. Open a terminal in Ubuntu.
2. Configure static IP addresses on both network adapters by editing the netplan configuration:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Example netplan configuration:

```yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens33:  # NAT Adapter
      addresses:
        - 192.168.71.100/24
      gateway4: 192.168.71.2
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
    ens37:  # Vmnet2 Adapter
      addresses:
        - 172.16.10.10/24
  version: 2
```

3. Apply the netplan configuration:

```bash
sudo netplan apply
```

4. Check the network interfaces:

```bash
ip addr show
```

Make sure the network interfaces have IP addresses and are in the "UP" state.

### Adding Cloud Node to GNS3

1. Open GNS3 and go to your workspace.
2. Drag the Cloud node into the workspace.
3. Connect the cloud node to your devices.
4. Right-click the cloud node and select "Configure."
5. Choose the network adapter that corresponds to your Ubuntu server network.
6. Click "OK" and save the project.

```{figure} ../images/vmnet.png
---
width: 50%
name: idle
---
Cloud Node Setting
```

### Installing VSCode and SSH Extension

1. Download and install VSCode from VSCode Downloads.
2. Open VSCode.
3. Go to Extensions (Ctrl+Shift+X) and search for "Remote - SSH."
4. Install the "Remote - SSH" extension.

```{figure} ../images/ssh-ext.png
---
width: 75%
name: idle
---
SSH Extension
```

### Configure SSH Connection

1. Click on the blue square icon (Remote Explorer) in the bottom-left corner of VSCode.
2. Click "Connect to Host" and add your SSH details (username, IP address).

### Connecting VSCode to Ubuntu Server

1. Click on the SSH target representing your Ubuntu Server.
2. Enter the password when prompted.
3. Verify the connection by running basic commands in the VSCode terminal.

#### Create and Test Python Scripts

1. Create a new Python file in VSCode.
2. Write a simple script (e.g., print("Hello, GNS3!")).
3. Run the script using the VSCode terminal.

## Setting Up Network Devices in GNS3

In this section, we'll add network devices to our workspace and configure them according to the provided lab topology.

### Lab Topology Overview

Here's the lab topology for this section:

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

Make sure each device has the correct IP address to match the topology.

### Setting Up User Credentials

Set up usernames and passwords on all network devices. Use consistent credentials for easier access and management.

### Enabling SSH

To manage the network devices remotely, we'll set up SSH on each router and switch. Follow these steps:

1. **Configure Domain and Generate RSA Keys**:
   ```bash
   ip domain-name lab.com
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

We've now added network devices to our GNS3 workspace, connected them according to the lab topology, assigned IP addresses, set up user credentials, and enabled SSH access. This sets up the foundation for more advanced network simulations and automation tasks.

### Establishing a Manual Connection

Before running Ansible commands or playbooks, manually connect to the managed nodes via SSH to confirm your credentials and add the device’s RSA key fingerprint to your known hosts. For example, to connect to a router:

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

Ansible is a powerful tool for automating IT infrastructure management, including network automation with broad device and protocol support. Its installation process is straightforward, and its features for privilege escalation and network-specific tasks further enhance its utility.

Congratulations! You've successfully set up your virtual network lab with GNS3, Ubuntu Server, and VSCode. This lab will help you test Python code and improve your networking skills.
