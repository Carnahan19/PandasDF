import requests
import hashlib
import pandas as pd
import sqlite3
import json
import time

def recibirDatosAPI():
    url = "https://restcountries.com/v3.1/all"
    resp = requests.get(url)
    paises = resp.json()
    datos = []

    for pais in paises:
        region = pais.get("region", "N/A")
        nombreP = pais.get("name", {}).get("common", "N/A")
        lenguages = pais.get("languages", {})
        for language_code, lengua in lenguages.items():
            tiempoI = time.perf_counter()
            lenguaHash = hashlib.sha1(lengua.encode()).hexdigest()
            tiempoF = time.perf_counter()
            tiempoProcesado = (tiempoF - tiempoI) * 1000
            datos.append([region, nombreP, lenguaHash, f"{tiempoProcesado:.2f} ms"])
    
    df = pd.DataFrame(datos, columns=["Region", "Ciudad", "Lengua", "Tiempo"])
    return df

def calcularEstadísitcas(df):
    df["Tiempo"] = df["Tiempo"].str.replace(" ms", "").astype(float)
    tiempoT = df["Tiempo"].sum()
    tiempoP = df["Tiempo"].mean()
    tiempoMin = df["Tiempo"].min()
    tiempoMax = df["Tiempo"].max()
    return tiempoT, tiempoP, tiempoMin, tiempoMax


def guardarSQL(df, db_name="paises.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("paises", conn, if_exists="replace", index=False)
    conn.close()
def guardarJSON(df, json_file="info.json"):
    df.to_json(json_file, orient="records", indent=4)

def main():
    df = recibirDatosAPI()
    tiempoT, tiempoP, tiempoMin, tiempoMax = calcularEstadísitcas(df)
    
    # Imprimir el DataFrame como tabla en la terminal
    print(df.to_string(index=False))
    guardarSQL(df)
    guardarJSON(df)

if __name__ == "__main__":
    main()
