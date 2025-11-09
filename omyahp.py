# app.py
# Application Streamlit pour la méthode AHP avec saisie directe de la matrice

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="AHP – Matrice personnalisée", layout="wide")

st.title("📊 Méthode AHP – Saisie directe de la matrice")
st.markdown("Tapez directement votre matrice de comparaison **AHP** (valeurs séparées par espace ou virgule).")

# --- Étape 1 : Nombre de critères ---
n = st.number_input("🧮 Entrez le nombre de critères :", min_value=2, max_value=10, value=3)

criteria_names = [st.text_input(f"Nom du critère {i+1}", f"Critère {i+1}") for i in range(n)]

st.divider()

# --- Étape 2 : Saisie de la matrice ---
st.markdown(f"### 📋 Entrez la matrice de comparaison ({n}×{n})")

example = "\n".join([" ".join(["1" if i == j else "1" for j in range(n)]) for i in range(n)])
matrix_text = st.text_area(
    "Collez votre matrice (chaque ligne séparée par une nouvelle ligne) :",
    value=example,
    height=150
)

# --- Étape 3 : Conversion en matrice numérique ---
try:
    lines = [line.replace(",", " ").split() for line in matrix_text.strip().split("\n")]
    matrix = np.array([[float(x) for x in line] for line in lines])

    if matrix.shape != (n, n):
        st.error(f"⚠️ La matrice doit être de taille {n}x{n}. Vous avez entré {matrix.shape}.")
    else:
        st.success("✅ Matrice correctement lue.")
        st.dataframe(pd.DataFrame(matrix, index=criteria_names, columns=criteria_names).round(4))

        # --- Étape 4 : Calcul AHP ---
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_eigval = np.max(eigvals.real)
        max_eigvec = eigvecs[:, eigvals.real.argmax()].real
        weights = max_eigvec / np.sum(max_eigvec)

        # --- Cohérence ---
        RI_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        CI = (max_eigval - n) / (n - 1)
        RI = RI_values.get(n, 1.49)
        CR = CI / RI if RI != 0 else 0

        # --- Résultats ---
        st.subheader("📈 Résultats AHP")
        result_df = pd.DataFrame({
            "Critère": criteria_names,
            "Poids": weights.round(4)
        }).sort_values(by="Poids", ascending=False)

        st.dataframe(result_df, use_container_width=True)

        st.markdown(f"**λmax** : {max_eigval:.4f}  **CI** : {CI:.4f}  **CR** : {CR:.4f}")
        if CR < 0.1:
            st.success("✅ Matrice cohérente (CR < 0.1).")
        else:
            st.warning("⚠️ Matrice incohérente (CR ≥ 0.1). Revérifiez vos valeurs.")

except Exception as e:
    st.error(f"Erreur lors de la lecture de la matrice : {e}")

st.markdown("---")
st.caption("Développé par Aya 💡 | AHP simplifié avec saisie directe")
