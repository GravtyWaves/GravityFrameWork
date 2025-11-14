# 🔐 Private Repository Authentication Guide

> **Complete guide for accessing private microservice repositories**

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Authentication Methods](#authentication-methods)
3. [GitHub Setup](#github-setup)
4. [GitLab Setup](#gitlab-setup)
5. [Bitbucket Setup](#bitbucket-setup)
6. [SSH Key Setup](#ssh-key-setup)
7. [Environment Configuration](#environment-configuration)
8. [Usage Examples](#usage-examples)
9. [Troubleshooting](#troubleshooting)
10. [Security Best Practices](#security-best-practices)

---

## 🎯 Overview

Gravity Framework supports accessing **private repositories** for microservices using multiple authentication methods:

- ✅ **Personal Access Tokens (PAT)** - HTTPS authentication
- ✅ **SSH Keys** - SSH authentication
- ✅ **OAuth Tokens** - OAuth flow (future support)
- ✅ **GitHub App** - GitHub App authentication (future support)

---

## 🔑 Authentication Methods

### 1️⃣ **Personal Access Token (Recommended for HTTPS)**

**Pros:**
- ✅ Easy to setup
- ✅ Works across all Git platforms
- ✅ Can be revoked anytime
- ✅ Fine-grained permissions

**Cons:**
- ❌ Must be kept secret
- ❌ Expires (needs renewal)

**Use when:**
- Using HTTPS URLs (`https://github.com/...`)
- Need simple authentication
- Working with multiple platforms

---

### 2️⃣ **SSH Keys (Recommended for SSH)**

**Pros:**
- ✅ More secure than passwords
- ✅ No expiration
- ✅ Standard in development

**Cons:**
- ❌ Requires SSH key generation
- ❌ More complex setup

**Use when:**
- Using SSH URLs (`git@github.com:...`)
- Maximum security needed
- Long-term access required

---

## 🐙 GitHub Setup

### Step 1: Create Personal Access Token

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**

2. Click **Generate new token**

3. Configure token:
   ```
   Name: Gravity Framework - Microservices Access
   Expiration: 90 days (or No expiration for production)
   
   Scopes:
   ✅ repo (Full control of private repositories)
      ✅ repo:status
      ✅ repo_deployment
      ✅ public_repo
      ✅ repo:invite
   ```

4. Click **Generate token**

5. **COPY THE TOKEN** (you won't see it again!)
   ```
   Example: ghp_1234567890abcdefghijklmnopqrstuvwxyzAB
   ```

### Step 2: Set Environment Variable

**Windows (PowerShell):**
```powershell
# Temporary (current session only)
$env:GIT_AUTH_TOKEN = "ghp_YOUR_TOKEN_HERE"

# Permanent (user environment)
[System.Environment]::SetEnvironmentVariable('GIT_AUTH_TOKEN', 'ghp_YOUR_TOKEN_HERE', 'User')
```

**Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export GIT_AUTH_TOKEN="ghp_YOUR_TOKEN_HERE"

# Reload shell
source ~/.bashrc
```

### Step 3: Use in Gravity Framework

```python
from gravity_framework.discovery import ServiceScanner

# Automatic authentication (reads from environment)
scanner = ServiceScanner(services_dir="./services")

# Or provide token explicitly
scanner = ServiceScanner(
    services_dir="./services",
    auth_token="ghp_YOUR_TOKEN_HERE"
)

# Discover private repository
service = scanner.discover_from_git(
    "https://github.com/your-org/private-auth-service.git"
)
```

---

## 🦊 GitLab Setup

### Step 1: Create Personal Access Token

1. Go to GitLab → **Preferences** → **Access Tokens**

2. Create new token:
   ```
   Name: Gravity Framework
   Expiration: 2025-12-31
   
   Scopes:
   ✅ read_repository
   ✅ write_repository
   ```

3. Click **Create personal access token**

4. Copy token:
   ```
   Example: glpat-1234567890abcdefghij
   ```

### Step 2: Use with Gravity

```python
scanner = ServiceScanner(
    services_dir="./services",
    auth_token="glpat-YOUR_TOKEN_HERE"
)

service = scanner.discover_from_git(
    "https://gitlab.com/your-org/private-service.git"
)
```

---

## 🪣 Bitbucket Setup

### Step 1: Create App Password

1. Go to Bitbucket → **Personal settings** → **App passwords**

2. Create app password:
   ```
   Label: Gravity Framework
   
   Permissions:
   ✅ Repositories: Read
   ✅ Repositories: Write
   ```

3. Copy password (shown once!)

### Step 2: Format for Bitbucket

```python
# Bitbucket requires username:password format
auth_token = f"{username}:{app_password}"

scanner = ServiceScanner(
    services_dir="./services",
    auth_token=auth_token
)

service = scanner.discover_from_git(
    "https://bitbucket.org/your-org/private-service.git"
)
```

---

## 🔐 SSH Key Setup

### Step 1: Generate SSH Key

**On your development machine:**

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Output:
# Generating public/private ed25519 key pair.
# Enter file in which to save the key (/home/user/.ssh/id_ed25519): 
# Enter passphrase (empty for no passphrase): 
# Your identification has been saved in /home/user/.ssh/id_ed25519
# Your public key has been saved in /home/user/.ssh/id_ed25519.pub
```

### Step 2: Add SSH Key to Git Platform

**GitHub:**
1. Copy public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste public key

**GitLab:**
1. Go to GitLab → Preferences → SSH Keys
2. Paste public key

**Bitbucket:**
1. Go to Bitbucket → Personal settings → SSH keys
2. Paste public key

### Step 3: Use SSH URL

```python
scanner = ServiceScanner(
    services_dir="./services",
    ssh_key_path="~/.ssh/id_ed25519"  # Optional, auto-detected
)

# Use SSH URL format
service = scanner.discover_from_git(
    "git@github.com:your-org/private-service.git"
)
```

---

## ⚙️ Environment Configuration

### `.env` File Setup

Create `.env` file in project root:

```bash
# Git Authentication
GIT_AUTH_TOKEN=ghp_YOUR_GITHUB_TOKEN_HERE
GIT_SSH_KEY_PATH=~/.ssh/id_ed25519

# Multiple tokens for different platforms
GITHUB_TOKEN=ghp_1234567890
GITLAB_TOKEN=glpat_1234567890
BITBUCKET_TOKEN=username:app_password
```

### Framework Configuration

```python
from pydantic_settings import BaseSettings

class GravitySettings(BaseSettings):
    git_auth_token: Optional[str] = None
    git_ssh_key_path: Optional[str] = None
    github_token: Optional[str] = None
    gitlab_token: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = GravitySettings()
```

---

## 💡 Usage Examples

### Example 1: Single Private Repository

```python
from gravity_framework import GravityFramework

# Initialize framework
framework = GravityFramework(
    project_name="my-app",
    auth_token="ghp_YOUR_TOKEN"
)

# Add private authentication service
framework.add_service(
    "https://github.com/company/private-auth-service.git"
)

# Install and start
framework.install()
framework.start()
```

### Example 2: Multiple Private Repositories

```python
# List of private microservices
private_services = [
    "https://github.com/company/auth-service.git",
    "https://github.com/company/user-service.git",
    "https://github.com/company/payment-service.git",
]

for service_url in private_services:
    framework.add_service(service_url)

framework.install()
```

### Example 3: Mix of Public and Private

```python
# Public repositories (no auth needed)
framework.add_service("https://github.com/public/open-service.git")

# Private repositories (uses auth from environment)
framework.add_service("https://github.com/company/private-service.git")
```

### Example 4: SSH Authentication

```python
scanner = ServiceScanner(
    services_dir="./services",
    ssh_key_path="~/.ssh/company_key"  # Company-specific key
)

service = scanner.discover_from_git(
    "git@github.com:company/secret-service.git"
)
```

---

## 🔍 Troubleshooting

### Problem 1: "Authentication failed"

**Error:**
```
GitCommandError: 'git clone' failed with status 128
fatal: Authentication failed for 'https://github.com/...'
```

**Solutions:**
1. ✅ Check token is valid (not expired)
2. ✅ Verify `GIT_AUTH_TOKEN` environment variable is set
3. ✅ Ensure token has `repo` scope for private repos
4. ✅ Try regenerating token

**Test token manually:**
```bash
# Windows PowerShell
git clone https://$env:GIT_AUTH_TOKEN@github.com/your-org/private-repo.git

# Linux/macOS
git clone https://$GIT_AUTH_TOKEN@github.com/your-org/private-repo.git
```

---

### Problem 2: "Permission denied (publickey)"

**Error:**
```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

**Solutions:**
1. ✅ Verify SSH key is added to Git platform
2. ✅ Check SSH agent is running:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```
3. ✅ Test SSH connection:
   ```bash
   ssh -T git@github.com
   # Should say: "Hi username! You've successfully authenticated"
   ```

---

### Problem 3: "Repository not found"

**Error:**
```
fatal: repository 'https://github.com/...' not found
```

**Possible causes:**
1. ❌ Repository is private but no authentication provided
2. ❌ Repository URL is incorrect
3. ❌ You don't have access to the repository

**Solutions:**
1. ✅ Verify repository exists
2. ✅ Check you have read access
3. ✅ Provide authentication token
4. ✅ Contact repository owner for access

---

### Problem 4: "Token expired"

**Error:**
```
remote: Invalid username or password.
fatal: Authentication failed
```

**Solutions:**
1. ✅ Generate new token (GitHub → Settings → Developer settings)
2. ✅ Update `GIT_AUTH_TOKEN` environment variable
3. ✅ Use tokens without expiration for production

---

## 🛡️ Security Best Practices

### ✅ DO:

1. **Use environment variables for tokens**
   ```python
   auth_token = os.getenv('GIT_AUTH_TOKEN')  # ✅ GOOD
   ```

2. **Add `.env` to `.gitignore`**
   ```bash
   # .gitignore
   .env
   .env.local
   ```

3. **Use fine-grained permissions**
   - Only `read_repository` if services are read-only
   - Avoid full `admin` permissions

4. **Rotate tokens regularly**
   - Set expiration dates (30-90 days)
   - Regenerate before expiry

5. **Use different tokens per project**
   - Easier to revoke
   - Better access control

6. **Store tokens in secrets manager (Production)**
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault

---

### ❌ DON'T:

1. **Never hardcode tokens in code**
   ```python
   auth_token = "ghp_1234567890"  # ❌ NEVER!
   ```

2. **Never commit `.env` files**
   ```bash
   git add .env  # ❌ NEVER!
   ```

3. **Never share tokens in chat/email**
   - Use secure sharing tools
   - Regenerate if accidentally exposed

4. **Never use personal tokens in production**
   - Use service accounts
   - Use deploy keys

5. **Never grant unnecessary permissions**
   - Principle of least privilege
   - Only what's needed

---

## 🚀 Advanced: CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Services

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Git authentication
        run: |
          echo "GIT_AUTH_TOKEN=${{ secrets.GIT_AUTH_TOKEN }}" >> $GITHUB_ENV
      
      - name: Install Gravity Framework
        run: pip install gravity-framework
      
      - name: Deploy microservices
        run: |
          gravity init my-app
          gravity service add https://github.com/company/auth-service.git
          gravity service add https://github.com/company/user-service.git
          gravity install
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - export GIT_AUTH_TOKEN=$GITLAB_TOKEN
    - pip install gravity-framework
    - gravity init my-app
    - gravity service add https://gitlab.com/company/service.git
    - gravity install
  variables:
    GITLAB_TOKEN: $CI_JOB_TOKEN  # GitLab CI token
```

---

## 📊 Authentication Decision Tree

```
Need to access private repository?
│
├─→ Using HTTPS URL?
│   ├─→ YES → Use Personal Access Token
│   │         • Set GIT_AUTH_TOKEN environment variable
│   │         • Framework auto-injects token in URL
│   │
│   └─→ NO → Continue to SSH
│
└─→ Using SSH URL (git@...)?
    └─→ Use SSH Key
        • Generate SSH key: ssh-keygen
        • Add public key to Git platform
        • Specify ssh_key_path (optional)
```

---

## 🎓 Summary

**For Developers (Local Development):**
- ✅ Use Personal Access Token (simple)
- ✅ Store in `.env` file
- ✅ Set `GIT_AUTH_TOKEN` environment variable

**For Production (CI/CD):**
- ✅ Use secrets manager (AWS/Azure/Vault)
- ✅ Use service accounts, not personal tokens
- ✅ Rotate credentials regularly

**For Maximum Security:**
- ✅ Use SSH keys instead of HTTPS
- ✅ Use different keys per project
- ✅ Enable 2FA on Git accounts

---

## 📚 References

- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitLab Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [SSH Key Generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Git Credential Storage](https://git-scm.com/docs/gitcredentials)

---

**Created by:** Gravity Framework Team  
**Last Updated:** November 14, 2025  
**Version:** 1.0.0
