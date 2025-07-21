# AKTA Chromatogram Viewer (Google Colab)

This project provides an interactive Google Colab interface for visualizing chromatograms from AKTA systems. It supports `.zip`, `.res`, and `.result` files exported from UNICORN software and allows fine control over:

- UV absorbance display (280 and 260 nm)
- Fraction markers and labeling
- Secondary Y-axis selection (e.g., conductivity, pH, etc.)
- Axis limits and font sizes

The app is built upon [proteovis](https://github.com/Tsuchihashi-ryo/proteovis), a fork of [PyCORN](https://github.com/pyahmed/PyCORN), and is designed for easy usage in a cloud environment.

---

## 📘 How to Use

1. Click the "Open in Colab" badge below to launch the notebook.
2. Upload your `.zip`, `.res`, or `.result` file when prompted.
3. Use the interactive sliders and controls to adjust the chromatogram view.
4. Optionally select a secondary Y-axis parameter (e.g., conductivity or pH).
5. Analyze or export the resulting plots as needed.

---

## ▶️ Launch in Colab

Click the badge below to open the app directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/josocjo/Colab-akta-chromatogram-viewer/blob/master/interactive_chromatogram_viewer.ipynb)

---

## 🔗 Acknowledgements

- **[PyCORN](https://github.com/pyahmed/PyCORN)** – Python Chromatogram Reader by [@pyahmed](https://github.com/pyahmed)
- **[proteovis](https://github.com/Tsuchihashi-ryo/proteovis)** – Interactive visualization fork by [@Tsuchihashi-ryo](https://github.com/Tsuchihashi-ryo)

---


## 📝 License

This project is distributed under the **GNU General Public License v2.0 (GPL-2.0)**.

It is based on:
- [`PyCORN`](https://github.com/pyahmed/PyCORN) by [@pyahmed](https://github.com/pyahmed), licensed under GPL-2.0
- [`proteovis`](https://github.com/Tsuchihashi-ryo/proteovis), a fork of PyCORN

As a derivative work, this Colab app inherits the GPL-2.0 obligations. You are free to use, modify, and redistribute this project under the same license.

