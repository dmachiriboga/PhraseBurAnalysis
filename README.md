# Measuring the Feel: Quantifying Swing as Expressive Microrhythm in Jazz Performance

**Repository for Data Analysis Scripts — Weimar Jazz Database & Benadon’s BUR Theory**

---

## Abstract

*To be added.*

---

## Overview

This repository contains Python scripts and analysis tools for the academic paper:

**"Measuring the Feel: Quantifying Swing as Expressive Microrhythm in Jazz Performance"**

The scripts are designed to analyze phrase-level swing ratio (BUR: Beat Upbeat Ratio) data from the [Weimar Jazz Database](https://jazzomat.hfm-weimar.de/dbformat/dboverview.html), focusing on the theoretical framework and methods described in:

> Benadon, Fernando. "Slicing the Beat: Jazz Eighth-Notes as Expressive Microrhythm." *Ethnomusicology* 53, no. 1 (2009): 73-98. [JSTOR link](https://www.jstor.org/stable/25653079)

---

## Analysis Focus

- **BUR Surge:** Detecting and quantifying significant increases or decreases in BUR within phrases.
- **BUR Variation:** Measuring phrase-level variability in swing ratios.
- **BUR and Phrase Structure:** Using BUR patterns to outline and interpret phrase structure in jazz improvisation.

All scripts are tailored for the Weimar Jazz Database and are intended to support research into expressive microrhythm in jazz, as theorized by Benadon.

---

## What is BUR?

**BUR (Beat Upbeat Ratio)** is a metric introduced by Benadon to quantify the ratio between the durations of downbeats and upbeats in jazz eighth-note pairs, providing a quantitative measure of swing feel and expressive timing.

---

## Data Source

- **Weimar Jazz Database:**  
  [https://jazzomat.hfm-weimar.de/dbformat/dboverview.html](https://jazzomat.hfm-weimar.de/dbformat/dboverview.html)  
  (Hochschule für Musik Franz Liszt Weimar)
- **PhraseBur.csv:** Generated using [melospygui](https://jazzomat.hfm-weimar.de/tools/melospy.html) from the Weimar Jazz Database.

---

## Citations

- Benadon, Fernando. "Slicing the Beat: Jazz Eighth-Notes as Expressive Microrhythm." *Ethnomusicology* 53, no. 1 (2009): 73-98. [JSTOR](https://www.jstor.org/stable/25653079)
- Pfleiderer, Martin, et al. "The Weimar Jazz Database: A User Guide." *Jazzomat Research Project*, Hochschule für Musik Franz Liszt Weimar. [Weimar Jazz Database](https://jazzomat.hfm-weimar.de/dbformat/dboverview.html)

---

## Repository Structure

- `PhraseBurAnalysis/` — All analysis scripts and notebooks
- `PhraseBur.csv` — Main input data file (not included; see Weimar Jazz Database)
- `README.md` — This file

---

## Usage

1. Download the relevant data from the Weimar Jazz Database.
2. Place `PhraseBur.csv` in the repository directory.
3. Run the analysis scripts as needed (see script headers for details).

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
