# Orbit AI Ops Assistant

Welcome to **Orbit AI Ops Assistant**, a powerful, terminal-based DevOps assistant designed to simplify and unify your workflows. Orbit integrates seamlessly with multiple tools and services to empower teams with intelligent, context-aware automation and suggestions.

---

## Project Overview

Orbit enables developers and operations teams to manage cloud infrastructure, orchestrate workflows, and troubleshoot issues efficiently using an intuitive command-line interface. By leveraging AI and modern DevOps tools, Orbit bridges the gap between manual operations and fully automated pipelines.

### Key Features

1.  **Workspace Management**

    - Create, switch, and manage named workspaces for multi-environment configurations.
    - Automatically load AWS profiles, Kubernetes contexts, and Terraform states.

2.  **Workflow Automation**

    - Define multi-step workflows in YAML files for seamless execution.
    - Execute commands in sequence with built-in error handling and rollback.

3.  **AI-Powered Suggestions**

    - Receive intelligent recommendations based on historical usage patterns.
    - Proactively troubleshoot issues and suggest fixes.

4.  **Integration with Key DevOps Tools**

    - **AWS**: Manage multiple accounts and roles with ease.
    - **Kubernetes**: Switch contexts, stream logs, and manage pods.
    - **Terraform**: Safely apply or destroy configurations.
    - **Helm**: Deploy, upgrade, and rollback Helm charts.
    - **Okta**: Securely authenticate and retrieve session tokens.

5.  **Security and Encryption**

    - Securely manage credentials, tokens, and secrets with AES encryption.
    - Implement automatic session cleanup and timeout management.

---

## Technology Stack

- **Programming Language**: Python
- **CLI Framework**: Typer for a robust and user-friendly command-line interface.
- **Cloud Integrations**:
  - AWS SDK (boto3)
  - Kubernetes Client
  - Terraform CLI Wrapper
  - Helm CLI Wrapper
  - Okta API for authentication
- **Workflow Automation**: YAML-based definitions using PyYAML.
- **AI Engine**: Integration with OpenAI API for intelligent suggestions and NLP.
- **Security**: PyCrypto for AES encryption of sensitive data.
- **Rich UI Enhancements**: [Rich](https://rich.readthedocs.io/) for colorful, interactive terminal output.

---

## Core Functionalities

### Workspace Management

Define and manage environments with ease:

`workspace:
  name: production
  aws_profile: prod-profile
  kubernetes_context: prod-cluster
  terraform_state: s3://prod-terraform-state`

### Workflow Orchestration

Simplify complex pipelines with YAML workflows:

```yaml
workflows
  deploy-infra:
    - aws: switch dev-account
    - tf: apply
    - k8s: switch prod-cluster
    - helm: deploy app-release`
```

### AI-Driven Insights

- **Command Suggestions**: "Would you like to run `terraform plan`? [Yes/No]"
- **Error Resolution**: "Detected pod crash. Suggested fix: restart pod or scale deployment."

### Security by Design

- **Encrypted Storage**: Securely store secrets and configurations.
- **Automatic Cleanup**: Ensure temporary files and session data are cleaned after use.

---

## Roadmap

### **Phase 1: Core Features (3 Months)**

- Workspace management
- AWS, Terraform, and Kubernetes basic functionality

### **Phase 2: Advanced Features (6 Months)**

- Helm and Okta integration
- Workflow automation
- Secrets management

### **Phase 3: AI Enhancements (9 Months)**

- Intelligent workflow predictions
- Proactive troubleshooting
- Natural language command support

---

## Repository Structure

```bash
├── .github/                  # CI/CD workflows
├── docs/                     # Project documentation
├── src/                      # Source code
│   ├── cli/                  # CLI components
│   ├── core/                 # Core logic (AI, workflows, config)
│   ├── integrations/         # Tool and API integrations
│   └── utils/                # Utility functions
├── tests/                    # Unit, integration, and E2E tests
├── requirements.txt          # Python dependencies
├── setup.py                  # Installation script
├── README.md                 # High-level project overview
└── LICENSE                   # License information`
```

---

## Contributing

We welcome contributions! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to get started.

---

## License

Orbit AI Ops Assistant is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

Empower your DevOps workflows with Orbit—making infrastructure management smarter, faster, and more reliable! 🚀
