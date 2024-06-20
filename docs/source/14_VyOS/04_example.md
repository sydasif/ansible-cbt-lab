## Gathering Facts About VyOS and Cisco Devices

In previous sections, we learned how to automate configurations for devices from the same vendor. Now, we will enhance our skills to handle a multi-vendor environment by gathering facts from mixed devices. These facts provide useful information about the device's current state and configuration, which can be used in your playbooks for better management and automation.

Our topology consists of:

- Two Cisco devices
- One VyOS device

### Sample Playbook for Gathering Facts

Let's create a playbook that gathers facts from both VyOS and Cisco devices.

1. Create a new playbook file named `gather_facts.yaml`:

```yaml
---
- name: Gather Facts from VyOS and Cisco Devices
  hosts: all
  gather_facts: false
  connection: network_cli

  tasks:
    - name: Gather facts from VyOS devices
      when: "ansible_network_os == 'vyos.vyos.vyos'"
      vyos.vyos.vyos_facts:
        gather_subset: config

    - name: Gather facts from Cisco devices
      when: "ansible_network_os == 'cisco.ios.ios'"
      cisco.ios.ios_facts:
        gather_subset: config
```

2. Run the playbook using the following command:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook playbook/multi_vendor_facts.yaml

PLAY [Gather Facts from VyOS and Cisco Devices] ****************************************

TASK [Gather facts from VyOS devices] **************************************************
skipping: [172.16.10.16]
skipping: [172.16.10.17]
ok: [172.16.10.15]

TASK [Gather facts from Cisco devices] *************************************************
skipping: [172.16.10.15]
ok: [172.16.10.17]
ok: [172.16.10.16]

PLAY RECAP *****************************************************************************
172.16.10.15               : ok=1    changed=0    unreachable=0    failed=0    skipped=1
172.16.10.16               : ok=1    changed=0    unreachable=0    failed=0    skipped=1
172.16.10.17               : ok=1    changed=0    unreachable=0    failed=0    skipped=1 
```

### Understanding the Playbook

This playbook performs the following actions:

- Gathers facts from VyOS devices using the `vyos.vyos.vyos_facts` module.
- Gathers facts from Cisco devices using the `cisco.ios.ios_facts` module.
- Skips tasks for devices that do not match the specific conditions.

As you can see, the tasks are executed correctly, with each device type only processing the relevant tasks.

### Printing Gathered Facts

To print the gathered facts, we can modify the playbook to include additional tasks that display the information. Let's update the playbook to print out the gathered facts.

1. Update the `gather_facts.yaml` file:

```yaml
---
- name: Gather Facts from VyOS and Cisco Devices
  hosts: all
  gather_facts: false
  connection: network_cli

  tasks:
    - name: Gather facts from VyOS devices
      when: "ansible_network_os == 'vyos.vyos.vyos'"
      vyos.vyos.vyos_facts:
        gather_subset: config
      register: vyos_facts

    - name: Gather facts from Cisco devices
      when: "ansible_network_os == 'cisco.ios.ios'"
      cisco.ios.ios_facts:
        gather_subset: config
      register: cisco_facts

    - name: Print Cisco Facts
      ansible.builtin.debug:
        msg: "{{ cisco_facts.ansible_facts.ansible_net_config.split('\n') }}"
      when: "ansible_network_os == 'cisco.ios.ios'"

    - name: Print VyOS Facts
      ansible.builtin.debug:
        msg: "{{ vyos_facts.ansible_facts.ansible_net_config[0].split('\n') }}"
      when: "ansible_network_os == 'vyos.vyos.vyos'"
