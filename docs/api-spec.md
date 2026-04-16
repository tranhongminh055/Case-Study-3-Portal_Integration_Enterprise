# API Specification for Enterprise Integration

## Overview
Backend API integrates two enterprise systems:
- SQL Server: HUMAN_2025 (master HR data)
- MySQL: payroll (salary, attendance, replicated employee data)

## Endpoints

### Employees
- `GET /employees`
- `GET /employees/{id}`
- `POST /employees`
- `PUT /employees/{id}`
- `DELETE /employees/{id}`

### Departments
- `GET /departments`
- `GET /departments/{id}`
- `POST /departments`
- `PUT /departments/{id}`
- `DELETE /departments/{id}`

### Positions
- `GET /positions`
- `GET /positions/{id}`
- `POST /positions`
- `PUT /positions/{id}`
- `DELETE /positions/{id}`

### Payroll
- `GET /salaries`
- `GET /attendance`

### Reports
- `GET /reports`

### Alerts
- `GET /alerts`

## Transaction behavior
For create/update operations affecting both databases:
1. Begin transaction across SQL Server and MySQL.
2. Write changes to SQL Server first.
3. Write changes to MySQL second.
4. Commit only if both sides succeed.
5. Roll back both sides when any error occurs.

## Error Handling
- `200` / `201`: success
- `400`: bad request
- `404`: not found
- `409`: conflict
- `500`: internal or transaction failure

## Test hooks (optional)
When `ENABLE_TEST_FAILURE_HOOKS=true`, test endpoints are available under `/testing` to validate rollback and replication.
