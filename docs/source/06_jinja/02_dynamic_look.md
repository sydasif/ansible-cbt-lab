## Dynamic Multi-Vendor Network Configuration

In the previous section, we used the same Jinja2 template for configuration. However, in a multi-vendor network, different devices may require different templates. Let's explore how to handle multi-vendor configurations using another example.

### Example Scenario

In the previous lab, we had two Cisco routers with IP addresses `172.16.10.11` and `172.16.10.14`. Suppose the router at `172.16.10.14` is a Juniper device and requires a different configuration. To achieve this, we need to add a key in the `host_vars` file to reference in the playbook.

**For Router `172.16.10.14`:**

```yaml
# host_vars/172.16.10.14.yaml
ospf:
  process_id: 88
  router_id: 88.88.88.88

device_vendor: "juniper"
```

Here, we define the key `device_vendor: "juniper"` for the Juniper device.

**For Router `172.16.10.11`:**

```yaml
# host_vars/172.16.10.11.yaml
ospf:
  process_id: 99
  router_id: 99.99.99.99

device_vendor: "cisco"
```

In this host file, we use the same key name with a different value `device_vendor: "cisco"`. It's important that the key names are the same but the values are different.

### Creating Vendor-Specific Templates

In the `templates` directory, create two files named `cisco.j2` and `juniper.j2`.

**`juniper.j2` Template:**

```jinja2
set protocols ospf area {{ ospf.process_id }} interface ge-0/0/0.0
set protocols ospf area {{ ospf.process_id }} router-id {{ ospf.router_id }}
```

**`cisco.j2` Template:**

```jinja2
router ospf {{ ospf.process_id }}
  router-id {{ ospf.router_id }}
```

### Updating the Playbook

Amend the playbook to accommodate the new configuration:

```yaml
---
- name: Load Jinja2 Template
  hosts: 172.16.10.11, 172.16.10.14
  gather_facts: false

  tasks:
    - name: Generate OSPF Configuration
      template:
        src: "templates/{{ device_vendor }}.j2"
        dest: "/path/to/output/ospf_config_{{ inventory_hostname }}.conf"
```

### Directory Structure

Ensure your directory structure looks like this:

```sh
your_project/
├── ansible.cfg
├── host_vars
│   ├── 172.16.10.11.yaml
│   └── 172.16.10.14.yaml
├── inventory.cfg
├── templates
│   ├── cisco.j2
│   └── juniper.j2
└── ospf_config.yaml
```

### Running the Playbook

Execute the playbook with Ansible:

```sh
ansible-playbook ospf_config.yaml
```

Sample output:

```
PLAY [Load Jinja2 Template] ************************************************************

TASK [Generate OSPF Configuration] *****************************************************
changed: [172.16.10.14]
changed: [172.16.10.11]

PLAY RECAP *****************************************************************************
172.16.10.11               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

### Resulting Configurations

The configurations will be generated and saved on the control node, not pushed directly to the devices.

**For Router `172.16.10.14` (Juniper):**

```
set protocols ospf area 88 interface ge-0/0/0.0
set protocols ospf area 88 router-id 88.88.88.88
```

**For Router `172.16.10.11` (Cisco):**

```
router ospf 99
  router-id 99.99.99.99
```

By using different Jinja2 templates and referencing them dynamically in the Ansible playbook, you can efficiently manage multi-vendor network configurations. This approach ensures that each device gets the correct configuration, reducing errors and streamlining the network management process.

The generated configurations are saved on the control node, allowing you to review them before applying them to the devices.
