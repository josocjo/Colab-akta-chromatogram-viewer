# AKTA Chromatogram Viewer

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/josocjo/akta-chromatogram-viewer/blob/main/viewer.ipynb)

**Interactive Google Colab viewer for AKTA chromatograms**.  
Allows uploading `.zip`, `.res`, or `.result` files from UNICORN systems and visualizing them with dual Y axes, customizable fraction display, and user-controlled signals.

---

## 🚀 Features

- 📁 Upload `.zip`, `.res`, or `.result` files exported from AKTA UNICORN
- 📊 Plot UV absorbance and any secondary signal (e.g., Conc B)
- 🔁 Dual Y axes with customizable ranges
- 🎯 Interactive controls for font sizes, axis limits, and tick labels
- 🧪 Show or hide fractions with spacing, height, and label settings
- 💻 Designed to run entirely in **Google Colab** using `ipywidgets`

---

## 📎 Based on

This project builds upon:

- [`proteovis`](https://github.com/Tsuchihashi-ryo/proteovis) by [@Tsuchihashi-ryo](https://github.com/Tsuchihashi-ryo)
- [`PyCORN`](https://github.com/pyahmed/PyCORN) by [@pyahmed](https://github.com/pyahmed)

Many thanks to both authors for their open-source contributions.  
We maintain all licenses and attributions accordingly.

If you are using this notebook, please consider citing or acknowledging their work.

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
