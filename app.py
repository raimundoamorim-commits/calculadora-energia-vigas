import sympy as sp
import streamlit as st

# Configuração da página do navegador
st.set_page_config(
    page_title="Calculadora de Energia Estrutural", page_icon="🏗️"
)

st.title("🏗️ Calculadora de Energia de Deformação")
st.write(
    "Calcule a energia interna de deformação em flexão ($U_M$) para vigas planas!"
)

# Seleção do tipo de viga
opcao = st.selectbox(
    "Escolha a configuração da viga:",
    ["Viga em Balanço (Carga P na ponta)", "Viga Bi-apoiada (Carga Uniforme q)"],
)

st.divider()

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

    if st.button("🚀 Calcular Energia", use_container_width=True):
        x = sp.Symbol("x")
        M_x = -P * (L - x)
        integrando = (M_x**2) / (2 * EI)
        U = sp.integrate(integrando, (x, 0, L))

        st.balloons()  # Efeito visual divertido!
        st.success(
            f"**Energia de Deformação Total (U):** `{float(U):.4f} kJ` (ou `{float(U)*1000:.2f} J`)"
        )
        st.info("Fórmula utilizada: $U = \\frac{P^2 L^3}{6EI}$")

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

    if st.button("🚀 Calcular Energia", use_container_width=True):
        x = sp.Symbol("x")
        M_x = (q * L / 2) * x - (q * x**2) / 2
        integrando = (M_x**2) / (2 * EI)
        U = sp.integrate(integrando, (x, 0, L))

        st.balloons()
        st.success(
            f"**Energia de Deformação Total (U):** `{float(U):.4f} kJ` (ou `{float(U)*1000:.2f} J`)"
        )
        st.info("Fórmula utilizada: $U = \\frac{q^2 L^5}{240EI}$")