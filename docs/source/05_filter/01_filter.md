## Formatting Data in Network Automation

Ansible filters are very helpful for changing and formatting data in your network automation playbooks. These filters can make network configuration data easier to read and debug.

### Rendering Data in JSON and YAML

When dealing with complex network configurations, it's useful to convert them into easier-to-read formats. Ansible lets you convert variables into JSON and YAML.

#### Converting to JSON

To convert a variable with network configuration data from YAML to JSON format, use the `to_json` filter:

```
{{ network_config | to_json }}
```

#### Converting to YAML

To convert a variable with network configuration data from JSON to YAML format, use the `to_yaml` filter:

```
{{ network_config | to_yaml }}
```

For more readable outputs, especially for debugging, Ansible provides filters to make JSON and YAML more human-readable.

#### Nicely Formatted JSON

To create a more readable JSON output, use the `to_nice_json` filter:

```
{{ network_config | to_nice_json }}
```

#### Nicely Formatted YAML

To create a more readable YAML output, use the `to_nice_yaml` filter:

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
