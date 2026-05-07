# tests/test_temperature.py
import pytest
from temperature import is_overheating

# ── Casos normales ──────────────────────────────────────────
def test_temperatura_alta():
    """Temperatura sobre el umbral → debe dar alarma."""
    assert is_overheating(90) is True

def test_temperatura_normal():
    """Temperatura bajo el umbral → debe ser OK."""
    assert is_overheating(60) is False

def test_temperatura_exacta_en_umbral():
    """Exactamente 80°C → no es alarma (límite no incluido)."""
    assert is_overheating(80) is False

def test_temperatura_un_grado_sobre_umbral():
    """80.1°C → sí es alarma."""
    assert is_overheating(80.1) is True

# ── Validación de sensor ────────────────────────────────────
def test_temperatura_negativa_lanza_error():
    """Temperatura negativa → error de sensor."""
    with pytest.raises(ValueError):
        is_overheating(-5)

def test_temperatura_cero_es_valida():
    """0°C es válido (no es negativo)."""
    assert is_overheating(0) is False

def test_temperatura_muy_alta():
    """Temperatura extrema → alarma."""
    assert is_overheating(999) is True

# ── Tipos inválidos ─────────────────────────────────────────
def test_tipo_invalido_string():
    """Un string debe lanzar TypeError."""
    with pytest.raises(TypeError):
        is_overheating("caliente")

def test_tipo_invalido_none():
    """None debe lanzar TypeError."""
    with pytest.raises(TypeError):
        is_overheating(None)


