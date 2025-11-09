# app.py
# --- Application Streamlit pour la méthode AHP ---
# Instructions :
# 1️⃣ Crée un dépôt GitHub avec ce fichier.
# 2️⃣ Va sur https://share.streamlit.io -> Connecte ton GitHub -> choisis ton dépôt.
# 3️⃣ L'application sera hébergée automatiquement.

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Méthode AHP - Comparaison Personnalisée", layout="wide")

st.title("📊 Méthode AHP – Matrice de comparaison personnalisée")
st.markdown("Cette application calcule les poids des critères selon la méthode **AHP (Analytic Hierarchy Process)**.")

# --- Étape 1 : Nombre de critères ---
n = st.number_input("🧮 Entrez le nombre de critères :", min_value=2, max_value=10, value=3)

criteria_names = [f"Critère {i+1}" for i in range(n)]
st.write("### 🔤 Noms des critères")
criteria_names = [st.text_input(f"Nom du critère {i+1}", value=criteria_names[i]) for i in range(n)]

st.divider()

# --- Étape 2 : Matrice de comparaison pair à pair ---
st.write("### 📋 Entrez la matrice de comparaison AHP")

default_matrix = np.ones((n, n))

# Création d’un tableau interactif
matrix = []
for i in range(n):
    row = []
    for j in range(n):
        if i == j:
            val = 1.0
        elif i < j:
            val = st.number_input(f"Importance de **{criteria_names[i]}** par rapport à **{criteria_names[j]}**", 
                                   min_value=1/9.0, max_value=9.0, value=1.0, step=0.1, key=f"{i}-{j}")
        else:
            val = 1 / matrix[j][i] if j < i else 1.0
        row.append(val)
    matrix.append(row)

matrix = np.array(matrix)
st.write("#### 🧩 Matrice de comparaison :")
st.dataframe(pd.DataFrame(matrix, index=criteria_names, columns=criteria_names).round(3))

# --- Étape 3 : Calcul des poids AHP ---
eigvals, eigvecs = np.linalg.eig(matrix)
max_eigval = np.max(eigvals.real)
max_eigvec = eigvecs[:, eigvals.real.argmax()].real
weights = max_eigvec / np.sum(max_eigvec)

# --- Étape 4 : Vérification de la cohérence ---
RI_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
CI = (max_eigval - n) / (n - 1)
RI = RI_values.get(n, 1.49)
CR = CI / RI if RI != 0 else 0

st.divider()

# --- Résultats ---
st.subheader("📈 Résultats AHP")
result_df = pd.DataFrame({
    "Critère": criteria_names,
    "Poids": weights.round(4)
}).sort_values(by="Poids", ascending=False)

st.dataframe(result_df, use_container_width=True)

st.markdown(f"**Valeur propre maximale (λmax)** : {max_eigval:.4f}")
st.markdown(f"**Indice de cohérence (CI)** : {CI:.4f}")
st.markdown(f"**Taux de cohérence (CR)** : {CR:.4f}")

if CR < 0.1:
    st.success("✅ La matrice est cohérente (CR < 0.1).")
else:
    st.error("⚠️ La matrice est incohérente (CR ≥ 0.1). Revérifiez vos comparaisons.")

st.markdown("---")
st.caption("Développé par Aya 💡 | AHP en Streamlit")

