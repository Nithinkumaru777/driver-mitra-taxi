# Builds the site for the company server and publishes it at
#   https://srv1995762.hstgr.cloud/arun-enterprises/driver-mitra-taxi/
# Caddy serves /opt/fleetpay/deploy/site there (see deploy/Caddyfile in the fleetpay-app repo).
# Usage: powershell -File scripts\deploy-vps.ps1
$ErrorActionPreference = 'Stop'
$server = 'root@62.72.57.27'
$path = 'arun-enterprises/driver-mitra-taxi'

Set-Location (Split-Path $PSScriptRoot)
$env:BASE_PATH = "/$path/"
$env:SITE_URL = 'https://srv1995762.hstgr.cloud'
npx astro build
if ($LASTEXITCODE) { throw 'build failed' }

$tar = Join-Path $env:TEMP 'driver-mitra-taxi-site.tgz'
tar -czf $tar -C dist .
scp $tar "${server}:/tmp/site.tgz"
# Unpack beside the live copy, then swap, so visitors never see a half-copied site.
ssh $server "set -e; d=/opt/fleetpay/deploy/site/$path; rm -rf `$d.new; mkdir -p `$d.new; tar -xzf /tmp/site.tgz -C `$d.new; chmod -R u=rwX,go=rX `$d.new; rm -rf `$d.old; [ -d `$d ] && mv `$d `$d.old; mv `$d.new `$d; rm -rf `$d.old /tmp/site.tgz"
Remove-Item $tar
Write-Host "Published: https://srv1995762.hstgr.cloud/$path/"
