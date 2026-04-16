# Test Plan for Enterprise Integration API

## Objectives
- Verify endpoint behavior across employee, department, position, payroll, reports, and alerts.
- Validate atomic cross-database synchronization.
- Confirm rollback behavior on partial failures.

## Test Scenarios

1. Add employee → success in both DBs.
2. Simulate MySQL failure during employee creation → rollback SQL Server.
3. Delete blocked when salary exists in payroll.
4. Update employee → sync correctly across both DBs.
5. Create department and position → replicate to MySQL.

## Environment Setup
- Backend running at `http://localhost:8000`
- Cypress installed in project root
- Test mode enabled with `ENABLE_TEST_FAILURE_HOOKS=true`

## Execution
- Generate test cases: `npm run cypress:generate`
- Run tests: `npm run cypress:run`
- Open interactive mode: `npm run cypress:open`

## Validation
- All API responses conform to expected status codes.
- No partial updates remain after simulated failures.
- Alerts and reports return combined results from both systems.
