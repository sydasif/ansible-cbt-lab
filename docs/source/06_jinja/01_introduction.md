## Generating Configuration with Jinja2

With Jinja2, you can create templates that define the structure of your configuration files. By feeding these templates with data, you can quickly generate configurations that are consistent and tailored to the specific needs of each device.

For network engineers, knowing how to use Jinja2 is a valuable skill. It simplifies the process of creating and managing network configurations, saves time, and reduces the likelihood of errors. This efficiency is crucial in managing complex and large-scale networks.

### How It Works- Static and Variable Data

As a network engineer, you might type a command like `router ospf 1`. In this command, `router ospf` is static, but the value `1` is variable and might be different for the next configuration, such as `99`. Jinja2 helps in separating this static data from the variable data, allowing you to create dynamic and reusable templates.

With Jinja2, you can define templates that include both static parts and placeholders for variable data. When you provide the specific variables, Jinja2 renders the final configuration by filling in these placeholders.

#### Storing Variables in Ansible

In Ansible, variables are stored in YAML files. These files can be part of the inventory, or located in `group_vars` and `host_vars` directories. This organization helps in managing and accessing the variables easily.

From these YAML files, Ansible pulls the variables and uses Jinja2 templates to generate the final configuration. This process makes network automation more efficient, as you can quickly apply different configurations by changing only the variable data.

By using Jinja2 with Ansible, network engineers can streamline the creation and deployment of network configurations, ensuring consistency and reducing manual errors.

To understand and master these concepts, practice is essential. Let's start with a simple exercise involving two routers.

#### Example Routers

We'll work with two routers with IP addresses `172.16.10.14` and `172.16.10.11`.

#### Creating YAML Files in `host_vars`

1. Create two files in the `host_vars` folder, one for each router.

2. Add the following YAML data for OSPF configuration:

**For Router `172.16.10.14`:**

```yaml
# host_vars/172.16.10.14.yml
ospf:
  id: 100
```

**For Router `172.16.10.11`:**

```yaml
# host_vars/172.16.10.11.yml
ospf:
  id: 99
```

These YAML files contain the variable data for each router's OSPF configuration. The Jinja2 template can then use these variables to generate the correct configuration for each router dynamically.

### Jinja2 Template for OSPF Configuration

To dynamically generate the OSPF configuration using the variables from the YAML files, you can create a Jinja2 template.

Create a Jinja2 template file, for example, `ospf.j2`:

```py
router ospf {{ ospf.id }}
```

This template uses the `ospf` dictionary to access the `id` variables from the YAML files. When rendered, it will produce the appropriate OSPF configuration for each router based on their respective variables.

#### Example Usage with Ansible

Here’s how you can use the Jinja2 template with Ansible to generate the configuration:

1. **Create the Playbook:**

Create a playbook file, for example, `ospf_config.yaml`:

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

2. **Directory Structure:**

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

Ansible will look at the templates directory by default.

3. **Run the Playbook:**

Execute the playbook with Ansible:

```
(.venv) [zolo@localhost ansible-cbt-lab]$ ansible-playbook ospf_config.yaml 

PLAY [Load Jinja2 Template] ************************************************************

TASK [Configure OSPF] ******************************************************************
changed: [172.16.10.14]
changed: [172.16.10.11]

PLAY RECAP *****************************************************************************
172.16.10.11               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
172.16.10.14               : ok=1    changed=1    unreachable=0    failed=0    skipped=0
```

This will generate OSPF configuration for each router as specified.

By using a Jinja2 template and Ansible, you can easily generate dynamic OSPF configurations for different routers. This approach simplifies the management of network configurations, making it more efficient and less error-prone.
