## Ansible Inventory Settings

Ansible uses an inventory to manage hosts in your infrastructure. The inventory lists information about target hosts, like their IP addresses or Fully Qualified Domain Names (FQDNs). The default inventory file is located at `/etc/ansible/hosts`, but you can specify a different file using the `-i <path>` option or in the configuration with `inventory`.

### Formats for Inventory Files

You can create inventory files in different formats, with `INI` and `YAML` being the most common. Here are examples based on a [lab setup](/docs/source/04_lab-setup/index.md):

#### INI Format

A basic INI format might look like this:

```ini
[router]
172.16.10.11

[core]
172.16.10.12

[switch]
172.16.10.13
172.16.10.14
```

The names in brackets are group names. They help classify hosts so you can manage specific sets of hosts easily.

You can also use DNS names instead of IP addresses:

```ini
[router]
r1

[core]
core-sw

[switch]
access1
access2
```

Ensure your DNS settings can resolve these names to the correct IP addresses.

#### YAML Format

Here’s how the same inventory looks in YAML format:

```yaml
all:
  children:
    router:
      hosts:
        172.16.10.11:
    core:
      hosts:
        172.16.10.12:
    switch:
      hosts:
        172.16.10.13:
        172.16.10.14:
```

In this format, `all` is the top-level group containing all hosts and groups. The `hosts` key lists each host, and `children` contains subgroups like `router`, `core`, and `switch`.

Ansible includes two default groups: `all`, which targets all hosts, and `ungrouped`, which contains hosts not in any other group.

### Defining Host Aliases

You can define aliases for hosts to make them easier to reference:

```ini
core-sw ansible_host=172.16.10.12
```

### Inventory and Variables

Ansible allows setting variables in the inventory to control behavior and manage hosts more effectively.

#### Host Variables

You can define variables for each host:

```ini
[router]
r1 ansible_host=172.16.10.11 ansible_user=bob

[core]
core-sw ansible_host=172.16.10.12 ansible_user=joe
```

#### Group Variables

Variables can also be set at the group level:

```ini
[router]
r1 ansible_host=172.16.10.11 ansible_user=bob ansible_password=bob123

[core]
core-sw ansible_host=172.16.10.12 ansible_user=joe ansible_password=joe123

[campus:children]
router
core

[campus:vars]
ansible_network_os=ios
ansible_connection=network_cli
```

Although you can set variables in the inventory, it’s usually better to store them in separate host and group variable files. This helps keep your project organized and clear.

Create folders named `group_vars` and `host_vars` in the same directory as your inventory file to store these variable files. For example, `group_vars/campus.yaml` might look like this:

```yaml
---
# group_vars/campus.yaml
ansible_user: admin
ansible_password: cisco
ansible_network_os: ios
ansible_connection: network_cli
```

### Viewing Inventory Information

Use the following command to view your inventory structure:

```bash
ansible-inventory -i inventory.yaml --graph
```

This command shows the group hierarchy and the hosts in each group. To view details about a specific host, use:

```bash
ansible-inventory -i inventory.yaml --host r1
```

### Key Points About Inventory

1. **Host Information:** Inventory files contain crucial information about target hosts.
2. **Default Location:** The default inventory file is at `/etc/ansible/hosts`.
3. **File Format:** Inventory files can be in `INI` or `YAML` format.
4. **Grouping Hosts:** Group names classify hosts based on common attributes or roles.
5. **Special Groups:** Groups like `campus` can categorize network devices.
6. **Default Groups:** `all` includes every host, and `ungrouped` includes hosts not in other groups.

Using the inventory helps you organize and manage your infrastructure efficiently, making automation tasks with Ansible easier and more effective.
