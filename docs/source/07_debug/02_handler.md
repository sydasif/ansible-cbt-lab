## Ansible Handlers

Sometimes, you want a task to run only when a change is made on a machine. For example, you may want to restart a service if a task updates the configuration of that service, but not if the configuration is unchanged. Ansible uses handlers to address this use case.

### Handler Example

In the previous example, we made a configuration change on `172.16.10.14` by configuring NTP servers on a router. Now, let's amend the playbook to include a handler.

1. **Create the Playbook with a Handler**

Update your playbook to notify a handler when the NTP configuration changes:

```yaml
---
- name: "Playbook - Register Variable"
  hosts: 172.16.10.14
  gather_facts: false

  tasks:
    - name: "NTP Configuration"
      cisco.ios.ios_config:
        src: "ntp.j2"
      notify:
        - NTP_Handler
      register: ntp_output

  handlers:
    - name: NTP_Handler
      ansible.builtin.debug:
        msg: "{{ ntp_output }}"
```

### Explanation of the Playbook

- **NTP Configuration Task**:
  - This task applies the NTP configuration using the `ios_config` module.
  - The `notify` keyword is used to notify the handler named `NTP_Handler` if the task results in a change.
  - The output of the task is registered in the `ntp_output` variable.
  
- **Handlers Section**:
  - The handler named `NTP_Handler` is defined to print the content of `ntp_output` using the `debug` module.

### Viewing the Output

After running the playbook, the output will be displayed in your terminal. For instance:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook handler_example.yaml

PLAY [Playbook - Register Variable] ****************************************************

TASK [NTP Configuration] ***************************************************************
ok: [172.16.10.14]

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=1    changed=0    unreachable=0    failed=0    skipped=0
```

- The playbook did not show the commands that were executed because there was no change in the device configuration.

### Updating the Configuration

Now, let's update our `host_vars` file to see the handler in action:

```yaml
# host_vars/172.16.10.14
---
ospf:
  process_id: 10
  router_id: 1.1.1.1
  networks:
    - network: 9.9.9.8
      mask: 0.0.0.3
    - network: 192.168.71.0
      mask: 0.0.0.255

ntp:
  servers:
    - 3.3.3.3
    - 4.4.4.4
    - 5.5.5.5
    - 6.6.6.6  # new entry
```

We have added a new NTP server `6.6.6.6`. Now, after running the playbook again:

```sh
(.venv) ➜  ansible-cbt-lab git:(main) ✗ ansible-playbook handler_example.yaml

PLAY [Playbook - Register Variable] ***************************************************

TASK [NTP Configuration] **************************************************************
changed: [172.16.10.14]

RUNNING HANDLER [NTP_Handler] *********************************************************
ok: [172.16.10.14] => {
    "msg": {
        "banners": {},
        "changed": true,
        "commands": [
            "ntp server 6.6.6.6"
        ],
        "failed": false,
        "updates": [
            "ntp server 6.6.6.6"
        ]
    }
}

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=2    changed=1    unreachable=0    failed=0    skipped=0
```

When the playbook is run, the `NTP Configuration` task detects a change due to the addition of the new NTP server. As a result, the handler `NTP_Handler` is triggered, and the `debug` module prints the `ntp_output` variable, showing the new NTP server that was added.

This way, you can use handlers to perform specific actions only when changes are detected, ensuring that tasks such as restarting services or printing debug information are only executed when necessary.
