## Ansible for Network Automation

In modern IT environments, automating network management is crucial. This section introduces Ansible for network automation, focusing on its practical benefits and ease of use, especially for those without extensive programming skills.

### Expanding Ansible’s Capabilities

Originally designed for server management, Ansible now supports network devices too. The core concepts, like modules and playbooks, are similar for both servers and networks, though some differences exist to accommodate network-specific tasks. This unified approach helps streamline IT operations and boosts efficiency.

### Push vs. Pull Models in Automation

Understanding the push and pull models is key to grasping how Ansible works.

**Push Model:**

- In a push model, the central server sends commands directly to managed nodes.
- Ansible uses this approach, pushing configurations from a central control machine to the nodes it manages.

**Pull Model:**

- In a pull model, managed nodes regularly check in with a central server to fetch new configurations.
- Tools like Puppet, Chef, and SaltStack use this approach.

### Ansible’s Automation Approach

Ansible is known for its simplicity and ease of use, especially for network engineers without a programming background. It operates in a procedural manner, executing tasks sequentially as defined in playbooks. Ansible also supports declarative models through technologies like NETCONF and RESTCONF, allowing for flexible and scalable network management.

### Easy Adoption for Network Engineers

Ansible is an excellent choice for network engineers looking to automate tasks without deep programming knowledge. The main requirement is understanding YAML, a human-readable data format used to write Ansible playbooks. With YAML, engineers can define tasks, configurations, and workflows clearly and concisely.

### Built-In Concurrency

One of Ansible's significant advantages over traditional Python scripting is its built-in concurrency. Ansible allows tasks to be executed in parallel across multiple nodes, speeding up deployment times and ensuring consistent configurations.

## Getting Started with Network Automation

Ansible supports a wide range of vendors, device types, and actions, enabling comprehensive network management with a single tool. This versatility makes Ansible a powerful solution for automating routine tasks and ensuring consistency across network infrastructures. Communication between the control node and managed nodes is handled through multiple protocols:

- **network_cli by SSH:** A widely-used, secure protocol for managing network devices.
- **netconf by SSH:** Designed specifically for network management, offering enhanced configuration and monitoring capabilities.
- **httpapi by HTTP/HTTPS:** A flexible protocol for interacting with network devices that support RESTful APIs.

Supported network platforms include:

- **Arista: eos:** Automation for Arista's Extensible Operating System.
- **Cisco: ios, iosxr, nxos:** Management of Cisco’s various network operating systems.
- **Juniper: junos:** Automation for Juniper's Junos OS.
- **VyOS: vyos:** Support for VyOS, an open-source network operating system.

Ansible’s extensive support for different network platforms and protocols helps streamline network automation processes and enhances operational efficiency.

### Network Modules

Unlike most Ansible modules, network modules do not run on the managed nodes because most network devices cannot run Python. Instead, these modules execute on the Ansible control node. This method ensures effective network device management. Additionally, network modules use the control node to store backup files, usually in the backup directory under the playbook root directory. This approach allows Ansible to provide consistent network management and backup capabilities without requiring Python on the network devices.

With Ansible, network engineers can streamline their workflows, reduce manual interventions, and achieve greater consistency and reliability in their network operations. This introduction sets the stage for exploring Ansible's capabilities and understanding how it can transform network management practices.