```

### Understanding the Updated Playbook

This updated playbook performs the following actions:

- Gathers facts from VyOS devices and registers the output in `vyos_facts`.
- Gathers facts from Cisco devices and registers the output in `cisco_facts`.
- Prints the gathered facts for Cisco devices.
- Prints the gathered facts for VyOS devices.

By adding the `ansible.builtin.debug` tasks, you can see the gathered configuration details directly in the playbook output.

## Configuring Interfaces on VyOS and Cisco Devices

In this final example, we configure interfaces on all devices using the appropriate Ansible module for each vendor. This demonstrates Ansible's ability to handle multi-vendor environments efficiently.

### Sample Playbook for Configuring Interfaces

Here is the playbook to configure interfaces on both VyOS and Cisco devices:

```yaml
---
- name: Configure Interfaces of VyOS and Cisco Devices
  hosts: all
  gather_facts: false
  connection: network_cli

  tasks:
    - name: Merge configuration with device configuration
      vyos.vyos.vyos_interfaces:
        config:
          - name: eth1
            description: LAN-Network
            mtu: 1500
            enabled: true
        state: merged
      register: vyos_facts
      when: "ansible_network_os == 'vyos.vyos.vyos'"

    - name: Merge configuration with device configuration
      cisco.ios.ios_interfaces:
        config:
          - name: "{{ interface }}"
            description: "{{ description }}"
            enabled: true
      register: cisco_facts
      when: ansible_network_os == 'cisco.ios.ios'

    - name: Print Cisco Facts
      ansible.builtin.debug:
        msg: "{{ cisco_facts.commands }}"
      when: ansible_network_os == 'cisco.ios.ios'

    - name: Print VyOS Facts
      ansible.builtin.debug:
        msg: "{{ vyos_facts.commands }}"
      when: ansible_network_os == 'vyos.vyos.vyos'
```

### Host Variables for Cisco Devices

Since Cisco devices may have different interface naming conventions (e.g., `FastEthernet` on routers and `Ethernet` on switches), we need to use `host_vars` files for each Cisco device.

#### Content of `host_vars/172.16.10.16` (Cisco Router)

```yaml
interface: FastEthernet0/1
description: link-to-sw1
```

#### Content of `host_vars/172.16.10.17` (Cisco Switch)

```yaml
interface: Ethernet0/1
description: link-to-pc
```

### Running the Playbook

Run the playbook using the following command:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook playbook/multi_vendor_config.yml

PLAY [Configure Interfaces of VyOS and Cisco Devices] **************************************

TASK [Merge configuration with device configuration] ***************************************
skipping: [172.16.10.17]
skipping: [172.16.10.16]
changed: [172.16.10.15]

TASK [Merge configuration with device configuration] ***************************************
skipping: [172.16.10.15]
changed: [172.16.10.17]
changed: [172.16.10.16]

TASK [Print Cisco Facts] *******************************************************************
skipping: [172.16.10.15]
ok: [172.16.10.16] => {
    "msg": [
        "interface FastEthernet0/1",
        "description link-to-sw1"
    ]
}
ok: [172.16.10.17] => {
    "msg": [
        "interface Ethernet0/1",
        "description link-to-pc"
    ]
}

TASK [Print VyOS Facts] ****************************************************************
skipping: [172.16.10.16]
skipping: [172.16.10.17]
ok: [172.16.10.15] => {
    "msg": [
        "set interfaces ethernet eth1 description 'LAN-Network'",
        "set interfaces ethernet eth1 mtu '1500'"
    ]
}

PLAY RECAP *****************************************************************************
172.16.10.15               : ok=2    changed=1    unreachable=0    failed=0    skipped=2
172.16.10.16               : ok=2    changed=1    unreachable=0    failed=0    skipped=2
172.16.10.17               : ok=2    changed=1    unreachable=0    failed=0    skipped=2 
```

### Explanation of Playbook Output

- **TASK [Merge configuration with device configuration]**: 
  - For VyOS (172.16.10.15), the interface `eth1` was configured with the description "LAN-Network" and an MTU of 1500. This task was skipped for the Cisco devices (172.16.10.16 and 172.16.10.17).
  - For Cisco devices, the interface configurations were applied based on the `host_vars` files. The playbook correctly identified and configured the `FastEthernet0/1` interface on the router and `Ethernet0/1` interface on the switch.
  
- **TASK [Print Cisco Facts]**: 
  - Displays the configuration commands that were sent to the Cisco devices:
    - For the router (172.16.10.16): `"interface FastEthernet0/1", "description link-to-sw1"`
    - For the switch (172.16.10.17): `"interface Ethernet0/1", "description link-to-pc"`

- **TASK [Print VyOS Facts]**: 
  - Displays the configuration commands that were sent to the VyOS device (172.16.10.15): 
    - `"set interfaces ethernet eth1 description 'LAN-Network'", "set interfaces ethernet eth1 mtu '1500'"`

- **PLAY RECAP**: 
  - Summary of the playbook execution:
    - All tasks were successfully executed for each device, with the appropriate configurations applied and verified.

This guide has demonstrated the power of Ansible in automating network configurations for both VyOS and Cisco devices in a multi-vendor environment. Ansible enhances network management by providing consistency, scalability, and efficiency. By using Ansible, network administrators can seamlessly manage diverse device types, ensuring robust and reliable network operations.
