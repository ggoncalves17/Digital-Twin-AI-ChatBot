# Git and GitHub Workflows

## Git branches

### Branch from main
```bash
# Switch to main
git switch main

# Create a new branch from main
git checkout -b <new branch>
```

### Use descriptive branch names
```
# Feature branches
feature/user-authentication
feature/payment-integration

# Bug fixes
fix/login-error-handling
fix/api-timeout-issue

# Documentation
docs/api-documentation
docs/setup-instructions
```

### Keep history clean
Unless a feature is complex, opt to squash and merge

### Delete after PR merge
Keeps repo clean


## Git commits

- Adhere to [Conventional Commits](https://conventionalcommits.org/)
- Be atomic, i.e., don't create commits dependent on other commits for the project to function.

## Pull requests
- Keep PR titles concise and descriptive.
- Start PR title with an action verb (e.g., Add, Update, Fix, Remove)

Use the following template:
```markdown
## Summary
Quick summary of changes and why

## Changes made
- List of changes made
- Another change
- Last changes

## Additional notes
(Optional) Additional notes or considerations
```
