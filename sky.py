import streamlit as st
import py3Dmol
from openbabel import pybel
from collections import Counter

st.set_page_config(page_title="Molecular Viewer", layout="centered")

st.title("🧪 Molecular Viewer & Property Calculator")

# 📌 Example compounds
example_smiles = {
    "Ethanol": "CCO",
    "Benzene": "C1=CC=CC=C1",
    "Acetic Acid": "CC(=O)O",
    "Methane": "C",
    "Water": "O",
    "Carbon Dioxide": "O=C=O",
    "Ammonia": "N",
    "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O",
    "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "Caffeine": "Cn1cnc2c1c(=O)n(C)c(=O)n2C"
}

# 🎯 Dropdown
st.subheader("🧪 Select Example Compound")
selected = st.selectbox("Choose a compound:", list(example_smiles.keys()))
smiles = example_smiles[selected]


# 🚀 Process molecule
try:
    mol = pybel.readstring("smi", smiles)

    st.success("✅ Valid molecule!")

    # 📊 Properties
    st.subheader("📊 Basic Properties")
    st.write("Molecular Weight:", round(mol.molwt, 2))
    st.write("Formula:", mol.formula)

    # 🔢 Structure Info
    st.subheader("🔢 Structure Information")
    st.write("Number of Atoms:", mol.OBMol.NumAtoms())
    st.write("Number of Bonds:", mol.OBMol.NumBonds())

    # 🧬 Elements
    st.subheader("🧬 Elements Present")

    elements = [atom.atomicnum for atom in mol]

    periodic_table = {
        1: "H", 6: "C", 7: "N", 8: "O",
        9: "F", 15: "P", 16: "S", 17: "Cl"
    }

    symbols = [periodic_table.get(num, str(num)) for num in elements]
    unique_elements = sorted(set(symbols))

    st.write("Elements:", ", ".join(unique_elements))

    # 🔢 Element Count
    st.subheader("🔢 Element Count")

    element_count = Counter(symbols)

    for element, count in element_count.items():
        st.write(f"{element}: {count}")

    # 📋 Atom Table
    st.subheader("📋 Atom Details")

    atom_data = []
    for atom in mol:
        atom_data.append({
            "Element": periodic_table.get(atom.atomicnum, atom.atomicnum),
            "Atomic Number": atom.atomicnum,
            "Coordinates": tuple(round(x, 2) for x in atom.coords)
        })

    st.write(atom_data)

    # 🔬 3D Structure
    st.subheader("🔬 3D Structure")

    mol.make3D()
    mol.localopt()

    mol_block = mol.write("mol")

    viewer = py3Dmol.view(width=500, height=500)
    viewer.addModel(mol_block, "mol")

    viewer.setStyle({
        "stick": {"radius": 0.2},
        "sphere": {"scale": 0.3}
    })

    viewer.setBackgroundColor("black")
    viewer.zoomTo()
    viewer.spin(True)

    st.components.v1.html(viewer._make_html(), height=500)

except Exception as e:
    st.error(f"❌ Invalid SMILES or Error: {e}")