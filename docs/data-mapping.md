# Data Mapping Documentation

## Employee Data
- SQL Server `employees` is the source of truth.
- MySQL replicates employee records in `employees` by the same primary key.
- Fields mapped:
  - `id`
  - `first_name`
  - `last_name`
  - `email`
  - `phone`
  - `hire_date`
  - `department_id`
  - `position_id`
  - `status`

## Department Data
- SQL Server `departments` is master.
- MySQL `departments` receives replicated rows on create/update/delete.
- Fields mapped:
  - `id`
  - `name`
  - `description`

## Position Data
- SQL Server `positions` is master.
- MySQL `positions` receives replicated rows on create/update/delete.
- Fields mapped:
  - `id`
  - `title`
  - `grade`
  - `description`

## Payroll Data
- MySQL `salaries` stores salary history.
- MySQL `attendance` stores attendance and leave.
- Reports combine SQL Server employee and MySQL payroll records via `employee_id`.
