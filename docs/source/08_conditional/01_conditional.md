## Conditional in Ansible

In Ansible, conditionals allow you to control whether a task or set of tasks should be executed based on the value of a variable, fact, or the outcome of a previous task. Here are some common ways to use conditionals in Ansible:

### Conditionals based on `ansible_facts`

Often, you want to execute or skip a task based on facts. Facts are attributes of individual hosts, including IP address, operating system, the status of a filesystem, and many more. With conditionals based on facts:

- You can install a certain package only when the operating system is a particular version.
- You can skip configuring a firewall on hosts with internal IP addresses.
- You can perform cleanup tasks only when a filesystem is getting full.

#### Example - Facts

Here is a sample conditional based on a fact:

```yaml
- name: Configure network devices
  hosts: core
  gather_facts: true

  tasks:
    - name: Configure interface on Cisco IOS
      cisco.ios.ios_config:
        lines:
          - interface FastEthernet 0/1
          - description Configured by Ansible
          - ip address 3.3.3.3 255.255.255.0
      when: ansible_net_hostname == 'CORE'
```

#### Output

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook condition_var.yaml 

PLAY [Configure network devices] *******************************************************

TASK [Gathering Facts] *****************************************************************
ok: [172.16.10.11]

TASK [Configure interface on Cisco IOS] ************************************************
changed: [172.16.10.11]

PLAY RECAP *****************************************************************************
172.16.10.11               : ok=2    changed=1    unreachable=0    failed=0    skipped=0
```

### Conditions based on registered variables

Often in a playbook, you want to execute or skip a task based on the outcome of an earlier task. For example, you might want to configure a service after it is upgraded by an earlier task. To create a conditional based on a registered variable:

- Register the outcome of the earlier task as a variable.
- Create a conditional test based on the registered variable.

You create the name of the registered variable using the `register` keyword. A registered variable always contains the status of the task that created it as well as any output that the task generated. You can access the string contents of the registered variable using `variable.stdout`.

#### Example - Register

Here is a sample conditional based on a register:

```yaml
- name: Check BGP status and configure if not running
  hosts: router
  gather_facts: false

  tasks:
    - name: Check BGP status
      cisco.ios.ios_command:
        commands: show ip bgp summary
      register: bgp_status

    - name: Configure BGP if not running
      cisco.ios.ios_config:
        lines:
          - router bgp 65000
          - neighbor 9.9.9.9 remote-as 65001
      when: '"% BGP not active" in bgp_status.stdout'
```

#### Output

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook condition_var.yaml

PLAY [Check BGP status and configure if not running] ***********************************

TASK [Check BGP status] ****************************************************************
ok: [172.16.10.14]

TASK [Configure BGP if not running] ****************************************************
changed: [172.16.10.14]

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=2    changed=1    unreachable=0    failed=0    skipped=0
```

### Using conditionals in loops

If you combine a `when` statement with a loop, Ansible processes the condition separately for each item. This is by design, so you can execute the task on some items in the loop and skip it on other items.

#### Example - Loop

Here is a sample conditional based on a loop:

```yaml
- name: Ensure specific VLANs are present on switches
  hosts: switches
  gather_facts: no

  tasks:
    - name: Configure VLANs
      cisco.ios.ios_config:
        lines:
          - vlan {{ item.id }}
          - name {{ item.name }}
      loop:
        - { id: 10, name: 'Engineering' }
        - { id: 20, name: 'HR' }
        - { id: 30, name: 'Sales' }
      when: item.id != 20
```

#### Output

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook condition_var.yaml

PLAY [Ensure specific VLANs are present on switches] ***********************************

TASK [Configure VLANs] *****************************************************************
changed: [172.16.10.12] => (item={'id': 10, 'name': 'Engineering'})
skipping: [172.16.10.12] => (item={'id': 20, 'name': 'HR'}) 
changed: [172.16.10.13] => (item={'id': 10, 'name': 'Engineering'})
skipping: [172.16.10.13] => (item={'id': 20, 'name': 'HR'}) 
changed: [172.16.10.12] => (item={'id': 30, 'name': 'Sales'})
changed: [172.16.10.13] => (item={'id': 30, 'name': 'Sales'})

PLAY RECAP *****************************************************************************
172.16.10.12               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
172.16.10.13               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

### Conditionals based on variables

In network automation, using conditionals based on variables allows for dynamic and context-aware configuration, ensuring tasks are executed only when specific conditions are met. This enhances the flexibility and efficiency of automation scripts. For instance, you can configure network devices differently based on their roles or operating systems.

#### Example - Variable

Here is a sample conditional based on a variable:

```yaml
- name: Configure network devices based on role
  hosts: switches
  vars:
    device_role: spine
  tasks:
    - name: Configure spine switch
      ios_config:
        lines:
          - interface Ethernet1
          - description Spine Switch
      when: device_role == 'spine'

    - name: Configure leaf switch
      ios_config:
        lines:
          - interface Ethernet1
          - description Leaf Switch
      when: device_role == 'leaf'
```

In this example, the interface configuration is applied based on whether the device is a spine or leaf switch. In Ansible, variables such as the device role can be defined in various places, including inventory files, group variables, host variables, or directly within the playbook itself. This example shows a hardcoded variable in the playbook, but typically, these variables would be defined per host in an inventory or variable file.

#### Example - Inventory

**Inventory File (`inventory.ini`)**

```ini
[switches]
spine1 ansible_host=192.168.1.1 device_role=spine
spine2 ansible_host=192.168.1.2 device_role=spine
leaf1 ansible_host=192.168.2.1 device_role=leaf
leaf2 ansible_host=192.168.2.2 device_role=leaf
```

By defining the device roles in the inventory file, you ensure that the playbook applies the correct configuration to each device dynamically based on its role.
