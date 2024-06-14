## Understanding Loops in Ansible

Loops in Ansible are used to repeat tasks multiple times. Ansible provides several keywords for looping, including `loop`, `with_<lookup>`, and `until`. These enable you to execute a task iteratively with different parameters, simplifying repetitive configurations.

### Example: Configuring NTP Servers on a Router

Let's consider an Ansible playbook that configures NTP (Network Time Protocol) on a router:

```yaml
---
- name: "Configure NTP"
  hosts: router
  gather_facts: false

  tasks:
    - name: "Configure NTP on Router"
      vars:
        ntp_server:
          - "1.1.1.1"
          - "2.2.2.2"
          - "3.3.3.3"
          - "4.4.4.4"
      cisco.ios.ios_ntp_global:
        config:
          peers:
            - peer: "{{ item }}"
              version: 2
      loop: "{{ ntp_server }}"
```

### Playbook Explanation

- **Play Definition**: The play is named "Configure NTP" and targets the `router` host group. The directive `gather_facts: false` disables the default fact-gathering behavior.

- **Task Definition**: A single task is defined within the play. This task uses the `vars` keyword to define a list of NTP servers.

- **Task Details**:
  - **Task Name**: "Configure NTP on Router"
  - **Variable Definition**: The `ntp_server` variable is defined as a list of four IP addresses.
  - **Module**: The `cisco.ios.ios_ntp_global` module configures NTP settings on Cisco IOS devices.
  - **Configuration**: The `config` parameter specifies the NTP peers to be configured, using a loop to iterate over the `ntp_server` list.
  - **Loop**: The `loop` keyword iterates over the `ntp_server` list, configuring each NTP server in turn.

### Understanding `item` in the Loop

In Ansible loops, `item` represents the current element in the list being processed. As the loop iterates over the `ntp_server` list, `item` holds the value of each NTP server IP address one by one.

For example:
- During the first iteration, `item` is `1.1.1.1`.
- During the second iteration, `item` is `2.2.2.2`.
- And so on for `3.3.3.3` and `4.4.4.4`.

This allows the task to apply the configuration for each NTP server individually.

### Running the Playbook

To execute the playbook, you would use the following command:

```bash
ansible-playbook ntp_config.yaml 
```

### Playbook Output

The playbook output might resemble this:

```plaintext
PLAY [Configure NTP] *******************************************************************

TASK [Configure NTP on Router] *********************************************************
changed: [172.16.10.14] => (item=1.1.1.1)
changed: [172.16.10.14] => (item=2.2.2.2)
changed: [172.16.10.14] => (item=3.3.3.3)
changed: [172.16.10.14] => (item=4.4.4.4)

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

### Analysis of Playbook Output

- **Play Execution**: The play named "Configure NTP" begins execution.
- **Task Execution**: The task "Configure NTP on Router" executes for each item in the `ntp_server` list.
  - For each IP address in the `ntp_server` list, a configuration change is applied to the router.
  - The output confirms successful configuration changes for each NTP server.
- **Play Recap**: The play recap summarizes the execution:
  - `ok=1`: One task executed successfully.
  - `changed=1`: The task made configuration changes.
  - `unreachable=0`: No hosts were unreachable.
  - `failed=0`: No tasks failed.
  - `skipped=0`: No tasks were skipped.

This example demonstrates the use of loops in Ansible to efficiently configure multiple items, simplifying the management of network devices.

## Loop Through Device Information

To process device information, we use the `ios_facts` module, which collects facts from a device running IOS.

Here's how it works:

```yaml
---
- name: "Playbook: Loop IP Addr"
  hosts: router
  gather_facts: false

  tasks:
    - name: "Get facts from device"
      cisco.ios.ios_facts:
        gather_subset: interfaces

    - name: "Print device information"
      ansible.builtin.debug:
        msg: "{{ ansible_facts['net_hostname'] }} has IP Addr {{ item }}"
      loop: "{{ ansible_facts['net_all_ipv4_addresses'] }}"
```

### Playbook Explanation

This playbook, named "Loop IP Addr," is designed to run on a host group named "router." The `gather_facts` option is set to `false` because we manually gather the necessary facts using the `ios_facts` module.

#### Tasks

1. **Get facts from device**

   - The `cisco.ios.ios_facts` module is used to gather information from the device, specifically focusing on the `interfaces` subset.

2. **Print device information**

   - The `ansible.builtin.debug` module is used to print the device's hostname and its IP addresses.
   - The `loop` directive iterates over the list of IP addresses stored in `ansible_facts['net_all_ipv4_addresses']`.

### Understanding the Loop

In the second task, the loop takes each IP address from the list `ansible_facts['net_all_ipv4_addresses']` and prints a message. The message includes the device's hostname and the current IP address (`{{ item }}`) from the loop. This way, each IP address of the device is printed along with the device's hostname.

```
PLAY [Playbook: Loop IP Addr] **********************************************************

TASK [Get facts from device] ***********************************************************
ok: [172.16.10.14]

TASK [Print device information] ********************************************************
ok: [172.16.10.14] => (item=9.9.9.10) => {
    "msg": "R1 has IP Addr 9.9.9.10"
}
ok: [172.16.10.14] => (item=172.16.10.14) => {
    "msg": "R1 has IP Addr 172.16.10.14"
}
ok: [172.16.10.14] => (item=192.168.71.139) => {
    "msg": "R1 has IP Addr 192.168.71.139"
}
ok: [172.16.10.14] => (item=1.1.1.1) => {
    "msg": "R1 has IP Addr 1.1.1.1"
}

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=2    changed=0    unreachable=0    failed=0    skipped=0
```

As per documentation, we can modify the playbook:

```yaml
---
- name: "Playbook: Loop IP Addr"
  hosts: router
  gather_facts: false

  tasks:
    - name: "Get facts from device"
      cisco.ios.ios_facts:
        gather_subset: interfaces

    - name: "Print device information"
      ansible.builtin.debug:
        msg: "{{ ansible_net_hostname }} has IP Addr {{ item }}"
      loop: "{{ ansible_net_all_ipv4_addresses }}"
```

This playbook demonstrates how to gather device information using the `ios_facts` module and print each IP address associated with a device. By utilizing the `debug` module and looping through the IP addresses, the playbook provides a clear and concise way to display critical network information for devices running IOS.
