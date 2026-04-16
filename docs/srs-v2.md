# SRS v2 - Enterprise Integration API

## System Overview
The API serves as an integration layer between HUMAN_2025 (SQL Server) and payroll (MySQL). It exposes REST endpoints for employee lifecycle, department and position management, payroll retrieval, reports, and alerts.

## Functional Requirements
- Read employee master data from SQL Server.
- Synchronize new and updated HR data into payroll MySQL.
- Prevent inconsistent deletion when salary or dividend references exist.
- Build atomic transactions spanning both databases.
- Provide combined reporting and alerting.

## Nonfunctional Requirements
- Use FastAPI and SQLAlchemy.
- Use Axios in frontend with React.
- Log all API calls and transaction events.
- Maintain API-only integration layer.

## Integration Flow
1. Client calls REST endpoint.
2. Backend validates payload.
3. Backend writes SQL Server first.
4. Backend writes MySQL second.
5. Commit both if all operations succeed.
6. Roll back both if any operation fails.
