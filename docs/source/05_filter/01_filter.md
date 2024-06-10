## Formatting Data in Network Automation

Ansible filters are incredibly useful for transforming and formatting data within your network automation playbooks. These filters can be particularly beneficial for debugging and ensuring that network configuration data is presented in a human-readable manner.

### Rendering Data in JSON and YAML

When working with complex network configuration data, it’s often helpful to convert it into a format that’s easier to read and understand. Ansible provides filters to convert variables into JSON and YAML formats.

#### Converting to JSON

To convert a variable containing network configuration data in YAML to JSON format, use the `to_json` filter:

```
{{ network_config | to_json }}
```

#### Converting to YAML

To convert a variable containing network configuration data from JSON to YAML format, use the `to_yaml` filter:

```
{{ network_config | to_yaml }}
```

For more readable outputs, especially useful during debugging, Ansible provides filters to produce nicely formatted JSON and YAML.

#### Nicely Formatted JSON

To produce a more human-readable JSON output for network data, use the `to_nice_json` filter:

```
{{ network_config | to_nice_json }}
```

#### Nicely Formatted YAML

To produce a more human-readable YAML output for network data, use the `to_nice_yaml` filter:

```
{{ network_config | to_nice_yaml }}
```

#### Finding the Minimum Value in a List

To get the smallest number from a list:

```yaml
- name: Find Minimum Number
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Display Min Number
      vars:
        my_list:
          - 1
          - 2
          - 3
          - 4
          - 5
      ansible.builtin.debug:
        msg: "{{ my_list | min }}"
```

#### Finding the Maximum Value in a List

To get the largest number from a list:

```yaml
- name: Find Maximum Number
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Display Max Number
      vars:
        my_list:
          - 1
          - 2
          - 3
          - 4
          - 5
      ansible.builtin.debug:
        msg: "{{ my_list | max }}"
```

### Set Theory Filters

These functions return unique sets from lists, which can be useful for comparing network configurations.

#### Finding the Symmetric Difference

To find items that are in either list1 or list2 but not in both:

```yaml
- name: Find Symmetric Difference
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Display Symmetric Difference
      vars:
        list1:
          - 1
          - 2
          - 3
          - 4

        list2:
          - 1
          - 2
          - 3

      ansible.builtin.debug:
        msg: "{{ list1 | symmetric_difference(list2) }}"
```
By using these simple filters, you can easily format and analyze your network configuration data, making your network automation tasks much easier.
