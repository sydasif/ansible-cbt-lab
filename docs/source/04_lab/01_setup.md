## Prerequisites for Setting Up a GNS3 Network Lab

Before setting up your virtual network lab with GNS3 on a Windows PC, ensure you have the following prerequisites:

1. **Windows PC Requirements**: Confirm your PC meets the necessary RAM, CPU, and disk space requirements for GNS3 and VMware. [Details here](https://docs.gns3.com/docs/getting-started/installation/windows/#minimum-requirements).
2. **GNS3 and GNS3 VM**: Install GNS3 and its VM in VMware. Download from the [GNS3 website](https://www.gns3.com/) and follow the [installation instructions](https://docs.gns3.com/docs/getting-started/installation/windows/#introduction). Helpful videos: [Video 1](https://www.youtube.com/watch?v=x9pGYyEqLYs), [Video 2](https://www.youtube.com/watch?v=lFEDmM_lsxI).
3. **Ubuntu 22 Server**: Install Ubuntu 22 Server in VMware, ensuring it has sufficient resources for optimal performance. Helpful [Video](https://youtu.be/Lj5qHBjSfMo?si=I5YZmZqnNqUKGdoP)

With these components in place, you're ready to proceed to setup the Network lab:

![network-lab](/images/automation-lab.png)

## Starting the Lab Environment

With the prerequisites in place, it's time to kick off the virtual network lab environment. This section outlines the steps to start GNS3, launch the GNS3 VM in VMware, and initiate the Ubuntu 22 Server.

Open GNS3 on your Windows PC. Navigate through any initial setup wizards or configurations if prompted. Once the GNS3 interface is accessible, you're ready to proceed.

Ensure that VMware is on, locate the GNS3 VM and check GNS3 VM to establish the connection between GNS3 GUI and the virtual machine.

![fig-1](/images/gns3-vm.PNG)

### Configuring Ubuntu Server

In this section, we'll configure the Ubuntu Server within your virtual lab environment. Follow these steps to set up a second network adapter for the Ubuntu Server in VMware:

#### Add Network Adapter

1. Open VMware and locate the Ubuntu Server virtual machine.
2. Ensure the VM is powered off.
3. Right-click on the VM and select "Settings."
4. In the VM Settings window, navigate to the "Network Adapter" tab and add a second adapter.
5. Change the network connection mode to `Vmnet2`.
6. Click OK to save the changes.

![fig-2](/images/network-adopter.PNG)

#### Start Ubuntu Server

1. Power on the Ubuntu Server virtual machine in VMware.
2. Allow the VM to boot up and log in using the credentials you configured during the Ubuntu setup.

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

4. Use the following command to check the network interfaces:

```bash
ip addr show
```

Example output:

```bash
zolo@u22s:~/gns3-lab$ ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:01:09:c2 brd ff:ff:ff:ff:ff:ff
    altname enp2s1
    inet 192.168.71.100/24 brd 192.168.71.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe01:9c2/64 scope link 
       valid_lft forever preferred_lft forever
3: ens37: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:01:09:cc brd ff:ff:ff:ff:ff:ff
    altname enp2s5
    inet 172.16.10.10/24 brd 172.16.10.255 scope global ens37
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe01:9cc/64 scope link 
       valid_lft forever preferred_lft forever
```

Ensure that the network interfaces are associated with IP addresses and are in the "UP" state.

By adding a network adapter, you enable communication between the Ubuntu Server and your GNS3 setup, facilitating connectivity with other devices in the virtual lab. With the network settings in place, proceed to Section 4, where we'll guide you through adding a cloud node to GNS3 and selecting your network.

### Adding Cloud Node to GNS3

In this section, we'll expand your virtual network lab in GNS3 by adding a cloud node. The cloud node serves as a bridge between the GNS3 environment and Ubuntu, enabling connectivity to network devices. Follow these steps to seamlessly integrate the cloud node:

#### Access the GNS3 Workspace

1. Open GNS3 and navigate to the workspace where you plan to build your network topology.

#### Add Cloud Node

1. From the GNS3 toolbar, locate and drag the `Cloud` node into the workspace.
2. Connect the cloud node to your existing devices using appropriate link types (Ethernet, WiFi).

#### Configure Cloud Node

1. Right-click on the cloud node and select "Configure."
2. In the "Node Configurations" window, select the `Ethernet Interfaces` tab.
3. Choose the network adapter that corresponds to your Ubuntu server network.

![fig-3](/images/vmnet.PNG)

#### Apply Changes

1. Click "OK" to apply the changes to the cloud node.
2. Save the GNS3 project to preserve the current configuration.

By adding a cloud node and configuring it, you establish a link between GNS3 network devices. This integration sets the stage for comprehensive testing and interaction within your virtual network lab.

### Installing VSCode and SSH Extension

In this section, we'll enhance your virtual network lab environment by integrating Visual Studio Code (VSCode) and installing the SSH extension. VSCode provides a versatile platform for code development and, with the SSH extension, allows seamless interaction with your Ubuntu Server. Follow these steps to set up this essential coding and remote connection environment:

#### Download and Install VSCode

1. Visit the official VSCode website at [VSCode Downloads](https://code.visualstudio.com/download) to download the installer.
2. Run the installer and follow the on-screen instructions to complete the installation.

#### Open VSCode

Once VSCode is installed, open the application on your Windows PC.

#### Install SSH Extension

1. In VSCode, go to the Extensions by clicking on the Extensions icon in the Activity Bar on the side of the window or using the shortcut `Ctrl+Shift+X`.
2. Search for "Remote - SSH" in the Extensions view search box.
3. Click "Install" next to the "Remote - SSH" extension.

![fig-4](/images/ssh-ext.PNG)

#### Configure SSH Connection

In the bottom-left corner of the VSCode window, click on the blue square icon (Remote Explorer).
Click on the "Connect to Host" to add a new SSH target.
Enter the SSH connection details for your Ubuntu Server (username, IP address).

![fig-5](/images/re-con.png)

With VSCode and the SSH extension installed, you now have a powerful coding environment directly linked to your Ubuntu Server. This integration streamlines the process of writing and testing Python scripts for your network lab.

### Connecting VSCode to Ubuntu Server

In this section, we'll establish a direct connection between Visual Studio Code (VSCode) and your Ubuntu Server within the GNS3 virtual network lab. This connection allows you to seamlessly write, test, and execute Python scripts on the Ubuntu Server. Follow these steps to ensure a smooth integration:

#### Access Remote Explorer

1. In the bottom-left corner of the VSCode window, click on the square icon (Remote Explorer).
2. You should see the SSH target you added in the previous section.

#### Connect to Ubuntu Server

1. Click on the SSH target representing your Ubuntu Server.
2. VSCode will establish an SSH connection to the Ubuntu Server, and you'll be prompted for the password. Enter the password for your Ubuntu Server.

#### Verify Connection

1. Once connected, you should see the Ubuntu Server's file system in the VSCode Explorer.
2. Open a terminal in VSCode and run basic commands to verify the SSH connection.

#### Create and Test Python Scripts

1. In VSCode, create a new Python file.
2. Write a simple Python script (e.g., print("Hello, GNS3!")) and save the file.
3. Use the VSCode terminal to navigate to the directory containing your Python script and run it.

With this connection established, you can seamlessly develop, debug, and test Python scripts directly on your Ubuntu Server from within the VSCode environment. This integration empowers you to leverage the full potential of your virtual network lab for scripting and automation tasks.

## Finalizing the Lab Setup

Congratulations on successfully setting up your virtual network lab with GNS3, Ubuntu Server, and Visual Studio Code (VSCode). In this section, we'll recap the key components of your lab setup and highlight the benefits of the interconnected environment you've created.

### Benefits of the Lab Setup

By creating this integrated virtual network lab, you've gained several advantages:

- **Hands-on Learning:** Actively engage with networking concepts through practical exercises and experiments.
- **Scripting and Automation:** Leverage Python scripts to automate network configurations and tasks.
- **Real-world Simulation:** Mimic real-world network scenarios and challenges within the GNS3 environment.

### Next Steps

As you continue your network exploration, consider the following next steps:

- **Expand Your Topology:** Add more devices to your GNS3 topology to simulate complex network architectures.
- **Experiment with Python:** Explore advanced Python scripts to handle various networking tasks.
- **Document Your Lab:** Maintain comprehensive documentation of your lab setup, including configurations and scripts, for future reference.

## Conclusion

In conclusion, you've successfully created a virtual network lab that serves as an invaluable resource for testing Python code on networking devices. This hands-on environment, comprising GNS3, Ubuntu Server, and VSCode, empowers you to refine your networking and coding skills in a dynamic and controlled setting.

[Cisco IOS Lab Images](https://drive.google.com/drive/folders/1m85cy4y8At0yrKL-6_2bNDwtf-u5bTDU?usp=sharing)
