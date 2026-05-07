UMBRAL_MAX = 80   # °C — temperatura máxima permitida

def is_overheating(temp_c: float) -> bool:
    """
    Evalúa si la temperatura supera el umbral máximo.

    Parámetros:
        temp_c (float): Temperatura en grados Celsius.

    Retorna:
        bool: True si hay sobrecalentamiento, False si es normal.

    Lanza:
        ValueError: Si la temperatura es negativa (error de sensor).
    """
    if not isinstance(temp_c, (int, float)):
        raise TypeError("La temperatura debe ser un número.")
    if temp_c < 0:
        raise ValueError(f"Temperatura inválida ({temp_c}°C): posible falla de sensor.")
    return temp_c > UMBRAL_MAX
