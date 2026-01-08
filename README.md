# 🏡 Boston House Price Predictor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This project is an end-to-end **Machine Learning Web Application** that predicts the market value of real estate in Boston based on various features such as crime rate, number of rooms, and proximity to employment centers.

The application is powered by an **XGBoost Regressor** model which achieved an **R² Score of 0.90**, outperforming Linear Regression and Random Forest models during the experimentation phase. The interface is built using **Streamlit** to provide a user-friendly experience for real-time predictions.

---

## 🚀 Key Features
* **High Accuracy:** Utilizes XGBoost (Extreme Gradient Boosting) for precise price estimation.
* **Interactive Dashboard:** User-friendly interface with sliders and inputs to adjust housing parameters.
* **Real-time Inference:** Instantly calculates price estimates upon button click.
* **Smart Visuals:** Dynamic progress bars indicate if a property is Budget, Mid-Range, or Luxury.
* **Reset Functionality:** One-click reset button to restore default values.

---

## 🛠️ Technologies Used
* **Language:** Python
* **Machine Learning:** XGBoost, Scikit-Learn, Pandas, NumPy
* **Web Framework:** Streamlit
* **Data Visualization:** Matplotlib (for analysis), Streamlit Elements (for UI)
* **IDE:** Jupyter Notebook / VS Code

---

## 📊 Model Performance
We evaluated three different models before finalizing XGBoost. Here is the performance comparison:

| Model | R² Score (Accuracy) | Mean Absolute Error (MAE) |
| :--- | :--- | :--- |
| **XGBoost (Selected)** | **0.9058** | **1.8909** |
| Random Forest | 0.8923 | 2.0395 |
| Linear Regression | 0.6655 | 3.1802 |

**Why XGBoost?**  
XGBoost was selected because it effectively captures non-linear relationships in the data (like the complex relationship between crime rates and property value) and provides the lowest error rate.

---

## ⚙️ How to Run Locally
If you want to run this app on your own machine, follow these steps:

## 1. Clone the Repository
git clone https://github.com/rishh19/Boston-House-Price-Predictor.git
cd Boston-House-Price-Predictor
## 2. Install Dependencies
pip install -r requirements.txt
## 3. Run the App
streamlit run app.py

### Insights from Data

During the analysis, we found the top drivers for house prices are:
**RM (Number of Rooms):** The strongest positive correlation. More rooms = higher price.
**LSTAT (Lower Status Population):** Strong negative correlation. Wealthier neighborhoods have higher prices.
**PTRATIO (Pupil-Teacher Ratio):** Lower ratios (better schools) lead to higher property values.

### 📜 License
This project is open-source and available for educational purposes.
## 📂 Project Structure
```bash
├── House Price Prediction.ipynb   # Jupyter Notebook for Data Cleaning & Training
├── app.py                         # Main Streamlit Application Code
├── house_price_model.pkl          # Serialized (Saved) XGBoost Model
├── Project-House-Price-File.csv   # Original Dataset
├── requirements.txt               # List of dependencies
└── README.md                      # Project Documentation

✨ Built with ❤️ by Rishav Kumar Shrivastava

