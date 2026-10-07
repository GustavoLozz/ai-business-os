"""Tests del dashboard."""
from src.orchestrator.core import Orchestrator
from src.orchestrator.dashboard import Dashboard


def test_dashboard_se_instancia():
    o = Orchestrator()
    d = Dashboard(o)
    assert d is not None


def test_dashboard_no_falla_al_mostrar():
    o = Orchestrator()
    d = Dashboard(o)
    # No debe lanzar excepcion
    d.mostrar()