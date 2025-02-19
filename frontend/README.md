# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

# Vue Router Configuration

This project uses Vue Router to manage navigation between different views. Below is a breakdown of the routes and their respective components.

## Routes Overview
 ------------------------------------------------------------------------------------------------------------------------
| Path           | Name                 | Component File         | Description                                           |
|----------------|----------------------|------------------------|-------------------------------------------------------|
| `/SignIn`      | Sign In              | `SignInView.vue`       | User authentication page for signing in.              |
| `/Dashboard`   | Student Dashboard    | `DashboardView.vue`    | The main dashboard for students to access their info. |
| `/Register`    | Student Registration | `RegistrationView.vue` | Page for students to register an account.             |
| `/Seek`        | Seek Portal          | `SeekPortalView.vue`   | A portal for lecures and assignments.                 |
| `/Agent`       | AI Agent             | `AiAgentView.vue`      | Interface for interacting with the AI agent.          |
| `/Admin`       | Admin Panel          | `AdminView.vue`        | Dashboard for administrators to manage the system.    |
| `/Admin/SignIn`| Admin Sign In        | `AdminSignInView.vue`  | Authentication page for administrators.               |
 ------------------------------------------------------------------------------------------------------------------------
## Lazy Loading
All routes use Vue’s **lazy loading** via dynamic imports to optimize performance. Each route is assigned a Webpack chunk name to enable efficient code splitting.


