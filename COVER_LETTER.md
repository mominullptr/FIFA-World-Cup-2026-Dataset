# Cover Letter for Journal Submission

**Date**: July 26, 2026  
**To**: Editor-in-Chief / Editorial Board  
**Target Journal**: *Scientific Data* (Springer Nature)  

**Subject**: Submission of Data Descriptor Manuscript — *"The FIFA World Cup 2026 Master Dataset: A Normalized 3NF Relational Benchmark of the Expanded 48-Team International Football Tournament"*

Dear Editor-in-Chief,

I am pleased to submit our Data Descriptor manuscript titled **"The FIFA World Cup 2026 Master Dataset: A Normalized 3NF Relational Benchmark of the Expanded 48-Team International Football Tournament"** for consideration as an original Data Article in *Scientific Data*.

### Summary & Dataset Scope
The 2026 FIFA World Cup marked the first tournament in international football to feature 48 participating national teams, expanding the match schedule from 64 to 104 matches across 16 host venues in Canada, Mexico, and the United States. Open sports datasets have become increasingly vital for quantitative analytics, machine learning benchmark evaluation, and reproducible research.

To the best of our knowledge, this dataset represents one of the first open-access, fully normalized 3rd Normal Form (3NF) relational databases capturing the complete 2026 FIFA World Cup tournament. The database includes all 104 matches, 48 qualified national teams, 1,248 registered squad players, 2,704 minute-by-minute lineup records, tactical team statistics, expected goals ($xG$), and pre-engineered predictive feature matrices. Data was harvested continuously across the 39-day tournament (concluding July 19, 2026), normalized into 12 relational tables, and audited using an automated 9-stage programmatic verification suite (100% referential and primary key integrity) alongside an empirical 30-match audit against official FIFA Technical Study Group bulletins (1,498 matching data points out of 1,500 audited, yielding 99.87% empirical accuracy).

### Novelty & Distinction from Existing Resources
Existing public football datasets—such as StatsBomb Open Data, SoccerNet, and historical Kaggle collections—provide valuable research assets. However, they either do not cover the completed 2026 tournament, lack a normalized relational schema, omit stadium geographic elevations, or require extensive preprocessing before machine learning deployment. The present dataset addresses these limitations by providing a fully normalized relational schema (`sqlite_fifa_world_cup_2026.db`, Parquet, CSV) coupled with pre-match predictive feature vectors (`match_prediction_features.csv`) and reproducible open-source processing pipelines.

### Research Impact & Target Audiences
This dataset is designed to support reproducible research across sports analytics, database engineering, statistical modeling, machine learning, and quantitative performance analysis.

### Statements & Author Confirmations
- **Originality**: This manuscript and underlying dataset are original work and have not been published previously, nor are they currently under consideration for publication by any other journal or conference.
- **Data Availability**: The complete dataset is permanently archived and publicly accessible under the Creative Commons CC0 1.0 Universal License via Zenodo (DOI: [`10.5281/zenodo.21592427`](https://doi.org/10.5281/zenodo.21592427)), as well as GitHub and Kaggle repositories.
- **Financial Hardship / APC Waiver Request**: As an independent student researcher from Shahjalal University of Science and Technology (SUST), Bangladesh, operating without institutional research grant funding, I respectfully request a **100% Article Processing Charge (APC) Financial Hardship Waiver** under your journal's open-access equity guidelines.

Thank you very much for your time, consideration, and editorial evaluation of this manuscript.

Sincerely,

**MD Mominul Islam**  
Department of Computer Science and Engineering  
Shahjalal University of Science and Technology (SUST)  
Sylhet 3114, Bangladesh  
**ORCID iD**: [0009-0009-1572-4830](https://orcid.org/0009-0009-1572-4830)  
**Email**: `mominulcse11@gmail.com`  
**Dataset DOI**: `10.5281/zenodo.21592427`  

   