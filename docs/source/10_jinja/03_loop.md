# Dynamic Configuration with Jinja2 Templates in Ansible

Creating dynamic and adaptable configurations for various network setups is crucial in network automation. Jinja2 templates offer a powerful way to achieve this by utilizing loops and other control structures. This section will guide you through creating dynamic Jinja2 templates that can handle different OSPF configurations for routers and how to integrate them into your Ansible playbooks.

## Understanding Jinja2 Loop Syntax

Jinja2 loop syntax is similar to Python, making it intuitive for those familiar with Python programming. Loops in Jinja2 are enclosed within `{% %}` tags. A typical loop starts with `{% for item in items %}` and ends with `{% endfor %}`. This allows you to iterate over lists or dictionaries in your template, dynamically generating content based on the provided data.

### Example of Jinja2 Loop

Here’s a basic example of how a loop works in a Jinja2 template:

```jinja2
{% for item in items %}
  {{ item }}
{% endfor %}
```

This template will iterate over the `items` list and print each `item`. We will apply this principle to generate dynamic OSPF configurations for different routers.

## Structuring Your Variables

To accommodate different network setups, update your YAML variable files with the necessary OSPF configurations. Each router will have its own YAML file under the `host_vars` directory.

### OSPF Configuration for Router `172.16.10.14`

Create a YAML file named `172.16.10.14.yaml` in the `host_vars` directory:

```yaml
# host_vars/172.16.10.14.yaml
ospf:
  process_id: 10
  router_id: 1.1.1.1
  networks:
    - network: 9.9.9.8
      mask: 0.0.0.3
    - network: 192.168.71.0
      mask: 0.0.0.255
```

### OSPF Configuration for Router `172.16.10.11`

Similarly, create a YAML file named `172.16.10.11.yaml`:

```yaml
# host_vars/172.16.10.11.yaml
ospf:
  process_id: 10
  router_id: 2.2.2.2
  networks:
    - network: 9.9.9.8
      mask: 0.0.0.3
    - network: 172.16.10.0
      mask: 0.0.0.255
```

## Creating the Jinja2 Template

Place the Jinja2 template file `ospf.j2` in the `templates` directory. This template will generate the OSPF configuration for each router based on the variables defined in their respective YAML files.

### `ospf.j2` Template

```jinja2
router ospf {{ ospf.process_id }}
  router-id {{ ospf.router_id }}
  {% for network in ospf.networks %}
  network {{ network.network }} {{ network.mask }} area 0
  {% endfor %}
```

### Explanation of the Template

- The `router ospf` command is followed by the OSPF process ID.
- The `router-id` command sets the OSPF router ID.
- The inner loop iterates over the `networks` list within the OSPF configuration, generating a `network` command for each network entry with the specified address and mask.

## Updating the Ansible Playbook

Use the existing playbook file, `ospf_config.yaml`, to apply the Jinja2 template to the routers.

### `ospf_config.yaml` Playbook

```yaml
---
- name: Load Jinja2 Template
  hosts: 172.16.10.11, 172.16.10.14
  gather_facts: false

  tasks:
    - name: Generate OSPF Configuration
      cisco.ios.ios_config:
        src: "ospf.j2"
```

### Explanation of the Playbook

- The playbook targets the hosts `172.16.10.11` and `172.16.10.14`.
- It uses the `cisco.ios.ios_config` module to apply the generated OSPF configuration from the `ospf.j2` template.

## Ensuring Proper Directory Structure

Ensure your project directory is structured correctly for Ansible to locate the necessary files and templates:

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

## Running the Playbook

Execute the playbook to generate and apply the OSPF configuration:

```sh
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook playbook/ospf_config.yaml

PLAY [Load Jinja2 Template] ************************************************************

TASK [Configure OSPF] *****************************************************************
changed: [172.16.10.14]
changed: [172.16.10.11]

PLAY RECAP *****************************************************************************
172.16.10.11               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

By using Jinja2 templates with loops, you can create dynamic and reusable configurations for different network devices. This approach not only simplifies the management of network configurations but also ensures consistency across different devices. With the provided example, you can easily adapt and extend the templates and variable files to suit various network requirements.
