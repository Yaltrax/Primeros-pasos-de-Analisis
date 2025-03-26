import pandas as pd
import matplotlib.pyplot as plt

ventas_df = pd.read_excel("proyecto1.xlsx")
sucursales_df = pd.read_excel("Catalogo_sucursal.xlsx")

ventas_df["B_mes"] = pd.to_datetime(ventas_df["B_mes"])

ventas_totales = ventas_df["ventas_tot"].sum()
print(f"Ventas totales del comercio: ${ventas_totales:,.2f}")

socios_adeudo = ventas_df.groupby("B_adeudo")["no_clientes"].sum()
total_socios = socios_adeudo.sum()
porcentajes_socios = (socios_adeudo / total_socios) * 100
print("\nSocios con y sin adeudo:")
print(socios_adeudo)
print("Porcentajes:")
print(porcentajes_socios.round(2))

ventas_por_mes = ventas_df.groupby(ventas_df["B_mes"].dt.to_period("M"))["ventas_tot"].sum()
ventas_por_mes.index = ventas_por_mes.index.to_timestamp()
plt.figure(figsize=(12, 6))
ventas_por_mes.plot(kind="bar")
plt.title("Ventas Totales por Mes")
plt.xlabel("Mes")
plt.ylabel("Ventas Totales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

std_pagos_mes = ventas_df.groupby(ventas_df["B_mes"].dt.to_period("M"))["pagos_tot"].std()
std_pagos_mes.index = std_pagos_mes.index.to_timestamp()
plt.figure(figsize=(12, 6))
std_pagos_mes.plot(marker='o')
plt.title("Desviación Estándar de Pagos por Mes")
plt.xlabel("Mes")
plt.ylabel("Desviación Estándar")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

deuda_total = ventas_df["adeudo_actual"].sum()
print(f"\nDeuda total de los clientes: ${deuda_total:,.2f}")

utilidad_total = ventas_totales - deuda_total
porcentaje_utilidad = (utilidad_total / ventas_totales) * 100
print(f"Utilidad total: ${utilidad_total:,.2f} ({porcentaje_utilidad:.2f}%)")

ventas_sucursales = ventas_df.merge(sucursales_df, on="id_sucursal")
ventas_por_sucursal = ventas_sucursales.groupby("suc")["ventas_tot"].sum()
plt.figure(figsize=(8, 8))
ventas_por_sucursal.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Distribución de Ventas por Sucursal")
plt.ylabel("")
plt.tight_layout()
plt.show()

deuda_por_sucursal = ventas_sucursales.groupby("suc")["adeudo_actual"].sum()
utilidad_por_sucursal = ventas_por_sucursal - deuda_por_sucursal
comparativo_df = pd.DataFrame({
    "Deuda Total": deuda_por_sucursal,
    "Utilidad": utilidad_por_sucursal
})
comparativo_df.plot(kind="bar", figsize=(12, 6))
plt.title("Deuda Total vs Utilidad por Sucursal")
plt.xlabel("Sucursal")
plt.ylabel("Monto ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
