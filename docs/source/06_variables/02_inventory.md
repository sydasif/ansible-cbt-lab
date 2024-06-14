## Group Variables `group_vars`

Group variables are defined for groups of hosts, allowing shared configurations among multiple hosts. Group variables can be defined:

1. **In Inventory File**: Directly within the inventory file.
2. **In Separate `group_vars` Directory**: YAML files named after your groups in the `group_vars` directory.

### Example: Defining Group Variables in `group_vars` Directory

Directory structure:

```
inventory/
├── group_vars/
│   └── router.yml
└── hosts
```

Contents of `router.yml`:

```yaml
ntp: "1.1.1.1"
```

## Host Variables `host_vars`

Host variables are defined for individual hosts, specifying unique configurations for specific hosts. Host variables can be defined:

1. **In Inventory File**: Directly within the inventory file.
2. **In Separate `host_vars` Directory**: YAML files named after your hosts in the `host_vars` directory.

### Example: Defining Host Variables in `host_vars` Directory

Directory structure:

```
inventory/
├── host_vars/
│   ├── 172.16.10.11.yml
└── hosts
```

Contents of `172.16.10.11.yml`:

```yaml
ntp: "2.2.2.2"
hostname: Core
```

### Combining Group and Host Variables

Ansible combines variables from different sources using a well-defined order of precedence. Host variables have higher precedence than group variables.

#### Example Inventory Structure

```
inventory/
├── group_vars/
│   ├── all.yml
│   └── router.yml
├── host_vars/
│   └── 172.16.10.11.yml
└── hosts
```

Contents of `all.yml` (applies to all hosts):

```yaml
# Username for SSH authentication
ansible_user: admin
# Password for SSH authentication
ansible_password: cisco12
# Operating system of the Cisco devices
ansible_network_os: cisco.ios.ios
# Connection method for Ansible (network_cli)
ansible_connection: ansible.netcommon.network_cli

ntp: "3.3.3.3"
```

Contents of `router.yml` (applies to `router` group):

```yaml
ntp: "1.1.1.1"
```

Contents of `172.16.10.11.yml` (applies to `172.16.10.11` host):

```yaml
hostname: Core
ntp: "2.2.2.2"
```

Contents of hosts file:

```ini
# Define the Cisco routers group with its host
[all]
172.16.10.11  # Core switch with its IP address
172.16.10.14  # Router 1 with its IP address

[router]
172.16.10.14  # Router 1 with its IP address

# Define the Cisco core switches group with its host
[core]
172.16.10.11  # Core switch with its IP address

# Grouping all the Cisco network devices together
[all:children]
router
core
```

### Using Group and Host Variables in Playbooks

Once defined, group and host variables can be used in your playbooks like any other variable.

#### Example Playbook

```yaml
---
- name: "Load Variable"
  hosts: all
  gather_facts: false
  
  tasks:
    - name: Print Variable
      ansible.builtin.debug:
        msg: "{{ hostvars[ansible_host] }}"
```

#### Example Output

```
############### Omitted for brevity #################

[zolo@localhost ansible-cbt-lab]$ ansible-playbook load_vars.yaml 

PLAY [Load Variable] ************************************************

TASK [Print Variable] ***********************************************
ok: [172.16.10.11] => {
    "msg": {
        "hostname": "Core",
        "inventory_dir": "/home/zolo/ansible-cbt-lab",
        "inventory_file": "/home/zolo/ansible-cbt-lab/inventory.cfg",
        "inventory_hostname": "172.16.10.11",
        "inventory_hostname_short": "172.16.10.11",
        "ntp": "2.2.2.2",
        "playbook_dir": "/home/zolo/ansible-cbt-lab"
    }
}
ok: [172.16.10.14] => {
    "msg": {
        "inventory_dir": "/home/zolo/ansible-cbt-lab",
        "inventory_file": "/home/zolo/ansible-cbt-lab/inventory.cfg",
        "inventory_hostname": "172.16.10.14",
        "inventory_hostname_short": "172.16.10.14",
        "ntp": "1.1.1.1",
        "playbook_dir": "/home/zolo/ansible-cbt-lab"
    }
}

PLAY RECAP **********************************************************
172.16.10.11               : ok=1    changed=0    unreachable=0    failed=0
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0
```

