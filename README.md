
# Project Icarus - Extension



## 📌 Description

<center>
<img src="source/assets/Flight_Data_Analysis_Dashboard.gif" alt="Flight Data Explorer Demo" width="700" align="center"/>
</center>


Project Icarus was originally delivered as a group project for the **Advanced Programming Summer 2024** course at NOVA SBE. However, since Jupyter Notebooks typically are less fun to interact with, I decided to extend the project making the class Streamlit ready and to build a cool Streamlit App based on the FlightData class from the project.

Project Icarus is a Python-based tool for **comprehensive analysis of commercial air travel data**, with a focus on **sustainability**. Built using the IATA dataset, it provides insights into flight patterns, airplane usage, and potential **decarbonization strategies**.

The base implementation of the flight class was extended and wrapped into a streamlit App to showcase more effectively its advanced features. Look at the demo [video](source/assets/Flight_Data_Analysis_Dashboard.webm) in your local browser or inspect the source code in **showcase_app.py** to get a better understanding of how it can be used.

> 📝 Scroll to the bottom for the detailed project outline and grading criteria.


---

## 📚 Project Documentation

Full documentation—including architecture, classes, functions, and examples—can be accessed in the `index.html` file:

📁 `/docs/_build/html/index.html`

Our documentation helps users and developers understand and contribute to Project Icarus more effectively.

---

## 🚀 Usage

### 🛠️ Environment Setup & Showcase Notebook

Follow these steps to set up the environment and run the showcase notebook:

1. **Clone the Repository**

   ```bash
   git clone https://gitlab.com/adpro3080008/group_09
   ```

2. **Navigate to Project Directory**

   ```bash
   cd group_09
   ```

3. **Install Dependencies**

   Create the Conda environment:

   ```bash
   conda env create -f environment.yml
   ```

4. **Activate the Environment**

   ```bash
   conda activate adpro_group09
   ```

5. **Set Up API Key for LLM Features**

   - Define a system variable: `OPENAI_API_KEY`
   - Guides:
     - [Windows](https://support.microsoft.com/pt-pt/topic/how-to-manage-environment-variables-in-windows-xp-5bf6725b-655e-151c-0b55-9a8c9c7f747d)
     - [MacOS](https://phoenixnap.com/kb/set-environment-variable-mac)

6. **Start the Streamlit App in your local browser**

   ```bash
   streamlit run showcase_app.py
   ```

   You should see the following GUI in your browser under http://localhost:8501
---

## 🧪 Unit Tests

We use **pytest** to test the `distance` function located in `source/Functions/distances.py`.

### ✅ Test Scenarios

- **Input Validation**: Raises `TypeError` for non-numeric inputs.
- **Intercontinental Test**: Distance between Düsseldorf and San Diego.
- **Identical Points**: Returns 0 for identical coordinates.

### 🧰 How to Run

```bash
pytest source/Test/test_distances.py
```

---

## 📂 Files

Input files (flight data) are available from GitLab:

[📥 Download flight_data.zip](https://gitlab.com/adpro1/adpro2024/-/raw/main/Files/flight_data.zip?inline=false)

---

## 👥 Authors

| Name                | Student No. | Email                    |
|---------------------|-------------|---------------------------|
| Adam Bernard        | 60865       | 60865@novasbe.pt         |
| Hendrik Künnemann   | 57995       | 57995@novasbe.pt         |
| Moritz Lind         | 61230       | 61230@novasbe.pt         |
| Luc Marc Pellinger  | 58611       | 58611@novasbe.pt         |

---

## 📄 License

Project Icarus is licensed under the **GNU AFFERO GENERAL PUBLIC LICENSE v3**.

Key Permissions:
- ✅ Use (personal, academic, commercial)
- ✅ Modify and redistribute (with source disclosure)
- ✅ Server use must disclose source

🔗 [Full License Details](https://www.gnu.org/licenses/agpl-3.0.en.html)

---

## 📊 Project Status

**Status**: ✅ Completed

---

## 📘 Project Outline & Instructions

> This section follows the project phases and grading rubric.

### Part 1

#### Phase 1: Setup

- [x] Create repository `Group_09`
- [x] Include README, LICENSE, `.gitignore`
- [x] Add all team members with Maintainer access
- [x] Clone repo locally

#### Phase 2: Class Structure

- [x] PEP8 compliant class
- [x] `.py` files in structured folders
- [x] Class downloads dataset into `/downloads`
- [x] Reads CSVs into pandas DataFrames

#### Phase 3: Methods

- [x] `plot_airports_by_country(country)`
- [x] `distance_analysis()`
- [x] `plot_flights_from_airport(airport, internal=False)`
- [x] `top_airplanes_by_country(country=None)`
- [x] `plot_flights_from_country(country, internal=False)`

#### Phase 4: Showcase Notebook

- [x] Tell a compelling story using all methods
- [x] Ensure all cells run start-to-finish
- [x] Keep prototyping notebooks in separate folder

---

### Part 2

#### Phase 1: LLM Integration

- [x] `aircrafts()` – lists all aircraft models
- [x] `aircraft_info(aircraft_name)` – with error handling and markdown table
- [x] `airport_info(airport_name)` – airport info using LLM

#### Phase 2: Decarbonization Case Study

- [x] Modify 5th method with `cutoff_distance`
- [x] Plot split by short-haul and long-haul
- [x] Add annotations: route count and total distance
- [x] Estimate emissions saved with train alternative (source cited in notebook)

#### Phase 3: Final Cleanup

- [x] Add `environment.yml` with all dependencies
- [x] Use **Sphinx** to generate `/docs`
- [x] Update `.gitignore` and README to guide user

---

### Grading Notes

- All tasks are worth **1 point** (except Phase 1: worth 1 point in total).
- Final delivery must contain the showcase notebook, `.py` class file, and clear documentation.
- 🛑 Do **not** use input prompts—only use method arguments!


