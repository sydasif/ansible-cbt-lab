## Registering Variables

You can create variables from the output of an Ansible task using the `register` keyword. These registered variables can be used in subsequent tasks within your playbook. Additionally, you can use the `debug` module to print statements during execution, which is useful for debugging variables or expressions.

### Example

Let's add NTP server configuration to a device.

1. **Add NTP Server Configuration in `host_vars` File**

Create a file named `host_vars/172.16.10.14` and add the following content:

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
```

2. **Create an NTP Template File**

Create a file named `ntp.j2` in the templates directory with the following content:

```j2
{% for server in ntp.servers %}
ntp server {{ server }}
{% endfor %}
```

3. **Create a Playbook**

Create a playbook for registering the variable and printing the result:

```yaml
---
- name: "Playbook - Register Variable"
  hosts: 172.16.10.14
  gather_facts: false

  tasks:
    - name: "NTP Configuration"
      cisco.ios.ios_config:
        src: "ntp.j2"
      register: ntp_output

    - name: "Print NTP Result"
      ansible.builtin.debug:
        msg: "{{ ntp_output }}"
```

### Explanation

- **NTP Configuration Task**: This task applies the NTP configuration using the `ios_config` module and registers the output in the variable `ntp_output`.
- **Print NTP Result Task**: This task uses the `debug` module to print the content of the `ntp_output` variable, showing what commands were executed.

#### Viewing the Output

After running the playbook, the output will be displayed in your terminal, showing the commands that were executed.

```sh
(.venv) ➜ ansible-cbt-lab git:(main) ✗ ansible-playbook playbook/register_variable.yaml

PLAY [Playbook - Register Variable] *****************************************************

TASK [NTP Configuration] ****************************************************************

TASK [Print NTP Result] *****************************************************************
ok: [172.16.10.14] => {
    "msg": {
        "banners": {},
        "changed": true,
        "commands": [
            "ntp server 3.3.3.3",
            "ntp server 4.4.4.4",
            "ntp server 5.5.5.5"
        ],
        "failed": false,
        "updates": [
            "ntp server 3.3.3.3",
            "ntp server 4.4.4.4",
            "ntp server 5.5.5.5"
        ]
    }
}

PLAY RECAP *****************************************************************************
172.16.10.14               : ok=2    changed=1    unreachable=0    failed=0    skipped=0
```

This way, you can capture and view the commands executed on the device, which helps in verifying and debugging the configuration changes made by Ansible.