### Analyzing the Variable Precedence

In the example playbook output, we see how Ansible processes variables for each host. The `ansible.builtin.debug` task prints out all variables available to each host. Let’s analyze the variables for two hosts, `172.16.10.11` and `172.16.10.14`.

#### Variables for `172.16.10.11`

- **Host `172.16.10.11`**:
  - **Group variables**:
    - `ansible_user: admin`
    - `ansible_password: cisco12`
    - `ansible_network_os: cisco.ios.ios`
    - `ansible_connection: ansible.netcommon.network_cli`
    - `ntp: 3.3.3.3` (from `all` group in the inventory file)
  - **Host variables**:
    - `hostname: Core`
    - `ntp: "2.2.2.2"`
  - **Resulting variables**:
    - The host variable `ntp: "2.2.2.2"` overwrites any group variable with the same name.
    - Final variables for `172.16.10.11` include `hostname: Core`, `ntp: "2.2.2.2"`, and all group variables defined above.

#### Variables for `172.16.10.14`

- **Host `172.16.10.14`**:
  - **Group variables**:
    - `ansible_user: admin`
    - `ansible_password: cisco12`
    - `ansible_network_os: cisco.ios.ios`
    - `ansible_connection: ansible.netcommon.network_cli`
    - `ntp: 3.3.3.3` (from `all` group in the inventory file)
    - `ntp: "1.1.1.1"` (from `router` group)
  - **Host variables**: None
  - **Resulting variables**:
    - The group variable `ntp: "1.1.1.1"` is used as there are no host-specific `ntp` variables to override it.
    - Final variables for `172.16.10.14` include all group variables defined above, with `ntp: "1.1.1.1"` coming from the `router` group.

The playbook output confirms that Ansible correctly combines and overrides variables based on their precedence. Host variables have the highest precedence, followed by group variables. Understanding this precedence ensures accurate and predictable configurations across your hosts.

## Understanding Ansible Magic and Facts Variables

In Ansible, magic variables provide valuable information about Ansible operations, hosts, and groups defined in your inventory. These variables are reserved and should not be overwritten. Additionally, the `environment` variable is reserved for system environment variables.

### Commonly Used Magic Variables

The most commonly used magic variables include:

- **`hostvars`**: Grants access to variables defined for any host in the play. It's also useful for accessing Ansible facts.
- **`groups`**: Provides information about host groups defined in your inventory.
- **`group_names`**: Lists the names of the groups to which a host belongs.
- **`inventory_hostname`**: Represents the name of the current inventory hostname.

### Understanding Ansible Facts Variables

Ansible facts are essential data about your remote systems, encompassing details such as operating systems, IP addresses, attached filesystems, and more. These facts are rich sources of variable data, providing insights into the state and configuration of managed hosts.

By default, Ansible makes facts available as top-level variables prefixed with `ansible_`, allowing for easy access within playbooks and tasks.

Now, let's revisit a playbook we used earlier to demonstrate how these concepts were applied:

```yaml
- name: "Print Host Variable"
  hosts: all
  gather_facts: false
  
  tasks:
    - name: "Print Host Variable"
      ansible.builtin.debug:
        msg: "{{ hostvars[ansible_host] }}"
```

In this playbook:

We use `hostvars[ansible_host]` to access the variables defined for the current host being processed in the playbook. The `hosts: all` directive ensures that the playbook runs on all hosts defined in the inventory.

Understanding and effectively utilizing these magic and facts variables in Ansible playbooks allow for more dynamic and flexible automation workflows. By harnessing the power of these variables, you can streamline configuration management tasks and ensure consistency across your infrastructure.
