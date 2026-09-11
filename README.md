# OrbitWatch: Space Domain Threat Characterization & Anomaly Detection 🛰️

An applied machine learning pipeline developed in conjunction with **The Data Mine of the Rockies (DMR)** in support of the **U.S. Space Force**. 

OrbitWatch identifies and characterizes anomalous behavioral shifts in Geosynchronous Orbit (GEO) satellites. The system ingests historical Two-Line Element (TLE) datasets, propagates orbital state vectors via SGP4, runs an Isolation Forest ensemble anomaly detector, and aligns detected outliers with **MITRE ATT&CK for Space / SPARTA** matrices to produce actionable threat and risk assessments.

---

## 🛠️ Tech Stack & Methods

* **Languages & Core Libraries:** Python, NumPy, Pandas, Scikit-learn
* **Astrodynamics & Orbital Mechanics:** SGP4 Propagation, TLE Parsing, Orbital Ephemeris Modeling
* **Machine Learning:** Isolation Forest Ensemble Modeling, Multidimensional Anomaly Scoring
* **Threat Frameworks:** SPARTA (Space Attack Research & Tactic Analysis), MITRE ATT&CK for Space

---

## 🔬 System Pipeline Architecture

```plaintext
   +-----------------------+
   |   Raw TLE & Ephemeris |
   +-----------+-----------+
               |
               v
   +-----------------------+
   |  SGP4 Orbit Propagator| ----> Feature Extraction (Semimajor axis,
   +-----------+-----------+       inclination drift, eccentricity delta)
               |
               v
   +-----------------------+
   | Isolation Forest Model| ----> Anomaly Identification & Deviation Outliers
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Threat Scoring Engine | ----> Mapped to MITRE ATT&CK / SPARTA Matrix
   +-----------------------+
