# 📚 WordPress Generator – An Educational Sandbox for Terraform Backends

This repository serves as a **structured learning environment** for provisioning and decommissioning AWS infrastructure by integrating **Python automation**, **Jinja2 templating**, and **Terraform** in the **AWS** Platform.

Rather than simply providing static code, this repository is intended to demonstrate key operational concepts in an accessible manner. It is designed for students and professionals who wish to gain a deeper understanding of backend state management and dynamic infrastructure generation, as well as anyone wanting to have their one website.

---

## 🌋 Repository Structure

The following structure exists at the root level:

```
wordpress-generator/
├── generate.py          # Python script to create backend (S3/DynamoDB) and generate Terraform files
├── destroy.py           # Python script to remove backend or site folders
├── README.md
│
├── templates/           # Jinja2 templates used by generate.py
│   ├── providers.tf.j2
│   ├── main.tf.j2
│   ├── data.tf.j2
│   ├── outputs.tf.j2
│
├── website-types/       # Startup scripts for each website type
│   ├── apache.sh
│   ├── wordpress.sh
│   └── (add new types, e.g., ghost.sh)
│
├── sites/               # Populated dynamically with generated site folders
    ├── example-apache/  # Example generated folder containing Terraform files
    ├── example-wordpress/
    │   ├── providers.tf
    │   ├── main.tf
    │   └── ...
```

---

## 📦 Dependencies

Ensure the following are installed prior to use:

- [Python 3.x](https://www.python.org/downloads/)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/) (optional but recommended)

**Python packages in use:**

```
External Packages
- boto3
- jinja2
- InquirerPy

Standard Library Packages
- shutil
- os
- random
- string
```

It is recommended to run this environment in [Visual Studio Code](https://code.visualstudio.com/) with a Python virtual environment for optimal workflow.

---

## 🚀 Quickstart

1. **Generating the Site**

    ```bash
    cd /aws-website-generator
    python generate.py
   # Prompts for Website Name (Cosmetic e.g. "test")
   # Prompts for Website Type (Selects from website-types)
   ```
    
2. **Deployment of the Site**

   ```bash
   cd sites/<your-site-folder>/
   terraform init
   terraform apply
   # Confirm with "yes"
   ```

3. **Decommissioning the Site**

   ```bash
   terraform destroy
   # Confirm with "yes"
   ```

4. **Cleanup of Website Resources**

   ```bash
   python destroy.py
   # Select your site
   ```

5. **Full Cleanup**

   ```bash
   python destroy.py
   # Select "core" to remove top level S3/DynamoDB backend resources
   ```

---

## 🔧 Extending the System

The repository is designed to be extensible. To add a new website type (e.g., Ghost):

1. Create a new startup script in `website-types/` (e.g., `ghost.sh`).
2. Edit `generate.py` to include `"ghost"` in the `websites` list for InquirerPy selection.
3. Execute `python generate.py` and select the new type to generate your configuration.

Terraform files will be rendered into a new folder under `sites/` (e.g., `sites/my-ghost/`).

---

## ✅ Prerequisites

Prior to running, ensure the following:

- A valid **AWS account** (Free Tier is sufficient).
- An **IAM user** with programmatic access and AdministratorAccess permissions, configured on your local machine:

```bash
aws configure
```

Provide the following when prompted:

- AWS Access Key ID and Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (`json` recommended)

---

## 📚 Key Learning Objectives

- **Terraform Remote Backends:** S3 for state storage and DynamoDB for state locking.
- **Python Automation:** Use boto3 to manage AWS resources programmatically.
- **Jinja2 Templating:** Generate Terraform files dynamically.
- **Extensibility:** Modify or add new website types with minimal effort.

---

## 🌱 Future Enhancements

- Additional website types (Ghost, Hugo, Nginx static hosting)

---

**Happy Learning and Automating!**
