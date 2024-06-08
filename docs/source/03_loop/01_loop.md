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
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ntp_config.yaml 
```

### Playbook Output

The playbook output might resemble this:

```plaintext
PLAY [Configure NTP] *********************************************************************

TASK [Configure NTP on Router] ************************************************************
changed: [172.16.10.14] => (item=1.1.1.1)
changed: [172.16.10.14] => (item=2.2.2.2)
changed: [172.16.10.14] => (item=3.3.3.3)
changed: [172.16.10.14] => (item=4.4.4.4)

PLAY RECAP *******************************************************************************
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
