# ============================================================
#  AI-BUSINESS-OS - Daily Audit
# ============================================================
# Corre todos los dias:
#   1. Flujo de agentes (auditoria automatica)
#   2. Informe ejecutivo
#   3. Reportes automaticos
#   4. Guarda todo en reports/YYYY-MM-DD/auto_audit/
# ============================================================

$ErrorActionPreference = "Continue"
$Root = "C:\Users\RCA\Desktop\AI-BUSINESS-OS"
$Python = "$Root\.venv\Scripts\python.exe"
$Today = Get-Date -Format "yyyy-MM-dd"
$Hour = Get-Date -Format "HHmmss"
$OutputDir = "$Root\reports\$Today\auto_audit"
$LogFile = "$OutputDir\daily_audit_$Hour.log"

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

function Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

Log "=== AI-BUSINESS-OS Daily Audit ==="
Log "Inicio: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

Set-Location $Root

# 1. Flujo de agentes
Log "[1/3] Corriendo flujo de agentes..."
$flujo = & $Python orchestrator.py --flujo "Auditar el estado del proyecto" 2>&1 | Out-String
$flujo | Out-File "$OutputDir\flujo_$Hour.txt" -Encoding utf8
Log "Flujo completado. Output: flujo_$Hour.txt"

# 2. Informe ejecutivo
Log "[2/3] Generando informe ejecutivo..."
$informe = & $Python orchestrator.py --informe-ejecutivo 2>&1 | Out-String
$informe | Out-File "$OutputDir\informe_$Hour.txt" -Encoding utf8
Log "Informe generado. Output: informe_$Hour.txt"

# 3. Reportes automaticos
Log "[3/3] Generando reportes automaticos..."
$reportes = & $Python orchestrator.py --reporte 2>&1 | Out-String
$reportes | Out-File "$OutputDir\reportes_$Hour.txt" -Encoding utf8
Log "Reportes generados."

Log "Fin: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Log "=== Daily Audit completado ==="

# Rotacion: borrar logs de mas de 30 dias
$Limite = (Get-Date).AddDays(-30)
Get-ChildItem "$Root\reports" -Directory | Where-Object {
    $_.Name -match "^\d{4}-\d{2}-\d{2}$" -and [datetime]::ParseExact($_.Name, "yyyy-MM-dd", $null) -lt $Limite
} | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Log "Rotacion de logs completada."