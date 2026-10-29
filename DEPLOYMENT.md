# Deployment to FASTPANEL / Nginx

The static site is built by GitHub Actions and deployed to:

`/var/www/virtreal_ru_usr27/data/www/virtreal.ru/sedrava/`

Domain: https://sedrava.virtreal.ru

## First deployment

1. Confirm in FASTPANEL that this is the document root for the subdomain, and that the selected SSH user has write permission to it.
2. Create a dedicated SSH key for deployment, preferably with restricted permissions. Do not use a root account.
3. In GitHub repository Settings → Secrets and variables → Actions, add:
   - `SSH_HOST`: VDS hostname or IP address
   - `SSH_USER`: restricted SSH account with write access to the site directory
   - `SSH_PRIVATE_KEY`: private key corresponding to an authorized public key on the VDS
   - `SSH_KNOWN_HOSTS`: verified SSH host key line (obtain from a trusted channel; do not blindly trust ssh-keyscan)
   - `SSH_PORT`: optional, defaults to 22
4. Optionally configure the `production` GitHub environment with approval requirements.
5. Run Actions → Deploy Sedrava website → Run workflow.
6. Verify both the English and Russian pages and HTTPS.

The deployment is intentionally manual initially and does **not** use `--delete` with rsync, to avoid removing unrelated files. After the first successful release, automate deployment and consider an atomic release directory with rollback.

Never commit passwords, SSH private keys, or server environment files.
