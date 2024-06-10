## Dynamic Jinja2 Template for OSPF Configuration

To create a more dynamic Jinja2 template that can handle various configurations, you can include additional variables and logic in your template. This will make it flexible enough to accommodate different network setups and requirements.

### Enhanced Jinja2 Template

Create a Jinja2 template file, for example, ospf.j2:

```py
{% for ospf_instance in ospf %}
router ospf {{ ospf_instance.process_id }}
  router-id {{ ospf_instance.router_id }}
  {% for network in ospf_instance.networks %}
  network {{ network.network }} {{ network.wildmask }} area {{ network.area }}
  {% endfor %}
{% endfor %}
```

#### Example YAML Variable Files

Update your YAML variable files with the new structure:

**For Router `172.16.10.14`:**

```yaml
# host_vars/172.16.10.14.yaml
ospf:
  - process_id: 88
    router_id: 88.88.88.88
    networks:
      - network: 8.8.8.0
        wildmask: 0.0.0.255
        area: 0
```

**For Router `172.16.10.11`:**

```yaml
# host_vars/172.16.10.11.yaml
ospf:
  - process_id: 99
    router_id: 99.99.99.99
    networks:
      - network: 9.9.9.0
        wildmask: 0.0.0.255
        area: 0
```

Use the same playbook file, `ospf_config.yaml`:

```yaml
---
- name: Load Jinja2 Template
  hosts: 172.16.10.11, 172.16.10.14
  gather_facts: false

  tasks:
    - name: Configure OSPF
      cisco.ios.ios_config:
        src: "ospf.j2"
```

#### Directory Structure

Ensure your directory structure looks like this:

```sh
your_project/
├── ansible.cfg
├── host_vars
│   ├── 172.16.10.11.yaml
│   └── 172.16.10.14.yaml
├── inventory.cfg
├── templates
│   └── ospf.j2
└── ospf_config.yaml
```

#### Running the Playbook

Execute the playbook with Ansible:

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ospf_config.yaml

PLAY [Load Jinja2 Template] ************************************************************

TASK [Configure OSPF] ******************************************************************
changed: [172.16.10.11]
changed: [172.16.10.14]

PLAY RECAP *****************************************************************************
172.16.10.11               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

### Resulting Configurations

**For Router `172.16.10.14`:**

```
router ospf 1
  router-id 88.88.88.88
  network 8.8.8.0 0.0.0.255 area 0
```

**For Router `172.16.10.11`:**

```
router ospf 99
  router-id 99.99.99.99
  network 9.9.9.0 0.0.0.255 area 0
```

By using this detailed Jinja2 template and Ansible, you can generate comprehensive and accurate OSPF configurations for different routers. This method enhances the management of network configurations, ensuring consistency and reducing manual errors.
