import pandas as pd
import matplotlib.pyplot as plt

df_ventas = pd.read_excel("proyecto1.xlsx")
df_sucursales = pd.read_excel("Catalogo_sucursal.xlsx")

df_ventas["B_mes"] = pd.to_datetime(df_ventas["B_mes"])

total_ventas = df_ventas["ventas_tot"].sum()
print(f"Ventas totales del comercio: ${total_ventas:,.2f}")

clientes_adeudo = df_ventas.groupby("B_adeudo")["no_clientes"].sum()
total_clientes = clientes_adeudo.sum()
porcentaje_adeudo = (clientes_adeudo / total_clientes) * 100
print("\nSocios con y sin adeudo:")
print(clientes_adeudo)
print("Porcentajes:")
print(porcentaje_adeudo.round(2))

ventas_por_periodo = df_ventas.groupby(df_ventas["B_mes"].dt.to_period("M"))["ventas_tot"].sum()
ventas_por_periodo.index = ventas_por_periodo.index.to_timestamp()

plt.figure(figsize=(12, 6))
ventas_por_periodo.plot(kind="bar")
plt.title("Ventas Totales por Mes")
plt.xlabel("Mes")
plt.ylabel("Ventas Totales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

std_pagos_por_mes = df_ventas.groupby(df_ventas["B_mes"].dt.to_period("M"))["pagos_tot"].std()
std_pagos_por_mes.index = std_pagos_por_mes.index.to_timestamp()

plt.figure(figsize=(12, 6))
std_pagos_por_mes.plot(marker='o')
plt.title("Desviación Estándar de Pagos por Mes")
plt.xlabel("Mes")
plt.ylabel("Desviación Estándar")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

deuda_global = df_ventas["adeudo_actual"].sum()
print(f"\nDeuda total de los clientes: ${deuda_global:,.2f}")

utilidad_global = total_ventas - deuda_global
porc_utilidad_global = (utilidad_global / total_ventas) * 100
print(f"Utilidad total: ${utilidad_global:,.2f} ({porc_utilidad_global:.2f}%)")

df_ventas_sucursales = df_ventas.merge(df_sucursales, on="id_sucursal")
ventas_por_suc = df_ventas_sucursales.groupby("suc")["ventas_tot"].sum()

plt.figure(figsize=(8, 8))
ventas_por_suc.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Distribución de Ventas por Sucursal")
plt.ylabel("")
plt.tight_layout()
plt.show()

deuda_suc = df_ventas_sucursales.groupby("suc")["adeudo_actual"].sum()
utilidad_suc = ventas_por_suc - deuda_suc

df_comparativo = pd.DataFrame({
    "Deuda Total": deuda_suc,
    "Utilidad": utilidad_suc
})

df_comparativo.plot(kind="bar", figsize=(12, 6))
plt.title("Deuda Total vs Utilidad por Sucursal")
plt.xlabel("Sucursal")
plt.ylabel("Monto ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
