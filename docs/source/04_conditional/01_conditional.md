## Conditional in Ansible

In Ansible, conditionals allow you to control whether a task or set of tasks should be executed based on the value of a variable, fact, or the outcome of a previous task. Here are some common ways to use conditionals in Ansible:

### Conditionals based on ansible_facts:

Often you want to execute or skip a task based on facts. Facts are attributes of individual hosts, including IP address, operating system, the status of a filesystem, and many more. With conditionals based on facts:

- You can install a certain package only when the operating system is a particular version.
- You can skip configuring a firewall on hosts with internal IP addresses.
- You can perform cleanup tasks only when a filesystem is getting full.

Here is a sample conditional based on a fact:

```yaml
- name: Configure network devices
  hosts: core
  gather_facts: no

  tasks:
    - name: Gather facts for Cisco IOS
      cisco.ios.ios_facts:

    - name: Configure interface on Cisco IOS
      cisco.ios.ios_config:
        lines:
          - interface loopback 1
          - description Configured by Ansible
          - ip address 192.168.1.1 255.255.255.0
      when: ansible_network_os == 'ios'
```

### Conditions based on registered variables:

Often in a playbook, you want to execute or skip a task based on the outcome of an earlier task. For example, you might want to configure a service after it is upgraded by an earlier task. To create a conditional based on a registered variable:

- Register the outcome of the earlier task as a variable.
- Create a conditional test based on the registered variable.

You create the name of the registered variable using the `register` keyword. A registered variable always contains the status of the task that created it as well as any output that the task generated. You can access the string contents of the registered variable using `variable.stdout`. For example:

```yaml
- name: Check BGP status and configure if not running
  hosts: routers
  gather_facts: no

  tasks:
    - name: Check BGP status
      cisco.ios.ios_command:
        commands: show ip bgp summary
      register: bgp_status

    - name: Configure BGP if not running
      cisco.ios.ios_config:
        lines:
          - router bgp 65000
          - neighbor 192.168.3.2 remote-as 65001
      when: '"Idle" in bgp_status.stdout'
```

### Using conditionals in loops:

If you combine a when statement with a loop, Ansible processes the condition separately for each item. This is by design, so you can execute the task on some items in the loop and skip it on other items. For example:

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

- Conditionals based on variables

In network automation, using conditionals based on variables allows for dynamic and context-aware configuration, ensuring tasks are executed only when specific conditions are met. This enhances the flexibility and efficiency of automation scripts. For instance, you can configure network devices differently based on their roles or operating systems.

### Example

```yaml
- name: Configure spine switches
  hosts: spine_switches
  vars:
    device_role: spine
  tasks:
    - name: Configure spine switch
      ios_config:
        lines:
          - interface Ethernet1
          - description Spine Switch
      when: device_role == 'spine'

- name: Configure leaf switches
  hosts: leaf_switches
  vars:
    device_role: leaf
  tasks:
    - name: Configure leaf switch
      ios_config:
        lines:
          - interface Ethernet1
          - description Leaf Switch
      when: device_role == 'leaf'
```

In this example, the interface configuration is applied based on whether the device is a spine or leaf switch. In Ansible, variables such as the device role can be defined in various places, including inventory files, group variables, host variables, or directly within the playbook itself.
