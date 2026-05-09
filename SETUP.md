# Setup — push this repo to GitHub

## One-time setup

1. Install Git: https://git-scm.com/download/win  (then close and reopen PowerShell)
2. Sign in to GitHub: https://github.com/signup
3. Create a new empty repo on GitHub named `intent-gap-study`
   - Don't add a README, .gitignore, or license — we already have ours
4. Configure git with your name/email (one time per machine):
   ```
   git config --global user.name "Kanupriya Yakhmi"
   git config --global user.email "kanupriyayakhmi@gmail.com"
   ```

## First push

Open PowerShell and paste these commands in order. Replace `YOUR-USERNAME` with your real GitHub username.

```
cd "C:\Users\KP\Documents\Claude\Projects\Startup defensible moat\intent-gap-study"
git init
git add .
git commit -m "Initial scaffold: scope, paper draft, lit review, code stubs, outreach"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/intent-gap-study.git
git push -u origin main
```

If `git push` asks for a password, use a GitHub Personal Access Token, not your account password. Make one at https://github.com/settings/tokens (classic, with `repo` scope).

## Pushing edits later

After you've made changes:

```
cd "C:\Users\KP\Documents\Claude\Projects\Startup defensible moat\intent-gap-study"
git add .
git commit -m "describe what you changed"
git push
```

## Common issues

- `git not recognized` → Git isn't installed or PowerShell wasn't reopened after install.
- `Permission denied` on push → use a Personal Access Token, not your password.
- `Updates were rejected` → run `git pull --rebase` first, then `git push`.
