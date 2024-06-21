# DBMS-final

NCCUCS 24SS DBMS final project

Project Member

* 112356007 鄭群霓
* 112753136 黃賀軍
* 111352027 鄧昱辰
* 112258005 鄭紹群
* 112753131 王聖安
* 112753123 徐浩洋

## Dataset

[Bikestore dataset](https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database/data?select=products.csv)

## Project Description

[Project description pdf file](https://drive.google.com/file/d/1IpZ-BegQSO7tb2QejDUOQeI0xI5H6CnF/view?usp=sharing)

## Final Report & Slides

- [Final report pdf file](https://drive.google.com/file/d/1Txs6O0NBaDtkAHZjLC5yF_eEYu9ze8GW/view?usp=sharing)
- [Final slides pdf file](https://drive.google.com/file/d/1Kh4aXQiPYj2qCg2EKAl2d72PkHMlHqkE/view?usp=sharing)

## System Architecture

```{.bash}
root/
├── README.md
├── bike.db
├── sql/
│   └── schema.sql
├── er model+schema/
│   ├── ER model.png
│   └── relational schema_bike.png
├── frontend/
│   ├── .gitignore
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/
│   │   ├── js/
│   │   │   ├── script.js
│   │   │   └── chart.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── crud.html
│   │   ├── dashboard.html
│   │   └── ...
├── backend/
│   ├── query.py
│   ├── import.py
│   └── ...
└── data/
```

## Main Features

### CRUD

We provide a simple CRUD interface for
the user to interact with the database.

### Dashboard

We build a dashboard to monitor the orders with different categories and brands.
