"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    input_path = "files/input/solicitudes_de_credito.csv"
    output_path = "files/output/solicitudes_de_credito.csv"
    os.makedirs("files/output", exist_ok=True)

    df = pd.read_csv(input_path, sep=";", index_col=0)

    str_cols = {
        "sexo": lambda s: s.str.strip().str.lower(),
        "tipo_de_emprendimiento": lambda s: s.str.strip().str.lower(),
        "idea_negocio": lambda s: (
            s.str.strip()
             .str.lower()
             .str.normalize('NFKD')
             .str.encode('ascii', errors='ignore')
             .str.decode('utf-8')
             .str.replace(" ", "", regex=False)
             .str.replace(r"[-._]", "", regex=True)
        ),
        "barrio": lambda s: (
            s.str.lower()
             .str.replace(r"[_|-]", " ", regex=True)
        ),
        "línea_credito": lambda s: (
            s.str.strip()
             .str.lower()
             .str.replace(" ", "", regex=False)
             .str.replace(r"[-._]", "", regex=True)
        ),
    }
    for col, func in str_cols.items():
        if col in df.columns:
            df[col] = func(df[col])

    if "comuna_ciudadano" in df.columns:
        df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
    if "fecha_de_beneficio" in df.columns:
        df["fecha_de_beneficio"] = pd.to_datetime(
            df["fecha_de_beneficio"], dayfirst=True, format="mixed", errors="coerce"
        )
    if "monto_del_credito" in df.columns:
        df["monto_del_credito"] = (
            df["monto_del_credito"]
            .astype(str)
            .str.strip()
            .str.lstrip("$")
            .str.replace(".00", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(int)
        )

    df = df.dropna().drop_duplicates()

    df.to_csv(output_path, index=False, sep=";")
    return df