#!/usr/bin/env bash
# Invoked only by the explicitly gated staging workflow. Never targets production.
set -euo pipefail
operation="${1:?install or rollback}"; backup="${2:?existing nonpublic backup directory}"; deployment="${3:?deployment identifier}"; digest="${4:-}"
target='/var/www/virtreal_ru_usr27/data/www/virtreal.ru/dev'
production='/var/www/virtreal_ru_usr27/data/www/virtreal.ru/sedrava'
[[ "$backup" =~ ^/[A-Za-z0-9_./-]+$ && "$backup" != *'/../'* && "$backup" != */.. ]]
[[ "$deployment" =~ ^[a-f0-9]{40}-[0-9]+$ ]]
[[ "$operation" == install || "$operation" == rollback ]]
[[ -d "$target" && -w "$target" && -d "$backup" && -w "$backup" ]]
[[ "$(readlink -f "$target")" == "$target" && "$(readlink -f "$backup")" == "$backup" ]]
# Backups must be outside every public domain directory, not merely outside dev.
[[ "$backup/" != /var/www/virtreal_ru_usr27/data/www/* ]]
[[ "$target" != "$production" ]]
[[ -z "$(find "$target" -type l -print -quit)" ]]
for command in tar sha256sum grep sort comm; do command -v "$command" >/dev/null; done
archive="$backup/$deployment.tar.gz"; sums="$backup/$deployment.files.sha256"; previous="$backup/$deployment.before.tar.gz"
rollback() {
  [[ -f "$previous" && -f "$sums" ]]
  # Remove only new managed files absent from the original snapshot; preserve unrelated files.
  tar -tzf "$previous" | sed 's#^./##' | sort > "$backup/$deployment.old-list"
  while IFS= read -r line; do
    file="${line:66}"
    [[ "$file" =~ ^[A-Za-z0-9_./-]+$ && "$file" != /* && "$file" != *'..'* ]]
    if ! grep -Fxq "$file" "$backup/$deployment.old-list"; then rm -f -- "$target/$file"; fi
  done < "$sums"
  tar -xzf "$previous" -C "$target"
  printf 'Restored previous dev snapshot %s\n' "$deployment"
}
if [[ "$operation" == rollback ]]; then rollback; exit; fi
[[ "$digest" =~ ^[a-f0-9]{64}$ && -f "$archive" && -f "$sums" && ! -e "$previous" ]]
printf '%s  %s\n' "$digest" "$archive" | sha256sum -c -
# The bundle is built by a reviewed local packager: files only, no absolute/traversal paths.
[[ -z "$(tar -tvzf "$archive" | sed -n '/^[^\-]/p')" ]]
while IFS= read -r file; do [[ "$file" =~ ^[A-Za-z0-9_./-]+$ && "$file" != /* && "$file" != *'..'* ]]; done < <(tar -tzf "$archive")
(umask 077; tar -czf "$previous" -C "$target" .)
trap 'rollback' ERR
(umask 022; tar -xzf "$archive" -C "$target")
(cd "$target" && sha256sum -c "$sums")
trap - ERR
printf 'Installed verified native preview on dev only: %s\n' "$deployment"
