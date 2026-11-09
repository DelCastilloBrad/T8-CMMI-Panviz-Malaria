"""Reglas de aceptación y motivos de rechazo (R02)."""
from datetime import date

REQUERIDOS = ("id_registro", "fecha_notificacion", "establecimiento",
              "evento", "distrito", "edad", "tipo_edad")

def grupo_etario(edad, tipo):
    """G1 0–4; G2 5–14; G3 15–29; G4 30–59; G5 60+ (años equivalentes)."""
    if tipo not in {"A", "M", "D"}:
        raise ValueError("TIPO_EDAD_INVALIDO")
    try:
        valor = int(edad)
    except (TypeError, ValueError) as exc:
        raise ValueError("EDAD_INVALIDA") from exc
    if valor < 0:
        raise ValueError("EDAD_INVALIDA")
    anios = valor if tipo == "A" else valor / (12 if tipo == "M" else 365)
    if anios < 5:
        return "G1"
    if anios < 15:
        return "G2"
    if anios < 30:
        return "G3"
    if anios < 60:
        return "G4"
    return "G5"

def validar(filas):
    """Devuelve aceptados y rechazados con número de fila y motivo estable."""
    aceptados, rechazados, ids = [], [], set()
    for numero, original in filas:
        fila = {clave: (valor.strip() if isinstance(valor, str) else valor)
                for clave, valor in original.items()}
        motivo = None
        for campo in REQUERIDOS:
            if not fila.get(campo):
                motivo = f"CAMPO_VACIO:{campo}"
                break
        if motivo is None and fila["id_registro"] in ids:
            motivo = "DUPLICADO"
        if motivo is None:
            try:
                fecha = date.fromisoformat(fila["fecha_notificacion"])
                # No se aceptan fechas no canónicas, aunque date.fromisoformat sea permisivo.
                if fecha.isoformat() != fila["fecha_notificacion"]:
                    raise ValueError("fecha no canónica")
            except ValueError:
                motivo = "FECHA_INVALIDA"
        if motivo is None:
            try:
                grupo = grupo_etario(fila["edad"], fila["tipo_edad"])
            except ValueError as exc:
                motivo = str(exc)
        if motivo is not None:
            rechazados.append({"fila": numero, "id_registro": fila.get("id_registro", ""),
                               "motivo": motivo})
            continue
        ids.add(fila["id_registro"])
        fila["semana_iso"] = f"{fecha.isocalendar().year}-W{fecha.isocalendar().week:02d}"
        fila["grupo_etario"] = grupo
        aceptados.append(fila)
    return aceptados, rechazados
