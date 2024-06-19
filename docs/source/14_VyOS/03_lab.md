## Ansible Integration with VyOS

VyOS is supported in Ansible through a dedicated collection. This collection provides modules to manage and configure VyOS devices.

- To install the VyOS collection, run the following command:

```bash
ansible-galaxy collection install vyos.vyos
```

- Detailed documentation on the available modules can be found on the [Ansible VyOS collection page](https://docs.ansible.com/ansible/latest/collections/vyos/vyos/index.html#modules).

### Setting Up the Lab

To interact with VyOS from our Ansible control node and automate configuration tasks, we will set up a lab environment. The lab topology is illustrated below:

```{figure} ../images/vyos-lab.png
---
width: 75%
name: idle
---
VyOS Lab Topology
```

In this lab, we have the following devices:

- One VyOS router
- One Cisco router
- One switch

### Configuring Ansible for Multi-Vendor Environment

Initially, our `group_vars/all.yaml` file is set up for Cisco devices only:

```yaml
# Group_vars/all.yaml - Variables for all hosts
ansible_user: admin
ansible_password: cisco12
ansible_network_os: cisco.ios.ios
ansible_connection: ansible.netcommon.network_cli
```

To support both Cisco and VyOS devices, we need to create separate configuration files in the `group_vars` directory.

1. Rename `all.yaml` to `cisco.yaml` for Cisco devices and create `vyos.yaml` for VyOS devices.

#### `group_vars/cisco.yaml`

```yaml
# Group_vars/cisco.yaml - Variables for Cisco devices
ansible_user: admin
ansible_password: cisco12
ansible_network_os: cisco.ios.ios
```

#### `group_vars/vyos.yaml`

```yaml
# Group_vars/vyos.yaml - Variables for VyOS devices
ansible_user: vyos
ansible_password: vyos
ansible_network_os: vyos.vyos.vyos
```

2. Update the `ansible.cfg` file to define the inventory for the lab:

```ini
[all]
172.16.10.15  
172.16.10.16  
172.16.10.17  

[cisco]
172.16.10.16  
172.16.10.17  

[vyos]
172.16.10.15  

[all:children]
cisco
vyos
```

With this setup, Ansible is now ready to work with a multi-vendor environment, allowing you to automate configuration tasks across both Cisco and VyOS devices.

In the next sections, we will explore specific Ansible playbooks and tasks to configure and manage VyOS devices effectively.
