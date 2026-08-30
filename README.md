# Shopping Comparison — Stage 1 MVP

## What's in here

```
backend/    -> FastAPI + PostgreSQL API
frontend/   -> React (Vite) app: Search page + Compare page
```

## Backend setup

1. Make sure PostgreSQL is installed and running on your machine.
2. Create a database:
   ```
   createdb shopping_comparison
   ```
   (or use pgAdmin / any Postgres GUI to create a database named `shopping_comparison`)

3. Open a terminal in the `backend/` folder:
   ```
   cd backend
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and put in your real Postgres password:
   ```
   cp .env.example .env
   ```
   Edit `.env` and update `DATABASE_URL` with your actual username/password.

6. Insert mock data (creates tables + adds sample mascara listings):
   ```
   python -m app.seed_data
   ```

7. Start the API server:
   ```
   uvicorn app.main:app --reload
   ```
   Visit http://localhost:8000/docs to see the interactive API docs.

## Frontend setup

1. Open a NEW terminal in the `frontend/` folder:
   ```
   cd frontend
   npm install
   ```

2. Start the dev server:
   ```
   npm run dev
   ```
   Visit http://localhost:5173

## Try it out

1. Make sure BOTH backend (port 8000) and frontend (port 5173) are running at the same time, in two separate terminals.
2. On the search page, search "mascara" or "Huda" — you should see the seeded product.
3. Click it to see the Compare page with listings.

## What's next (Stage 2)

Once this is running end-to-end, the next step is building the product
matching pipeline (brand extraction, quantity normalization, variant
detection) so raw_listing rows get automatically linked to matched_product
rows instead of being seeded by hand.
