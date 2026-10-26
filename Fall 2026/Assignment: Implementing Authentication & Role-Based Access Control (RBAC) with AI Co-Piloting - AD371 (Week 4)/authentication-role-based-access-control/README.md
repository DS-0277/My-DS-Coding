# Authentication and RBAC Starter

Educational Node.js and Express starter for authentication and role-based access control.

## Initial security decisions

- Passwords are stored as bcrypt hashes.
- New public registrations always receive the `User` role.
- Authentication and Admin authorization are enforced on the server.
- Login failures use a generic message.
- Password hashes are not returned in API responses.
- The session secret is loaded from an environment variable.

## Planned next work

The implementation has completed the initial audit and local QA checks. Review the AI prompt and audit history in `prompt-log.md`.

## QA test summary

| Test | Result | Observed behavior |
|---|---|---|
| Public endpoint | PASS | `GET /` returned 200 |
| Protected endpoint while logged out | PASS | `GET /dashboard` returned 401 |
| New User registration | PASS | `POST /register` returned 201 and assigned `User` |
| Invalid login | PASS | Returned 401 with a generic error |
| User login | PASS | Returned 200 and created a session |
| User dashboard | PASS | Returned 200 for the authenticated User |
| User attempts Admin endpoint | PASS | Returned 403 |
| Logout | PASS | Returned 200 and destroyed the session |
| Admin login | PASS | Controlled Admin account returned 200 |
| Admin endpoint | PASS | Returned 200 for the Admin role |
| Invalid registration input | PASS | Returned 400 |

The browser DevTools Network and Console checks should also be performed manually for the recorded walkthrough. The dependency installation reported three npm audit vulnerabilities; those should be reviewed before public deployment.
