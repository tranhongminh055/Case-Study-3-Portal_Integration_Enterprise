# Enterprise Integration Case Study

## Backend

1. Install Python dependencies:
   ```bash
   cd "d:\Case Study 3\backend"
   python -m pip install -r requirements.txt
   ```
2. Ensure SQL Server and MySQL connection settings are configured via environment variables or `backend/.env`.
    - If frontend is running on `http://localhost:5174`, set:
       ```powershell
       $env:FRONTEND_ORIGIN = "http://localhost:5174"
       ```
    - Or create `backend/.env` with these values (example):
       ```ini
      # SQL Server
      SQLSERVER_SERVER=localhost
      SQLSERVER_DATABASE=HUMAN
      SQLSERVER_UID=sa
      SQLSERVER_PWD=YourStrong!Passw0rd

      # MySQL (local) — payroll DB
      MYSQL_HOST=127.0.0.1
      MYSQL_PORT=3306
      MYSQL_DATABASE=PAYROLL
      MYSQL_USER=root
      MYSQL_PASSWORD=Hieuthi22032005@

       FRONTEND_ORIGIN=http://localhost:5174
       ```
3. Start FastAPI from the project root directory:
   ```bash
   cd "d:\Case Study 3"
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend

1. Install Node dependencies:
   ```bash
   cd "d:\Case Study 3\frontend"
   npm install
   ```
2. Start the app:
   ```bash
   npm run dev
   ```
3. Open the browser at:
   ```bash
   http://localhost:5174/
   ```

If you want to start the frontend from the project root, run:
```bash
npm start
```

## Cypress Testing

1. Install root dev dependencies:
   ```bash
   cd "d:\Case Study 3"
   npm install
   ```
2. Run generated Cypress tests:
   ```bash
   npm run cypress:run
   ```
3. Open the interactive Cypress UI:
   ```bash
   npm run cypress:open
   ```

## Notes

- Test hook endpoints are enabled when `ENABLE_TEST_FAILURE_HOOKS=true`.
- All cross-database synchronization is implemented through the API layer.
- Department and position create/update/delete operations are synchronized to MySQL.

## Troubleshooting — SQL Server connectivity

- If the backend logs show `Could not connect to SQL Server` or `\\.\SQLEXPRESS` issues:
   - Ensure an ODBC driver is installed (recommended: "ODBC Driver 18 for SQL Server" or 17).
   - Confirm the SQL Server instance is running and accessible (e.g., named instance `SQLEXPRESS`).
   - For local Windows Integrated Security, set `USE_TRUSTED_CONNECTION=true` in `backend/.env`.
   - The code now normalizes `.` instance names (e.g. `.\\SQLEXPRESS`) to `localhost\\SQLEXPRESS`.
   - For developer convenience you can enable a local fallback DB by setting `FALLBACK_TO_SQLITE=true` in `backend/.env`.
      When enabled the app will create `dev_sqlserver_fallback.db` if SQL Server cannot be reached.

If problems persist, paste the backend startup logs (the lines showing driver attempts and errors) and I'll help diagnose further.
