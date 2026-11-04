# Native preview staging and rollback / Staging и откат

**Production is not switched.** The production `.github/workflows/deploy.yml`, existing Astro source and `sedrava-dev/` are unchanged. On `main`, the registered `deploy-sedrava-dev.yml` also remains unchanged; only the feature-branch copy is replaced with a manual native-staging wrapper. Preview CI cannot publish. No release/tag/package upload.

## Single manual confirmation using the existing registered workflow

The safe native staging workflow is only in a feature branch. GitHub requires a manual workflow to be registered on the default branch. To avoid merging site code or triggering production deployment, use the existing `Build Sedrava dev website` workflow (which is already registered on main) and select the native feature branch:

https://github.com/VasiliiBabkin/sedrava-site/actions/workflows/deploy-sedrava-dev.yml

1. Open **Run workflow**, select `feature/sedrava-native-docs-live-examples`.
2. To prepare without publishing, leave `publish` unchecked. The job checks the latest successful preview for the exact chosen SHA and packages the accepted bytes.
3. To explicitly approve publication to **dev.virtreal.ru only**, check `publish` and click **Run workflow**. No run ID or domain typing is needed; the safe wrapper fixes the dev target.
4. Monitor the job and its `sedrava-native-staging-http-evidence` artifact. The HTTP and cache gate can still fail and trigger a rollback; no production deployment is authorized.

For backups, an existing `SEDRAVA_STAGING_BACKUP_DIR` variable is used if configured. Otherwise, the remote SSH account creates `$HOME/.sedrava-native-backups` (0700), only if it canonically resolves outside the public site tree. If this cannot be established, the workflow fails before touching the dev root. No backup directory under the web root is accepted. The existing `production` GitHub environment is used only for its stored SSH credentials; its deployment **target is hard-coded to dev**.

## Verified-artifact preparation

1. Wait for all three engines in `preview-sedrava-native.yml` to succeed at the exact website SHA. Review screenshots and `native-parity.json` / `native-provenance.json`. The independent `build webapp` outputs must match the embedded bytes.
2. Download a successful `sedrava-native-site-chromium` artifact. It contains `native-site/`, standalone comparison apps and source/file hash receipts. Browser screenshots/results and traces are in separate evidence/traces artifacts of the same successful run.
3. `stage_bundle.py` rejects a different/dirty SHA, missing/extra/modified files, symlinks, unsafe names and oversized payloads. It creates a deterministic file-only tar and checksum list **without rebuilding** the accepted website.
4. The manual `stage-sedrava-native.yml` verifies that the chosen preview run finished successfully on this exact SHA before downloading it. `publish` defaults to false. Merely building/downloading the bundle never accesses SSH.

## Preconditions for real dev publication

- Explicit manual `publish: true`, confirmation exactly `dev.virtreal.ru`, and the native feature branch.
- Existing reviewed `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS` (and optional port). Keys are not requested or copied into the repository.
- Repository/environment variable `SEDRAVA_STAGING_BACKUP_DIR`: an **existing approved writable nonpublic directory**, outside the documented public web tree. No guessed backup path is created. It must resolve canonically without symlinks.
- The only deployment target is the already documented dev root from the existing dev workflow: `/var/www/virtreal_ru_usr27/data/www/virtreal.ru/dev`. It can never be overridden with the production path.
- GitHub may require registering a new manual workflow on the default branch before it can be dispatched. That infrastructure-only change requires owner review; do not merge this entire site feature to production merely to register a workflow.

The workflow has not been executed against the server. The current managed session cannot reach `https://dev.virtreal.ru`: the network proxy returned **403 CONNECT tunnel failed**. This is an access-policy limitation, not evidence that the host is down. Remote route handling, headers, permissions, backup and rollback are **unverified** until an actual approved staging run completes. Availability/values of SSH secrets and backup configuration have not been assumed.

## Publication behavior and rollback

`stage_remote.sh` checks the exact canonical dev directory, rejects symlink trees and non-file/archive traversal entries, checks the accepted tar SHA, and backs up the current dev tree **before writing any site file**. It writes only the accepted bundle paths; unrelated old files are retained. Extraction is not an atomic directory switch; dev can briefly serve mixed files. This limitation is explicit and is not acceptable evidence of an atomic production cutover.

A failed extraction/hash check restores the old snapshot. A failed external HTTP verification also invokes rollback. Rollback removes only newly introduced managed file paths and restores the previous dev snapshot. It never targets Astro production. Backups are not put under the public document root.

For a later manual rollback, use the same reviewed SSH identity and approved backup directory, and run the checked-in script on the server with operation `rollback` and the recorded deployment identifier (`<40-hex-website-SHA>-<numeric-GitHub-run-ID>`). Review the script and identifier before executing. Do not delete the backup until dev has been accepted. Server-side rollback has not been exercised by this session; local tests validate the bundle/checksum/caching guards only.

## Real HTTP acceptance and cache policy

`verify_staging.py` requests the actual dev routes/resources and compares every response against the accepted manifest. It checks clean directory routes and records Cache-Control/ETag/Last-Modified. Mutable HTML, JS, CSS and JSON need `no-cache`, `no-store` or max-age <=300; content-addressed assets may have long immutable caching. A missing/overlong policy blocks acceptance and triggers rollback. The script does not silently modify Nginx/FASTPANEL configuration.

Suggested host policy for owner review: revalidate HTML and unversioned runtime files; cache hash-named assets immutably; serve directory index.html with `try_files` without SPA rewrites; retain HTTPS. Actual server configuration paths are not known and are not invented here. The catalog endpoint is CI-only; a static 404/error remains visible and must not be replaced with fake success.

Before accepting dev, also run the real browser flows against HTTPS dev, including inline iframe readiness, actions and search. Byte equality alone cannot prove that server CSP/X-Frame-Options allows embedding. This remote browser gate remains unverified.

## Status decisions

- **GO for local/artifact inspection:** only after the exact SHA has green browser, source/link parity and security/accessibility checks.
- **NO-GO for claiming a verified dev deployment:** until the real manual run, backup/rollback and HTTP verification succeed.
- **NO-GO for production cutover:** requires complete acceptance, remote evidence and a separate explicit owner decision. Do not merge to main to bypass it.

Русский: workflow готовит только проверенный артефакт. Публикация требует явного ручного флага, точного домена, прежних SSH-данных и согласованного непубличного каталога резервных копий. Каталог production не используется. Перед записью создаётся backup; ошибка хешей/HTTP вызывает откат. Распаковка dev не атомарна. В этой сессии удалённые проверки и откат не выполнялись из-за сетевого 403; зелёные локальные тесты не подменяют их. Для production нужно отдельное решение владельца.
