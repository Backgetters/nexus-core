#!/bin/bash
# GitHub CLI wrapper functions for OpenClaw

# Repository operations
github_repo_info() {
    gh repo view "$1" --json name,description,url,defaultBranch
}

# List pull requests
github_pr_list() {
    gh pr list --state "$1" --limit 10
}

# Create issue
github_issue_create() {
    gh issue create --title "$1" --body "$2"
}

# Clone repository
github_clone() {
    gh repo clone "$1"
}

# Check authentication status
github_auth_status() {
    gh auth status
}