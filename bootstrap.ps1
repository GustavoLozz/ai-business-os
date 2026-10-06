$ErrorActionPreference = "Stop"
Set-Location "C:\Users\RCA\Desktop\AI-BUSINESS-OS"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   AI-BUSINESS-OS  -  BOOTSTRAP v1.2" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[0/8] Verificando Python..." -ForegroundColor Yellow
try {
    $py = py -3.13 --version 2>$null
    if (-not $py) { throw "Python no encontrado" }
    Write-Host "      OK -> $py" -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Python no encontrado en PATH." -ForegroundColor Red
    Read-Host
    exit 1
}

Write-Host "[1/8] Creando estructura de carpetas..." -ForegroundColor Yellow
$dirs = @(
    "src\orchestrator","src\memory","src\tasks","src\agents",
    "src\permissions","src\git_checkpoints","src\tests",
    "src\reports","src\dashboard",
    "agents\director","agents\architect","agents\developer",
    "agents\quantum_rd","agents\tester","agents\auditor","agents\business",
    "simulator\customers","simulator\products","simulator\costs",
    "simulator\sales","simulator\margins","simulator\scenarios",
    "reports","logs","memory","checkpoints"
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}
Write-Host "      OK -> $($dirs.Count) carpetas verificadas/creadas" -ForegroundColor Green

Write-Host "[2/8] Creando entorno virtual Python..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    py -3.13 -m venv .venv
    Write-Host "      OK -> .venv creado" -ForegroundColor Green
} else {
    Write-Host "      OK -> .venv ya existia" -ForegroundColor Green
}

Write-Host "[3/8] Escribiendo requirements.txt..." -ForegroundColor Yellow
$req = @(
    "rich==13.9.4",
    "pydantic==2.10.4",
    "python-dotenv==1.0.1",
    "pyyaml==6.0.2",
    "requests==2.32.3",
    "pytest==8.3.4",
    "qiskit==1.3.1"
)
$req | Out-File -Encoding utf8 requirements.txt
Write-Host "      OK -> requirements.txt" -ForegroundColor Green

Write-Host "[4/8] Instalando dependencias (puede tardar varios minutos)..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
Write-Host "      OK -> dependencias instaladas" -ForegroundColor Green

Write-Host "[5/8] Escribiendo GOVERNANCE.md..." -ForegroundColor Yellow
$gov = @(
    "# AI-BUSINESS-OS - GOVERNANCE",
    "",
    "## Autoridad",
    "- GUSTAVO: autoridad final.",
    "- DIRECCION/DISENO: arquitectura, estrategia, prioridades.",
    "- ORCHESTRATOR: ejecuta y coordina. NO improvisa arquitectura.",
    "- AGENTES: ejecutan dentro de sus permisos.",
    "",
    "## Reglas de oro",
    "1. Ningun agente modifica main directamente.",
    "2. Flujo: checkpoint -> cambio -> test -> auditoria -> aprobacion.",
    "3. Maximo 3 intentos por tarea. Luego STOP + informe + espera humano.",
    "4. Prohibido: borrar sin permiso, instalar software arbitrario,",
    "   operar cuentas reales, enviar mensajes reales.",
    "5. Prohibido convertir tarea chica en reescritura general sin aprobacion.",
    "",
    "## Presupuesto de autonomia",
    "MAX_INTENTOS_POR_TAREA = 3",
    "REQUIERE_APROBACION    = cambios criticos"
)
$gov | Out-File -Encoding utf8 GOVERNANCE.md
Write-Host "      OK -> GOVERNANCE.md" -ForegroundColor Green

Write-Host "[6/8] Escribiendo .gitignore..." -ForegroundColor Yellow
$gi = @(
    ".venv/",
    "__pycache__/",
    "*.pyc",
    ".env",
    "*.log",
    "memory/*.tmp"
)
$gi | Out-File -Encoding utf8 .gitignore
Write-Host "      OK -> .gitignore" -ForegroundColor Green

Write-Host "[7/8] Inicializando Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init | Out-Null
    git config user.name "AI-BUSINESS-OS" | Out-Null
    git config user.email "os@local" | Out-Null
}
git add . 2>$null
git commit -m "checkpoint-000-inicial: bootstrap AI-BUSINESS-OS" 2>$null | Out-Null
Write-Host "      OK -> checkpoint-000-inicial creado" -ForegroundColor Green

Write-Host "[8/8] Generando primer reporte..." -ForegroundColor Yellow
$today = Get-Date -Format "yyyy-MM-dd"
$reportDir = "reports\$today"
if (-not (Test-Path $reportDir)) { New-Item -ItemType Directory -Path $reportDir -Force | Out-Null }
$reportLines = @(
    "# AI-BUSINESS-OS - Reporte Bootstrap",
    "",
    "Fecha: $today",
    "Estado: ETAPA 0 COMPLETADA",
    "Python: $py"
)
$reportLines | Out-File -Encoding utf8 "$reportDir\daily-report.md"
Write-Host "      OK -> $reportDir\daily-report.md" -ForegroundColor Green

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "          AI-BUSINESS-OS - PANEL CEO" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " SISTEMA       OK OPERATIVO" -ForegroundColor Green
Write-Host " ORQUESTADOR   OK (esqueleto)" -ForegroundColor Green
Write-Host " CHECKPOINT    checkpoint-000-inicial"
Write-Host " REPORTE       reports\$today\daily-report.md"
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " ETAPA 0 COMPLETADA." -ForegroundColor Green
Write-Host ""
Write-Host "Presiona ENTER para cerrar esta ventana..." -ForegroundColor Yellow
Read-Host