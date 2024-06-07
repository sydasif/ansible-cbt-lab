## Defining Variables in a Play

Variables in Ansible can be defined directly within a play using the `vars` keyword. This allows for easy configuration and access to variables that are only visible to tasks executed in that particular play.

```yaml
- hosts: webservers
  vars:
    http_port: 80
```

In the example above, the `http_port` variable is set to `80` and will be accessible to any tasks within the play that targets the `webservers` group.

## Loop in Ansible

Loops in programming are used to perform the same task repeatedly. Ansible provides several keywords for looping, including `loop`, `with_<lookup>`, and `until`. These allow you to execute a task multiple times with different parameters. For instance, if you need to configure the same settings on different network interfaces, loops can simplify the process.

### Example: Configuring NTP Servers on a Router

Consider the following Ansible playbook, which configures NTP (Network Time Protocol) on a router:

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

### Explanation of the Playbook

- **Play Definition**: The play is named "Configure NTP" and targets the `router` host group. The `gather_facts: false` directive disables the default behavior of gathering facts about the hosts.

- **Task Definition**: A single task is defined within the play. This task uses the `vars` keyword to define a list of NTP servers.

- **Task Details**:
  - **Task Name**: "Configure NTP on Router"
  - **Variable Definition**: The `ntp_server` variable is defined as a list of four IP addresses.
  - **Module**: The `cisco.ios.ios_ntp_global` module is used to configure NTP settings on Cisco IOS devices.
  - **Configuration**: The `config` parameter specifies the NTP peers to be configured, using a loop to iterate over the `ntp_server` list.
  - **Loop**: The `loop` keyword iterates over the `ntp_server` list, configuring each NTP server in turn.

### Understanding `item` in the Loop

In the context of Ansible loops, the `item` keyword represents the current element in the list being processed. When the loop iterates over the `ntp_server` list, `item` takes on the value of each NTP server IP address, one by one.

For example:
- During the first iteration, `item` is `1.1.1.1`.
- During the second iteration, `item` is `2.2.2.2`.
- And so on for `3.3.3.3` and `4.4.4.4`.

This allows the task to apply the configuration for each NTP server individually.

### Executing the Playbook

To execute the playbook, you would run the following command:

```bash
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ntp_config.yaml 
```

### Playbook Output

The output of running the playbook might look like this:

```plaintext
PLAY [Configure NTP] *****************************************************************************************************

TASK [Configure NTP on Router] *******************************************************************************************
changed: [172.16.10.14] => (item=1.1.1.1)
changed: [172.16.10.14] => (item=2.2.2.2)
changed: [172.16.10.14] => (item=3.3.3.3)
changed: [172.16.10.14] => (item=4.4.4.4)

PLAY RECAP ***************************************************************************************************************
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Analysis of Playbook Output

- **Play Execution**: The play named "Configure NTP" starts execution.
- **Task Execution**: The task "Configure NTP on Router" is executed for each item in the `ntp_server` list.
  - For each IP address in the `ntp_server` list, a configuration change is applied to the router.
  - The output indicates that the configuration was successfully changed for each NTP server.
- **Play Recap**: The play recap shows the summary of the execution:
  - `ok=1`: One task was executed successfully.
  - `changed=1`: The task made changes to the configuration.
  - `unreachable=0`: No hosts were unreachable.
  - `failed=0`: No tasks failed.
  - `skipped=0`: No tasks were skipped.
  - `rescued=0`: No tasks were rescued from failure.
  - `ignored=0`: No tasks were ignored.

This example demonstrates how to use loops in Ansible to configure multiple items efficiently, making the process of managing network devices more streamlined and less error-prone.
