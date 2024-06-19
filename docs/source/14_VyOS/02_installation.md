## Installation of VyOS

There are different ways to test VyOS, and in this section, we will focus on installing VyOS in GNS3. Before we begin, it's crucial to ensure that your environment meets the necessary prerequisites for running VyOS. This includes hardware requirements and downloading the appropriate VyOS image.

### Prerequisites

- **Processor**: x86-64 CPU
- **Memory**: Minimum 512 MB of RAM

VyOS images are available for download from the official VyOS website. Ensure you select the appropriate version for your hardware.

### Downloading VyOS

1. Visit the [VyOS Downloads Page](https://vyos.io/download).
2. Choose the rolling release version.
3. Download the ISO image to your local machine.

## Installing VyOS

The installation process in GNS3 is straightforward but can be lengthy. For a detailed step-by-step guide, refer to the [Running on GNS3](https://docs.vyos.io/en/equuleus/installation/virtual/gns3.html) blog.

## Post-Installation Configuration

After the initial installation, there are a few additional steps to configure your VyOS system:

### Initial Login

Log in using the default credentials:

- Username: `vyos`
- Password: `vyos`

### Network Configuration

Configure the network interfaces and other necessary network settings:

```bash
configure
set interfaces ethernet eth1 address '172.16.10.15/24'
commit
save
exit
```

### SSH Management

Enable SSH for remote management:

```bash
configure
set service ssh port '22'
commit
save
exit
```

### Verify Configuration

Ensure that the network interfaces and other settings are correctly configured by using commands like:

```bash
show interfaces
```

### SSH from Control Node

To access the VyOS system remotely, use SSH from your control node:

```bash
ssh vyos@172.16.10.15
```

Accept the keys to establish the connection.

With VyOS successfully installed and configured, you are now ready to integrate it with Ansible for automated network management. The next sections will guide you through setting up and using Ansible with VyOS.
