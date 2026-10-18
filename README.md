<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="./assets/profile-cover-mobile.svg" />
    <img src="./assets/profile-cover.svg" width="100%" alt="Pruthvi Raj Pudi — Data Analytics &amp; Data Engineering. From raw data to reliable decisions." />
  </picture>
</p>

<p align="center">
  <a href="#selected-work">Selected work</a> &nbsp; / &nbsp;
  <a href="#toolkit">Toolkit</a> &nbsp; / &nbsp;
  <a href="./assets/PruthviRajPudiResume.pdf">Résumé</a> &nbsp; / &nbsp;
  <a href="https://www.linkedin.com/in/pruthvirajpudi/">LinkedIn</a> &nbsp; / &nbsp;
  <a href="mailto:pruthvirajpudi@gmail.com">Email</a>
</p>

# Hi, I'm Pruthvi.

I build the data foundations behind useful analysis, from ingestion and warehouse models to dashboards and business reporting.

My background includes **3+ years in operations at Amazon and Accenture**, working with SLA tracking, case management, and data quality auditing. That experience shapes the questions I bring to data: where did it come from, can we trust it, and what decision does it support?

**M.S. Data Science, Pace University** · GPA 3.79

**Open to opportunities in data analytics and data engineering.**

---

## Selected work

### 01 / Olist Marketplace Data Pipeline

**Data engineering · E-commerce operations · In development**

Building a cloud data pipeline to investigate fulfillment, seller performance, and customer experience using Olist's Brazilian e-commerce dataset.

**Python → Azure Blob Storage → Snowflake → dbt**

- Implemented extraction and upload code, warehouse loading SQL, and **10 dbt staging models** with explicit grains for orders, items, payments, reviews, and related entities.
- Defined model grains and data checks for uniqueness, required fields, accepted values, and relationships.
- Added a **Groq review-translation prototype** that writes an English-enriched sample separately from the original reviews.

**Next:** validate warehouse execution, build business reporting models, and publish a dashboard.

[Explore the pipeline →](https://github.com/pruthviiraj/olist-marketplace-pipeline)

---

### 02 / Sales & Financial Performance

**Data analytics · AtliQ Hardwares · Excel reporting**

Connecting sales growth, market targets, and profitability through **8 reports** spanning customer, product, market, and P&L analysis.

- Prepared data with Power Query, built relationships in Power Pivot, and created a fiscal calendar and DAX calculations.
- Reported a **$54.9M sales target gap** in 2021 and declining gross margin across the analyzed period.
- Published report PDFs so the findings can be inspected alongside the project write-up.

<sub>Excel &nbsp; · &nbsp; Power Query &nbsp; · &nbsp; Power Pivot &nbsp; · &nbsp; DAX</sub>

[Explore the analysis →](https://github.com/pruthviiraj/Excel-Projects/tree/main/Sales%20%26%20Financial%20Performance%20Analysis)

---

### 03 / CRM & ERP Sales Data Warehouse

**Data engineering · SQL Server · Dimensional modeling**

Turning separate CRM and ERP source files into a structured foundation for sales analysis.

- Built **Bronze → Silver → Gold** layers with T-SQL ingestion and transformation procedures.
- Modeled customer and product dimensions with a sales fact table for analytical queries.
- Included data quality SQL, architecture diagrams, and a Gold-layer data catalog.

<sub>SQL Server &nbsp; · &nbsp; T-SQL &nbsp; · &nbsp; ETL &nbsp; · &nbsp; Star schema</sub>

[Explore the warehouse →](https://github.com/pruthviiraj/crm-and-erp-sales-data-warehouse-project)

---

### 04 / HR Analytics Dashboard

**Data analytics · Atlas Labs · Power BI**

A **4-page dashboard** exploring a sample dataset of **1,470 employees**, with views of workforce composition, attrition, and employee performance.

- Built a star schema with **5 tables and 16 DAX measures**.
- Highlighted **16.1% attrition** and compared patterns across roles and overtime groups.

<sub>Power BI &nbsp; · &nbsp; DAX &nbsp; · &nbsp; Data modeling &nbsp; · &nbsp; Dashboard design</sub>

[View the interactive dashboard →](https://app.powerbi.com/view?r=eyJrIjoiMmQxMTk5YTktNzg4Yy00N2VkLTk5MDItNjg1MjU0NDIzMzliIiwidCI6ImIyN2RhZWIzLThjZmUtNDFiNi1iYTNhLWY1MzRhNGMzN2ZhNCJ9)

<sub>Portfolio projects use public or sample datasets. Findings describe those datasets.</sub>

---

## Toolkit

| Area | Tools & practices |
| :--- | :--- |
| **Analytics & reporting** | SQL · Power BI · Excel · DAX · Power Query · Power Pivot · Looker Studio |
| **Pipelines & transformation** | Python · pandas · dbt · ETL · Azure Blob Storage |
| **Warehousing & modeling** | Snowflake · SQL Server · T-SQL · PostgreSQL · Star schemas · Medallion architecture |
| **Quality & workflow** | Data profiling · dbt tests · Git · GitHub · Data documentation |

## Building next

I'm extending the Olist pipeline from staging into documented reporting models, with attention to model grain, join accuracy, and data quality before dashboarding.

Alongside project work, I document SQL practice and analytical concepts in [my learning log](https://github.com/pruthviiraj/my-learnings).

---

<p align="center">
  <strong>Good decisions start with data you can trust.</strong><br />
  Let's talk about analytics, data engineering, and the business problems behind them.
</p>

<p align="center">
  <a href="mailto:pruthvirajpudi@gmail.com">Get in touch</a> &nbsp; / &nbsp;
  <a href="https://www.linkedin.com/in/pruthvirajpudi/">Connect on LinkedIn</a> &nbsp; / &nbsp;
  <a href="https://github.com/pruthviiraj?tab=repositories">All repositories</a>
</p>
