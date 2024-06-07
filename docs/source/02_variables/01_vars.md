## Variables in Programming

Variables in programming are symbolic names that store data values which can be changed during the execution of a program. They are essential for managing and manipulating data.

### Key Characteristics of Variables

1. **Name (Identifier)**: A unique name given to the variable.
2. **Type**: The kind of value the variable can hold (e.g., integer, string, boolean).
3. **Value**: The actual data stored in the variable.
4. **Scope**: The part of the program where the variable is accessible.
5. **Lifetime**: The duration for which the variable exists in memory.

### Example in Python

```python
# Declaration and Initialization
x = 5             # integer
y = "Hello"       # string
is_valid = True   # boolean
```

## Variables in Ansible

Ansible is a powerful tool for automating configuration management. It uses variables to manage dynamic values, making playbooks flexible and reusable. Let’s explore how variables work in Ansible, focusing on group variables (`group_vars`) and host variables (`host_vars`).

### Defining Variables in Ansible

Ansible variables can be defined in several places:

1. **Inventory files**: Variables associated with hosts and groups in your inventory.
2. **Playbooks**: Variables defined at the playbook level.
3. **Roles**: Variables included in roles to make them reusable.
4. **Command Line**: Variables passed from the command line using the `-e` option.
5. **Extra Vars**: Variables defined in the `vars` section of a playbook.
6. **Facts**: Variables discovered about the system during the `gather_facts` step.

### Group Variables (`group_vars`)

Group variables are defined for groups of hosts, allowing shared configurations among multiple hosts. Group variables can be defined:

1. **In Inventory File**: Directly within the inventory file.
2. **In Separate `group_vars` Directory**: YAML files named after your groups in the `group_vars` directory.

#### Example: Defining Group Variables in `group_vars` Directory

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

### Host Variables (`host_vars`)

Host variables are defined for individual hosts, specifying unique configurations for specific hosts. Host variables can be defined:

1. **In Inventory File**: Directly within the inventory file.
2. **In Separate `host_vars` Directory**: YAML files named after your hosts in the `host_vars` directory.

#### Example: Defining Host Variables in `host_vars` Directory

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

### Example Inventory Structure

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
        msg: "{{ hostvars[inventory_hostname] }}"
```

Output:

```json
[zolo@localhost ansible-cbt-lab]$ ansible-playbook load_vars.yaml 

PLAY [Load Variable] ******************************************************************************************************

TASK [Print Variable] *****************************************************************************************************
ok: [172.16.10.11] => {
    "msg": {
        "ansible_check_mode": false,
        "ansible_config_file": "/home/zolo/ansible-cbt-lab/ansible.cfg",
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_diff_mode": false,
        "ansible_facts": {},
        "ansible_forks": 5,
        "ansible_inventory_sources": [
            "/home/zolo/ansible-cbt-lab/inventory.cfg"
        ],
        "ansible_network_os": "cisco.ios.ios",
        "ansible_password": "cisco12",
        "ansible_playbook_python": "/usr/bin/python",
        "ansible_run_tags": [
            "all"
        ],
        "ansible_skip_tags": [],
        "ansible_user": "admin",
        "ansible_verbosity": 0,
        "ansible_version": {
            "full": "2.15.12",
            "major": 2,
            "minor": 15,
            "revision": 12,
            "string": "2.15.12"
        },
        "group_names": [
            "core"
        ],
        "groups": {
            "all": [
                "172.16.10.11",
                "172.16.10.14"
            ],
            "core": [
                "172.16.10.11"
            ],
            "router": [
                "172.16.10.14"
            ],
            "ungrouped": []
        },
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
        "ansible_check_mode": false,
        "ansible_config_file": "/home/zolo/ansible-cbt-lab/ansible.cfg",
        "ansible_connection": "ansible.netcommon.network_cli",
        "ansible_diff_mode": false,
        "ansible_facts": {},
        "ansible_forks": 5,
        "ansible_inventory_sources": [
            "/home/zolo/ansible-cbt-lab/inventory.cfg"
        ],
        "ansible_network_os": "cisco.ios.ios",
        "ansible_password": "cisco12",
        "ansible_playbook_python": "/usr/bin/python",
        "ansible_run_tags": [
            "all"
        ],
        "ansible_skip_tags": [],
        "ansible_user": "admin",
        "ansible_verbosity": 0,
        "ansible_version": {
            "full": "2.15.12",
            "major": 2,
            "minor": 15,
            "revision": 12,
            "string": "2.15.12"
        },
        "group_names": [
            "router"
        ],
        "groups": {
            "all": [
                "172.16.10.11",
                "172.16.10.14"
            ],
            "core": [
                "172.16.10.11"
            ],
            "router": [
                "172.16.10.14"
            ],
            "ungrouped": []
        },
        "inventory_dir": "/home/zolo/ansible-cbt-lab",
        "inventory_file": "/home/zolo/ansible-c

bt-lab/inventory.cfg",
        "inventory_hostname": "172.16.10.14",
        "inventory_hostname_short": "172.16.10.14",
        "ntp": "1.1.1.1",
        "playbook_dir": "/home/zolo/ansible-cbt-lab"
    }
}

PLAY RECAP ****************************************************************************************************************
172.16.10.11               : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

### Analyzing the Playbook Output and Variable Precedence

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

### Conclusion

Variables in Ansible are crucial for managing dynamic configurations. By understanding how Ansible processes and applies variables from different sources, such as group and host variables, you can ensure that your playbooks are both flexible and maintainable. Mastering the precedence and combination of variables helps you achieve consistent and accurate configurations across all your managed hosts.
