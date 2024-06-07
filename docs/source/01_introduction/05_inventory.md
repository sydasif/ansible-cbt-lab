## [Ansible Inventory Setting](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#how-to-build-your-inventory)

Inventory serves as the foundation for managing hosts within our infrastructure using Ansible. It consolidates information about target hosts, including their IP addresses or Fully Qualified Domain Names (FQDNs). The simplest inventory is a single file with a list of hosts and groups. The default location for this file is `/etc/ansible/hosts`. You can specify a different inventory file at the command line using the `-i <path>` option or in configuration using `inventory`.

## Formats for Inventory Files

You can create your inventory file in various formats, the most common being `INI` and [`YAML`](https://yaml.org/). For this tutorial, see my [GNS3 Lab Setup](https://github.com/sydasif/gns3-lab).

A basic INI format might look like this as per my lab setup:

```ini
[router]
172.16.10.11

[core]
172.16.10.12

[switch]
172.16.10.13
172.16.10.14
```

The headings in brackets are group names. These group names are used to classify hosts, allowing you to decide which hosts to control at specific times and for particular purposes.

To build an inventory file using DNS names instead of IP addresses, you would replace the IP with the DNS names of your devices. Here's how you can modify the example:

```ini
[router]
r1

[core]
core-sw

[switch]
access1
access2
```

Ensure that the DNS names you use are resolvable from the system where you are running Ansible. This means that your DNS settings should be correctly configured to resolve these names to the appropriate IP addresses.

Here’s that same basic inventory file in YAML format:

```yaml
all:
  children:
    router:
      hosts:
        172.16.10.11:
    core:
      hosts:
        172.16.10.12:
    switch:
      hosts:
        172.16.10.13:
        172.16.10.14:
```

In this YAML inventory, `all` is the top-level group that contains all hosts and groups. The `hosts` key under `all` lists each host along with its properties, such as `ansible_host`. The `children` key under `all` contains subgroups like `router`, `core`, and `switch`, each with their respective hosts. This structure ensures the inventory is organized and easily manageable.

> By default, we can also reference two groups without defining them. The `all` group targets all our hosts in the inventory, and `ungrouped` contains any host that isn’t part of any user-defined group.

#### Defining Host Aliases

Another useful functionality is the option to define aliases for hosts in the inventory. For example, we can run Ansible against the host alias `core-sw` if we define it in the inventory as:

```ini
core-sw ansible_host=172.16.10.12
```

#### Inventory and Variables

An important aspect of Ansible’s setup is variable assignment and management. Ansible offers many different ways of setting variables, and defining them in the inventory is one of them.

##### Host Variables

For example, let’s define variables for each host in our inventory:

```ini
[router]
r1 ansible_host=172.16.10.11 ansible_user=bob

[core]
core-sw ansible_host=172.16.10.12 ansible_user=joe
```

Ansible-specific connection variables such as `ansible_user` or `ansible_host` are examples of host variables defined in the inventory.

##### Group Variables

Similarly, variables can also be set at the group level in the inventory, offering a convenient way to apply variables to hosts with common characteristics:

```ini
[router]
r1 ansible_host=172.16.10.11 ansible_user=bob ansible_password=bob123

[core]
core-sw ansible_host=172.16.10.12 ansible_user=joe ansible_password=joe123

[campus:children]
router
core

[campus:vars]
ansible_network_os=ios
ansible_connection=network_cli
```

Although setting variables in the inventory is possible, it’s usually not the preferred way. Instead, store separate host and group variable files to enable better organization and clarity for your Ansible projects. Note that host and group variable files must use the YAML syntax.

In the same directory where we keep our inventory file, we can create two folders named `group_vars` and `host_vars` containing our variable files. For example, we could have a file `group_vars/campus.yaml` that contains all the variables for the campus network:

```yaml
---
# group_vars/campus.yaml
ansible_user: admin
ansible_password: cisco
ansible_network_os: ios
ansible_connection: network_cli
```

Let’s view the generated inventory with the command:

```bash
zolo@u22s:~/ansible-networking-lab$ ansible-inventory -i inventory.yaml --graph
@all:
  |--@ungrouped:
  |--@campus:
  |  |--@router:
  |  |  |--r1
  |  |--@core:
  |  |  |--core-sw
  |  |--@switch:
  |  |  |--access1
  |  |  |--access2

##################################################################################

zolo@u22s:~/ansible-networking-lab$ ansible-inventory -i inventory.yaml --host r1
{
    "ansible_connection": "network_cli",
    "ansible_host": "172.16.10.11",
    "ansible_network_os": "ios",
    "ansible_password": "cisco",
    "ansible_user": "admin",
    "hostname": "r1"
}
```

The command fetches information from our hosts/inventory file and creates several groups according to our configuration/setup.

#### Key Points About Inventory

1. **Host Information:** Inventory files contain crucial information about target hosts, such as their IP addresses and connection variables.
2. **Default Location:** The default location for the inventory file is `/etc/ansible/hosts`, though you can specify a different location as needed.
3. **File Format:** Inventory can be written in either `INI` or `YAML` format, providing flexibility in structuring and organizing host information.
4. **Grouping Hosts:** Group names, enclosed in brackets, serve to classify hosts based on common attributes or roles they fulfill within the infrastructure.
5. **Special Groups:** The `campus` group is an example of a special group used for categorizing network devices, enabling targeted management of specific device types.
6. **Default Groups:** Ansible includes two default groups, namely `all` and `ungrouped`. The `all` group encompasses every host defined in the inventory, while the `ungrouped` group comprises hosts that do not belong to any other group aside from `all`.

By leveraging the inventory, Ansible users can effectively organize, manage, and automate tasks across their infrastructure, streamlining operations and enhancing efficiency.
