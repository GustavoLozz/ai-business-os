"""Tests de los 7 agentes."""
from src.agents import Director, Architect, Developer, QuantumRD, Tester, Auditor, Business


def test_director_descompone_objetivo():
    d = Director()
    r = d.ejecutar({"descripcion": "Simular 30 dias de una empresa"})
    assert r["agente"] == "Director"
    assert len(r["subtareas"]) >= 3
    assert r["metodo"] == "simbolico"


def test_arquitecto_propone_componentes():
    a = Architect()
    r = a.ejecutar({"descripcion": "Simular empresa"})
    assert r["agente"] == "Arquitecto"
    assert len(r["arquitectura"]["componentes"]) >= 3
    assert "modulos" in r["arquitectura"]


def test_developer_escribe_en_sandbox():
    d = Developer()
    r = d.ejecutar({"descripcion": "Modelo de clientes"})
    assert r["agente"] == "Developer"
    assert r["sandbox"] is True
    assert r["requiere_aprobacion"] is True
    assert len(r["propuesta"]["archivos"]) >= 1


def test_developer_no_toca_produccion():
    d = Developer()
    d.ejecutar({"descripcion": "Modelo de productos"})
    # El sandbox acumula propuestas, no toca archivos reales
    assert len(d.sandbox) == 1


def test_quantum_experimenta():
    q = QuantumRD()
    r = q.ejecutar({"descripcion": "Optimizar beneficios"})
    assert r["agente"] == "Quantum_RD"
    assert r["sandbox"] is True
    assert "algoritmo" in r["experimento"]
    assert "resultado_simulado" in r["experimento"]


def test_tester_corre_suite():
    t = Tester()
    r = t.ejecutar({"descripcion": "Probar sistema"})
    assert r["agente"] == "Tester"
    assert "resultado" in r
    assert "passed" in r["resultado"]


def test_auditor_aprueba_tarea_limpia():
    a = Auditor()
    r = a.ejecutar({"descripcion": "Tarea normal sin violaciones"})
    assert r["agente"] == "Auditor"
    assert r["aprobado"] is True
    assert r["veredicto"] == "APROBADO"


def test_auditor_bloquea_intento_de_main():
    a = Auditor()
    r = a.ejecutar({"accion": "modificar main", "descripcion": "intento peligroso"})
    assert r["aprobado"] is False
    assert r["veredicto"] == "BLOQUEADO"
    assert any("main" in v for v in r["violaciones"])


def test_auditor_bloquea_borrado_sin_permiso():
    a = Auditor()
    r = a.ejecutar({"accion": "borrar archivos", "descripcion": "sin aprobacion"})
    assert r["aprobado"] is False
    assert any("borrar" in v for v in r["violaciones"])


def test_business_analiza_simulacion():
    b = Business()
    r = b.ejecutar({"descripcion": "Simular empresa 30 dias"})
    assert r["agente"] == "Business"
    assert r["analisis"]["viabilidad"] in ("alta", "media", "baja")
    assert "facturacion_estimada" in r["analisis"]


def test_todos_los_agentes_tienen_reportar():
    agentes = [Director(), Architect(), Developer(), QuantumRD(),
               Tester(), Auditor(), Business()]
    for a in agentes:
        rep = a.reportar()
        assert "nombre" in rep
        assert "rol" in rep
        assert rep["cerebro"] == "simbolico"