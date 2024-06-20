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



This guide has demonstrated the power of Ansible in automating network configurations for both VyOS and Cisco devices in a multi-vendor environment. We covered:

- **Introduction to VyOS**: Understanding VyOS and its integration with Ansible.
- **Installation**: Steps to install VyOS in a virtual environment.
- **Configuration**: Using Ansible to set up banners on VyOS routers.
- **Multi-Vendor Management**: Creating playbooks to gather facts from both VyOS and Cisco devices.

Ansible enhances network management by providing consistency, scalability, and efficiency. By leveraging Ansible, network administrators can seamlessly manage diverse device types, ensuring robust and reliable network operations.
