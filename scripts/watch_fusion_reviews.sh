#!/usr/bin/env bash
# watch_fusion_reviews.sh - surveillance locale des heartbeats et mandats de l'IA Contradictoire
# Usage :
#   baseline                       amorce l'état connu sans signaler les fichiers existants
#   watch [interval_sec]           boucle de surveillance (défaut : 10 secondes)
#   check                          état courant (PID, log, nombre de fichiers connus)
#   stop                           arrête le watcher enregistré
# Surveille : HEARTBEAT_CONTRADICTOIRE*.md, HEARTBIT_CONTRADICTOIRE*.md,
#             REVIEW_REQUEST_*.md et REVIEW_ADMISSION_REGISTRY.md.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
WATCH_DIR="${REPO_DIR}/docs/fusion"
STATE_DIR="${STATE_DIR:-/tmp/codex-fusion-watch}"
LOG="${STATE_DIR}/detections.log"
KNOWN="${STATE_DIR}/known.tsv"
PIDFILE="${STATE_DIR}/watch.pid"
INTERVALFILE="${STATE_DIR}/interval"
INTERVAL="${INTERVAL:-10}"

mkdir -p "${STATE_DIR}"
touch "${KNOWN}" "${LOG}"

log() { printf '[%s] %s\n' "$(date -Is)" "$*" >> "${LOG}"; }

scan_worktree() {
  local file hash line
  for file in "${WATCH_DIR}"/HEARTBEAT_CONTRADICTOIRE*.md \
              "${WATCH_DIR}"/HEARTBIT_CONTRADICTOIRE*.md \
              "${WATCH_DIR}"/REVIEW_REQUEST_*.md \
              "${WATCH_DIR}"/REVIEW_ADMISSION_REGISTRY.md; do
    [ -f "${file}" ] || continue
    hash=$(sha256sum "${file}" | cut -d' ' -f1)
    line="${file}|${hash}|worktree"
    if ! grep -Fqx "${line}" "${KNOWN}"; then
      if grep -Fq "${file}|" "${KNOWN}"; then
        log "MODIFIED ${file} sha256=${hash}"
      else
        log "NEW ${file} sha256=${hash}"
      fi
      printf '%s\n' "${line}" >> "${KNOWN}"
    fi
  done
}

cmd_baseline() {
  scan_worktree
  log "baseline amorcée (${INTERVAL}s)"
}

cmd_watch() {
  local interval="${1:-${INTERVAL}}"
  printf '%s\n' "$$" > "${PIDFILE}"
  printf '%s\n' "${interval}" > "${INTERVALFILE}"
  log "watch démarré PID=$$ interval=${interval}s"
  while true; do
    scan_worktree
    sleep "${interval}"
  done
}

cmd_check() {
  if [ -f "${PIDFILE}" ] && kill -0 "$(cat "${PIDFILE}")" 2>/dev/null; then
    echo "watcher: ACTIF (PID $(cat "${PIDFILE}"), interval $(cat "${INTERVALFILE}" 2>/dev/null || echo unknown)s)"
  else
    echo "watcher: INACTIF"
  fi
  echo "fichiers connus : $(wc -l < "${KNOWN}")"
  echo "--- dernières détections ---"
  tail -20 "${LOG}" 2>/dev/null || echo "(log vide)"
}

cmd_stop() {
  if [ -f "${PIDFILE}" ] && kill -0 "$(cat "${PIDFILE}")" 2>/dev/null; then
    kill "$(cat "${PIDFILE}")"
    echo "watcher: arrêt demandé (PID $(cat "${PIDFILE}"))"
  else
    echo "watcher: déjà inactif"
  fi
  rm -f "${PIDFILE}"
  rm -f "${INTERVALFILE}"
}

case "${1:-}" in
  baseline) cmd_baseline ;;
  watch) cmd_watch "${2:-}" ;;
  check) cmd_check ;;
  stop) cmd_stop ;;
  *) echo "usage: $0 {baseline|watch [sec]|check|stop}" >&2; exit 2 ;;
esac
