#!/usr/bin/env bash
set -euo pipefail

# --- config ---
VERIFY_URL="${VERIFY_URL:-http://localhost:8088}"
GNAP_URL="${GNAP_URL:-http://localhost:8089}"
MISTY_BASE="${MISTY:-}"

say() { printf "\n==> %s\n" "$*"; }
ok()  { printf "   ✅ %s\n" "$*"; }
bad() { printf "   ❌ %s\n" "$*"; exit 1; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || bad "Missing command: $1"
}

http_code() {
  # prints status code only
  curl -sS -o /dev/null -w "%{http_code}" "$1"
}

json_get() {
  curl -sS "$1"
}

post_json() {
  local url="$1"
  local body="$2"
  curl -sS -H "Content-Type: application/json" -d "$body" "$url"
}

# --- checks ---
say "Command prerequisites"
need_cmd docker
need_cmd curl
ok "docker + curl present"

say "Docker daemon"
docker info >/dev/null 2>&1 || bad "Docker daemon not reachable (is Docker Desktop running?)"
ok "Docker daemon reachable"

say "Containers running (expect: a2a-gateway-verify-1, a2a-gateway-gnap-1)"
running="$(docker ps --format '{{.Names}}' | tr '\n' ' ')"
echo "   Running: $running"
echo "$running" | grep -q "a2a-gateway-verify-1" || bad "verify container not running"
echo "$running" | grep -q "a2a-gateway-gnap-1"   || bad "gnap container not running"
ok "verify + gnap containers running"

say "Service health endpoints"
vcode="$(http_code "${VERIFY_URL}/health")"
gcode="$(http_code "${GNAP_URL}/health")"
echo "   verify /health HTTP $vcode"
echo "   gnap   /health HTTP $gcode"
[ "$vcode" = "200" ] || bad "verify health failed"
[ "$gcode" = "200" ] || bad "gnap health failed"
ok "verify + gnap health OK"

say "Misty reachability"
[ -n "$MISTY_BASE" ] || bad "MISTY env var is not set. Example: export MISTY='http://192.168.1.183/api'"
echo "   MISTY=$MISTY_BASE"

# quick Misty GETs that do not change state
scode="$(http_code "${MISTY_BASE%/}/skills/running")"
echo "   Misty /skills/running HTTP $scode"
[ "$scode" = "200" ] || bad "Cannot reach Misty at $MISTY_BASE (check Wi-Fi/VLAN/IP)"

ok "Misty reachable"

say "Optional: Misty speak (set DO_SPEAK=1 to enable)"
if [ "${DO_SPEAK:-0}" = "1" ]; then
  resp="$(post_json "${MISTY_BASE%/}/tts/speak" '{"text":"Sanity check: gateway host can reach Misty."}')"
  echo "   Response: $resp"
  ok "Misty speak request sent"
else
  echo "   (skipped) export DO_SPEAK=1 to test TTS"
fi

say "DONE"
ok "All checks passed"
