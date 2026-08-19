import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import sympy as sp

st.set_page_config(
    page_title="Calculadora de Energia Estrutural", page_icon="🏗️"
)

st.title("🏗️ Calculadora de Energia Estrutural")
st.write("Calcule a energia interna de deformação ($U$) e visualize o diagrama!")

# Seleção da Estrutura
opcao = st.selectbox(
    "Escolha o modelo estrutural:",
    [
        "Viga em Balanço (Carga P na ponta)",
        "Viga Bi-apoiada (Carga Uniforme q)",
        "Pórtico em L (Força P na extremidade livre)",
    ],
)

st.divider()

# --- CASO 1: VIGA EM BALANÇO ---
if opcao == "Viga em Balanço (Carga P na ponta)":
    st.subheader("📐 Viga em Balanço")

    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input(
            "Força P (kN):", value=10.0, step=1.0, format="%.2f"
        )
        L = st.number_input(
            "Comprimento L (m):", value=5.0, step=0.5, format="%.2f"
        )
    with col2:
        EI = st.number_input(
            "Rigidez EI (kN.m²):", value=10500.0, step=500.0, format="%.2f"
        )

    if st.button("🚀 Calcular e Gerar Gráfico", use_container_width=True):
        # Cálculo Simbólico
        x = sp.Symbol("x")
        M_x = -P * (L - x)
        integrando = (M_x**2) / (2 * EI)
        U = sp.integrate(integrando, (x, 0, L))

        st.balloons()
        st.success(
            f"**Energia de Deformação Total (U):** `{float(U):.4f} kJ` (ou `{float(U)*1000:.2f} J`)"
        )

        # Gráfico do Momento Fletor
        st.subheader("📈 Diagrama de Momento Fletor M(x)")
        x_vals = np.linspace(0, L, 100)
        M_vals = -P * (L - x_vals)

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(x_vals, M_vals, color="crimson", lw=2)
        ax.axhline(0, color="black", lw=0.8, ls="--")
        ax.fill_between(x_vals, M_vals, color="crimson", alpha=0.2)
        ax.set_xlabel("Posição x (m)")
        ax.set_ylabel("Momento Fletor M(x) [kN.m]")
        ax.grid(True, linestyle=":", alpha=0.6)

        st.pyplot(fig)

# --- CASO 2: VIGA BI-APOIADA ---
elif opcao == "Viga Bi-apoiada (Carga Uniforme q)":
    st.subheader("📐 Viga Bi-apoiada")

    col1, col2 = st.columns(2)
    with col1:
        q = st.number_input(
            "Carga distribuída q (kN/m):",
            value=5.0,
            step=0.5,
            format="%.2f",
        )
        L = st.number_input(
            "Comprimento L (m):", value=6.0, step=0.5, format="%.2f"
        )
    with col2:
        EI = st.number_input(
            "Rigidez EI (kN.m²):", value=10500.0, step=500.0, format="%.2f"
        )

    if st.button("🚀 Calcular e Gerar Gráfico", use_container_width=True):
        x = sp.Symbol("x")
        M_x = (q * L / 2) * x - (q * x**2) / 2
        integrando = (M_x**2) / (2 * EI)
        U = sp.integrate(integrando, (x, 0, L))

        st.balloons()
        st.success(
            f"**Energia de Deformação Total (U):** `{float(U):.4f} kJ` (ou `{float(U)*1000:.2f} J`)"
        )

        # Gráfico do Momento Fletor
        st.subheader("📈 Diagrama de Momento Fletor M(x)")
        x_vals = np.linspace(0, L, 100)
        M_vals = (q * L / 2) * x_vals - (q * x_vals**2) / 2

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(x_vals, M_vals, color="royalblue", lw=2)
        ax.axhline(0, color="black", lw=0.8, ls="--")
        ax.fill_between(x_vals, M_vals, color="royalblue", alpha=0.2)
        ax.set_xlabel("Posição x (m)")
        ax.set_ylabel("Momento Fletor M(x) [kN.m]")
        ax.grid(True, linestyle=":", alpha=0.6)

        st.pyplot(fig)

# --- CASO 3: PÓRTICO EM L ---
elif opcao == "Pórtico em L (Força P na extremidade livre)":
    st.subheader("🏛️ Pórtico Plano em L")
    st.write(
        "Pilar vertical $AB$ (engastado em A) + Viga horizontal $BC$ (força P em C)."
    )

    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input(
            "Força P (kN):", value=10.0, step=1.0, format="%.2f"
        )
        L_viga = st.number_input(
            "Comprimento da Viga L (m):", value=4.0, step=0.5, format="%.2f"
        )
        H_pilar = st.number_input(
            "Altura do Pilar H (m):", value=3.0, step=0.5, format="%.2f"
        )
    with col2:
        EI = st.number_input(
            "Rigidez EI (kN.m²):", value=10500.0, step=500.0, format="%.2f"
        )

    if st.button("🚀 Calcular Energia Total", use_container_width=True):
        x = sp.Symbol("x")

        # 1. Energia da Viga BC: M(x) = -P*x
        U_viga = sp.integrate((-P * x) ** 2 / (2 * EI), (x, 0, L_viga))

        # 2. Energia do Pilar AB: Momento constante transmitido pelo nó B -> M = -P*L_viga
        U_pilar = sp.integrate(
            (-P * L_viga) ** 2 / (2 * EI), (x, 0, H_pilar)
        )

        U_total = U_viga + U_pilar

        st.balloons()
        st.success(
            f"**Energia de Deformação Total (U_total):** `{float(U_total):.4f} kJ`"
        )

        col_a, col_b = st.columns(2)
        col_a.metric("Energia na Viga (U_viga)", f"{float(U_viga):.4f} kJ")
        col_b.metric("Energia no Pilar (U_pilar)", f"{float(U_pilar):.4f} kJ")
   
