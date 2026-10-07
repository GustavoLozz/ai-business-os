"""Panel CEO enriquecido. Usa rich si esta disponible, sino texto plano."""
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    RICH_DISPONIBLE = True
except ImportError:
    RICH_DISPONIBLE = False


class Dashboard:
    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.console = Console() if RICH_DISPONIBLE else None

    def mostrar(self):
        if RICH_DISPONIBLE:
            self._mostrar_rich()
        else:
            self._mostrar_plano()

    def _mostrar_plano(self):
        e = self.orch.estado()
        lineas = [
            "=" * 60,
            "              AI-BUSINESS-OS - PANEL CEO",
            "=" * 60,
            f"  SISTEMA              [OK] OPERATIVO",
            f"  ORQUESTADOR          [OK] ACTIVO",
            f"  AGENTES              {e['agentes']}",
            f"  TAREAS               {e['tareas']['total']}",
            f"  MEMORIAS             {e['memoria']['total']}",
            f"  PENDIENTES APROB.    {e['pendientes_aprobacion']}",
            "=" * 60,
            "  AGENTES",
        ]
        for a in self.orch.registry.listar():
            icono = "[*]" if a["estado"] == "activo" else "[ ]"
            lineas.append(f"    {icono} {a['nombre']:15} - {a['rol']}")
        lineas.extend([
            "=" * 60,
            f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
        ])
        print("\n".join(lineas))

    def _mostrar_rich(self):
        e = self.orch.estado()
        self.console.clear()
        self.console.print()
        self.console.rule("[bold cyan]AI-BUSINESS-OS - PANEL CEO[/bold cyan]")

        # Estado general
        tabla = Table(show_header=False, box=None, padding=(0, 2))
        tabla.add_column("K", style="bold")
        tabla.add_column("V")
        tabla.add_row("SISTEMA", "[green]OK OPERATIVO[/green]")
        tabla.add_row("ORQUESTADOR", "[green]OK ACTIVO[/green]")
        tabla.add_row("AGENTES", str(e["agentes"]))
        tabla.add_row("TAREAS", str(e["tareas"]["total"]))
        tabla.add_row("MEMORIAS", str(e["memoria"]["total"]))
        tabla.add_row("PENDIENTES APROB.", str(e["pendientes_aprobacion"]))
        self.console.print(Panel(tabla, title="[bold]Estado[/bold]", border_style="cyan"))

        # Agentes
        ta = Table(title="Agentes", show_header=True, header_style="bold cyan")
        ta.add_column("Estado", width=10)
        ta.add_column("Nombre", style="bold")
        ta.add_column("Rol")
        for a in self.orch.registry.listar():
            estado = "[green]activo[/green]" if a["estado"] == "activo" else "[yellow]registrado[/yellow]"
            ta.add_row(estado, a["nombre"], a["rol"])
        self.console.print(ta)

        self.console.print(
            f"[dim]Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
        )
        self.console.rule()