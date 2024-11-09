# DNA mutant detection API

This program provides an API to detect whether a given DNA sequence belongs to a mutant or not and tracks statistics for the count verified sequences for mutants and non-mutants.

## Features

- *Detects mutant DNA based on a sequence of identical characters (A, T, C, G) horizontally, vertically, or diagonally.*
- *Stores verified DNA sequences in a PostgreSQL database.*
- *Exposes a `/mutant/` endpoint to check if a DNA sequence is mutant.*
- *Exposes a `/stats/` endpoint to fetch statistics on mutant DNA verification.*

## Requirements

- *Python 3.7+*
- *PostgreSQL (Render will provide the database)*
- *Flask*
- *SQLAlchemy*
- *psycopg2*

## Setup instructions

### 1. Clone the repository

```bash
git clone https://github.com/nicoPuegher/mutant_api.git
cd dna-mutant-api
```

### 2. Install Dependencies

Create a virtual environment and install the required dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip3 install -r requirements.txt
```

### 3. Set up environment variables

You will need to set the database `URL` for the **PostgreSQL** instance. You can either use an `.env` file or manually set the environment variable. For local development, **Render** provides a **PostgreSQL** database `URL` that you can use.

Example of how to set the database `URL` locally:
```bash
export DATABASE_URL="postgres://username:password@hostname:5432/database_name?sslmode=require"
```

### 4. Database setup

Once the environment variable is set, initialize the database by running:
```bash
python3 -m db.database
```

### 5. Running the API

Run the **Flask** development server locally:
```bash
flask run
```
This will start the **API** server locally at `http://127.0.0.1:5000`.

### 6. Deploying to Render (optional)

If you want to deploy the **API** to **Render**, follow the instructions below:

- Push your repository to **GitHub**.
- Create a new **Web Service** on **Render**.
- Connect your **GitHub** repository to **Render**.
- Set the environment variable `DATABASE_URL` with the correct **PostgreSQL** connection string from **Render**.
- **Render** will automatically install the dependencies and run the app for you.

### 7. Accessing the API

Once the application is running, you can access the endpoints:

- **POST** `/mutant/` - Submit a DNA sequence to check if it is mutant.
- **GET** `/stats/` - Get statistics of mutants and non-mutants count.

#### POST request (mutant DNA) - Expected: `200 OK`

```bash
curl -X POST https://mutant-api-3z9f.onrender.com/mutant/ \
-H "Content-Type: application/json" \
-d '{
    "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
}'
```
This should return an **HTTP** `200 OK` response.

Response:
```json
{
    "status":"Mutant detected"
}
```

#### POST request (human DNA) - Expected: `403 Forbidden`

```bash
curl -X POST https://mutant-api-3z9f.onrender.com/mutant/ \
  -H "Content-Type: application/json" \
  -d '{"dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGAAGG", "CCGCTA", "TCACTG"]}'
```
This should return an **HTTP** `403 Forbidden` response.

Response:
```json
{
    "status":"Not a mutant"
}
```

#### A bad request - Expected: `400 Bad Request`

```bash
curl -X POST https://mutant-api-3z9f.onrender.com/mutant/ \
  -H "Content-Type: application/json" \
  -d '{"dna": "ATGCGA, CAGTGC, TTATGT"}'
```
This should return an **HTTP** `404 Bad Request` response.

Response:
```json
{
    "error":"Invalid DNA format"
}
```

#### GET request (stats)

```bash
curl -X GET https://mutant-api-3z9f.onrender.com/stats
```

Response:
```json
{
    "count_human_dna":1,
    "count_mutant_dna":2,
    "ratio":2.0
}
```

#### Summary of expected responses

- **POST** `/mutant/` (mutant DNA): **HTTP** `200 OK`
- **POST** `/mutant/` (human DNA): **HTTP** `403 Forbidden`
- **POST** `/mutant/ `(invalid data): **HTTP** `400 Bad Request`
- **GET** `/stats/`: **JSON** with the DNA statistics

#### Troubleshooting

- **Logs:** If you encounter any issues, check the logs in your **Render** dashboard for any errors.
- **Database check:** You can also verify if the records are being correctly saved by querying the database through a direct **SQL** connection or checking the app logs for any **SQL** errors.

## Notes

Remember to replace `mutant-api-3z9f.onrender.com` with the actual `URL` of your **Render** deployment.
