

---

# ✨🎌 Anime Recommendation System - Complete MLOps Project 🚀

---

Welcome to the **Anime Recommendation System** powered by a **full MLOps pipeline**! 🎯
This project showcases how to **build**, **deploy**, **monitor**, **retrain**, and **continuously update** a Machine Learning model using modern MLOps tools like **Docker**, **Airflow**, **DVC**, and **MLflow** — with a beautiful **Streamlit Frontend**! 🎨⚙️

---

## 📚 Table of Contents

* [🚀 Project Overview](#-project-overview)
* [🛠️ Tools and Tech Stack](#-tools-and-tech-stack)
* [📦 Project Structure](#-project-structure)
* [🛠️ Setting Up Locally](#-setting-up-locally)
* [✨ Adding New Anime via Frontend](#-adding-new-anime-via-frontend)
* [🔎 Adding Anime Manually (Advanced)](#-adding-anime-manually-advanced)
* [🌀 Continuous Integration (CI)](#-continuous-integration-ci)
* [📈 Architecture Overview](#-architecture-overview)
* [👨‍💻 About Me](#-about-me)

---

## 🚀 Project Overview

This is a **personalized Anime Recommendation System** 🎎 — with full **MLOps capabilities**:

* 🌀 ETL Pipeline using Airflow
* 📦 Data and Model Versioning with DVC
* 📈 Monitoring via MLflow
* 🐳 Deployment via Docker Compose
* 🎨 Interactive Frontend built with Streamlit
* 🔁 Retraining Pipelines
* 🎯 CI/CD Integration

---

## 🛠️ Tools and Tech Stack

| Tool/Tech         | Purpose                                   |
| ----------------- | ----------------------------------------- |
| 🐳 Docker         | Containerization                          |
| 🛫 Apache Airflow | ETL Scheduling, Retraining Pipelines      |
| 📦 DVC            | Data and Model Versioning                 |
| 📈 MLflow         | Experiment Tracking, Model Monitoring     |
| 🐍 Python         | Core Programming Language                 |
| 🗃️ SQLite3       | Storing User Inputs and Preprocessed Data |
| 🌐 FastAPI        | Backend API                               |
| 🎨 Streamlit      | Frontend Web App                          |
| 🧼 GitHub Actions | Continuous Integration                    |

---

## 📦 Project Structure

```
Recommendatuon_System_MLOPS/
│
├── airflow/                      # Airflow DAGs for ETL, Retraining
├── backend/                      # FastAPI backend APIs
│   └── database/                 # SQLite databases
├── data/                         # Raw and processed datasets
├── frontend/                     # Streamlit Frontend application
├── monitoring/                   # MLflow and Monitoring setup
├── .dvc/                         # DVC tracking files
├── docker-compose.yml            # Docker Compose Setup
├── README.md                     # (this file!)
└── requirements.txt              # Project dependencies
```

---

## 🛠️ Setting Up Locally

Clone the repository first:

```bash
git clone https://github.com/Anurag-raj03/Recommendatuon_System_MLOPS.git
cd Recommendatuon_System_MLOPS
```

Make sure you have **Docker** installed! 🐳

Then start the whole system:

```bash
docker compose up --build
```

This will automatically:

* Spin up Airflow (Scheduler, Webserver)
* Spin up FastAPI Backend
* Spin up MLflow Server
* Start Streamlit Frontend
* Start Monitoring

✨ Everything is ready with one single command!

---

## ✨ Adding New Anime via Frontend (Streamlit UI)

If the Anime you search for is **NOT found** in recommendations —
you can **add it directly via the Streamlit UI**! 🎨

### 🔥 Flow:

1. Search for an Anime in the app.
2. If Anime is not found, a **Form** appears automatically.
3. Fill Anime details (Name, Genre, Rating, MAL ID, etc.).
4. When you **submit**:

   * The data is first stored into **`anime_dat.db`** (Raw User Database).
   * **Airflow pipeline** is automatically triggered.
   * **ETL process** runs and **preprocesses** the new Anime data.
   * Then stored into **`anime_preprocessed_dat.db`** (Processed Database).
5. The new Anime becomes available for Recommendation within minutes! 🚀

### 🗃️ Two SQLite Databases:

| Database                    | Purpose                                |
| --------------------------- | -------------------------------------- |
| `anime_dat.db`              | Stores User Input directly             |
| `anime_preprocessed_dat.db` | Stores Preprocessed Cleaned Anime Data |

---

## 🔎 Adding Anime Manually (Advanced)

If you want to add Anime directly **Always use MYANIMELIST DATA with anime ID IN THE BELOW EXAMPLE**

### ✨ Steps:

1. Visit [MyAnimeList.net](https://myanimelist.net/).
2. Search the Anime (Example: [Grand Blue Dream](https://myanimelist.net/anime/37105)).

```bash
data/processed/anime_dataset.csv
```

Manually add a **new row** with Anime details.

4. Run the following DVC commands:

```bash
dvc add data/processed/anime_dataset.csv
git add data/processed/anime_dataset.csv.dvc
git commit -m "Added new anime: Grand Blue Dream"
git push origin main
dvc push
```

✅ Done! Your dataset is now version-controlled and pushed to remote storage.

---

## 🌀 Continuous Integration (CI)

Every push triggers the CI Pipeline:

* Build Docker Images
* Validate MLOps Stack Health
* Auto Push Images
* Run Pre-deployment Tests

🎯 Fully automated deployment setup via GitHub Actions!

---

## 📈 Architecture Overview

```
                +----------------------------+
                |       Streamlit App         |
                |  (Anime Search & Add Form)   |
                +--------------+--------------+
                               |
                               v
                +----------------------------+
                |       FastAPI Backend       |
                | (Search + Add Anime API)     |
                +------+---------------+------+
                       |               |
              +--------v----+    +------v--------+
              | anime_dat.db |    | anime_preprocessed_dat.db |
              +-------------+    +----------------+
                       |               ^
                       v               |
             +----------------------------+
             |         Airflow DAGs         |
             | (ETL + Transform + Load)     |
             +-----------------------------+
                       |
                       v
                +----------------------------+
                |         MLflow Server       |
                |  (Monitoring & Experiments) |
                +----------------------------+
```

---

## 👨‍💻 About Me

* 💼 **LinkedIn:** [Anurag Raj](https://www.linkedin.com/in/anurag-raj-770b6524a)
* 📊 **Kaggle:** [Anurag's Kaggle Projects](https://www.kaggle.com/anuragraj03/code)
* 📬 **Gmail:** [anuragraj4483@gmail.com](mailto:anuragraj4483@gmail.com)
* 🐳 **DockerHub:** [Anime MLOps Docker Images](https://hub.docker.com/repository/docker/anuragraj03/mlops_recommendation/tags)

---

# 🌟 Thank You for Visiting! 🌟

If you like the project, **star** the repo ⭐ and **connect** with me!
Happy Recommending! 🚀🎎✨

---


