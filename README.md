# TaxAuto

TaxAuto is a Windows desktop application for tax operations teams that combines three kinds of work in a single local-first workspace:

1. Browser and ERP automation for repetitive fiscal tasks.
2. Data-processing routines that audit and reconcile tax files.
3. Operational utilities and master-data management for companies, branches, and branch groups.

The project is built as an Electron desktop shell that hosts an Angular frontend and boots a local Python FastAPI backend on startup. The backend is responsible for filesystem access, SQLite persistence, pandas-based processing, and Selenium-driven automation.

## Core Idea

The central idea of the application is to remove manual effort from recurring tax workflows without depending on a remote SaaS backend.

Instead of sending accounting files to an external service, TaxAuto runs locally on the operator's machine and:

- orchestrates automations against browser and ERP interfaces;
- stores operational data locally in SQLite;
- creates workspace folders in the user's machine for fiscal periods and generated outputs;
- validates, merges, and audits spreadsheets and tax reports;
- gives the operator a guided UI to execute tasks and inspect results.

This makes the application especially suited to tax teams that work with local files, internal portals, and desktop/browser-based routines.

## Product Areas

The current codebase is organized around these product areas:

- `TaxAuto / Automacao`
  - Generates fiscal books and related outputs through automation flows.
  - Includes automation for cancelled invoice report generation.
- `TaxData`
  - Focuses on local data processing and audit workflows.
  - Currently the strongest implemented flow is the audit of cancelled invoices.
  - There is also a fiscal period/apuracao area with UI and models in place, but parts of that flow are still scaffolded.
- `Utilitarios`
  - Consolidates Excel/CSV files into a unified spreadsheet.
  - Manages companies, branches, and branch groups through CRUD screens.
- `TaxTrack`
  - Dashboard-style module currently backed by mock data, useful as a design and navigation scaffold.

## Architecture

### High-level runtime

```text
Electron main process
  -> starts Python backend
  -> captures backend port
  -> creates desktop window
  -> exposes native IPC APIs to renderer

Angular frontend (renderer)
  -> asks Electron for backend port during app init
  -> calls local FastAPI endpoints via HttpClient
  -> uses IPC for native file/folder dialogs and opening local paths

FastAPI backend
  -> exposes local API on 127.0.0.1:<dynamic_port>
  -> runs SQLite migrations on startup
  -> executes automation use cases
  -> performs pandas/openpyxl data processing
  -> reads/writes local workspace and AppData folders
```

### Frontend

The frontend lives in [`app-desktop`](./app-desktop) and is built with Angular standalone components.

Key characteristics:

- Angular 20.
- Standalone routes and components.
- Shared UI layer for cards, buttons, select fields, modal windows, drag-and-drop, notifications, top bar, and side menu.
- A `BackendService` initialized at application startup reads the local backend port from Electron before any API call is made.
- The renderer depends on Electron preload APIs, so the frontend is intended to run inside Electron rather than as a plain browser SPA.

Main route groups are defined in [`app-desktop/src/app/app.routes.ts`](./app-desktop/src/app/app.routes.ts):

- `/taxauto/livros-fiscais`
- `/taxdata/cancelled-invoices`
- `/taxdata/cancelled-invoices/report-details/:fileName`
- `/taxdata/cancelled-invoices/workflow`
- `/taxdata/apuracao`
- `/utilitarios/merge-excel-files`
- `/utilitarios/branch-manager`
- `/taxtrack/dashboard`

### Electron

The Electron layer lives in [`electron`](./electron).

Responsibilities:

- ensures single-instance behavior;
- starts the backend and waits for `/health`;
- passes the chosen backend port to the renderer through IPC;
- exposes native capabilities such as:
  - select directory;
  - select files;
  - focus the main window;
  - open local paths in the OS shell;
- stops the backend when the app closes.

Important files:

- [`electron/main/main.js`](./electron/main/main.js)
- [`electron/main/backend.js`](./electron/main/backend.js)
- [`electron/main/ipc/window.ipc.js`](./electron/main/ipc/window.ipc.js)
- [`electron/preload/preload.js`](./electron/preload/preload.js)

### Backend

The backend lives in [`local-backend`](./local-backend) and is a FastAPI application structured by module and use case.

Core backend traits:

- FastAPI for local HTTP APIs.
- SQLite for local persistence.
- pandas and openpyxl for spreadsheet processing and report generation.
- Selenium for browser automation.
- DI provider modules that assemble use cases and services.
- Local workspace and AppData folders created automatically.

Main backend entrypoint:

- [`local-backend/main.py`](./local-backend/main.py)

Dependency wiring:

- [`local-backend/core/di/automation_provider.py`](./local-backend/core/di/automation_provider.py)
- [`local-backend/core/di/data_process_provider.py`](./local-backend/core/di/data_process_provider.py)
- [`local-backend/core/di/shared_provider.py`](./local-backend/core/di/shared_provider.py)

Database bootstrap:

- [`local-backend/core/database/connection.py`](./local-backend/core/database/connection.py)

## Backend Modules

### 1. Shared module

The shared module provides local master-data management:

- companies;
- branches;
- branch groups;
- related repositories and query services.

These are stored in SQLite and exposed through CRUD-style endpoints.

Routes:

- `GET/POST/PATCH/DELETE /api/v1/companies`
- `GET/POST/PATCH/DELETE /api/v1/branches`
- `GET/POST /api/v1/branch-group`
- `POST /api/v1/branch-group/{group_id}/branches/{branch_id}`

### 2. Automation module

This module handles tasks that interact with external systems or files automatically.

Implemented backend flows include:

- tax report automation for fiscal books;
- cancelled invoice report generation through Selenium;
- multi-file merge for Excel/CSV consolidation.

Representative use cases:

- [`local-backend/modules/automation/application/usecases/run_livros_fiscais.py`](./local-backend/modules/automation/application/usecases/run_livros_fiscais.py)
- [`local-backend/modules/automation/application/usecases/cancelled_invoices_usecase.py`](./local-backend/modules/automation/application/usecases/cancelled_invoices_usecase.py)
- [`local-backend/modules/automation/application/usecases/merge_excel_files_usecase.py`](./local-backend/modules/automation/application/usecases/merge_excel_files_usecase.py)

Routes:

- `POST /api/v1/automation/tax-reports/run`
- `POST /api/v1/automation/cancelled-invoices/run`
- `POST /api/v1/automation/cancelled-invoices/validate-file`
- `POST /api/v1/utilities/merge-excel-files/run`

### 3. Data process module

This module focuses on local data analysis and auditing.

The most complete flow today is the cancelled invoices audit:

- load fiscal book and portal report;
- normalize and merge data;
- classify discrepancies by audit rules;
- compute summary metrics;
- export Excel audit reports;
- list, read, and delete saved audit reports.

Representative files:

- [`local-backend/modules/data_process/application/usecases/audit_cancelled_invoices_usecase.py`](./local-backend/modules/data_process/application/usecases/audit_cancelled_invoices_usecase.py)
- [`local-backend/modules/data_process/application/usecases/list_audit_reports_usecase.py`](./local-backend/modules/data_process/application/usecases/list_audit_reports_usecase.py)
- [`local-backend/modules/data_process/application/usecases/read_audit_report_usecase.py`](./local-backend/modules/data_process/application/usecases/read_audit_report_usecase.py)
- [`local-backend/modules/data_process/auditions/cancelled_invoices/services/load_and_merge_date_service.py`](./local-backend/modules/data_process/auditions/cancelled_invoices/services/load_and_merge_date_service.py)

Routes:

- `POST /api/v1/taxdata/cancelled-invoices/run`
- `GET /api/v1/taxdata/cancelled-invoices/report`
- `GET /api/v1/taxdata/cancelled-invoices/reports`
- `DELETE /api/v1/taxdata/cancelled-invoices/report`

There is also a fiscal period module that currently creates and lists periods and creates the directory structure for each period:

- `POST /api/v1/periodos/`
- `GET /api/v1/periodos/`
- `GET /api/v1/periodos/{id}`

## Main Frontend Flows

### Cancelled invoices audit

This is currently one of the clearest end-to-end flows in the project.

Frontend:

- upload or select the fiscal book and the portal cancelled invoices file;
- call the audit backend endpoint;
- navigate to a report details page;
- list previously generated audits;
- open saved report details;
- delete saved audit entries.

Backend:

- reads both files;
- detects headers in CSV/XLSX;
- creates normalized composite keys;
- performs an outer merge;
- classifies discrepancies according to cataloged rules;
- exports an Excel report to local storage;
- reconstructs summary information when an old report is opened later.

### Fiscal book automation

From the `Gerar Relatorios` screen, the operator can:

- choose the report/book type;
- choose a date range;
- choose branches;
- choose tasks like open, update, close, save spreadsheet, and save PDF;
- provide PortalGED credentials for the cancelled-invoices-related path;
- select an output folder through a native dialog.

The backend then validates the request and delegates execution to orchestration services that work with browser/ERP automation services.

### Merge Excel files

This utility:

- accepts multiple CSV/XLS/XLSX files;
- detects headers robustly;
- aligns columns across heterogeneous files;
- preserves source file name;
- writes a consolidated Excel output into a chosen directory.

### Branch manager

The branch manager is a local administrative area for:

- companies;
- branches;
- branch groups.

It includes:

- creation;
- inline editing;
- deletion;
- local filtering/search;
- validation of branch fields such as UF, CNPJ, and IE.

## Filesystem and Local Storage

The backend is designed to operate locally on Windows user folders.

### AppData storage

Configured in [`local-backend/core/config/settings.py`](./local-backend/core/config/settings.py):

- `APPDATA/taxauto/database.db`
- `APPDATA/taxauto/logs`
- `APPDATA/taxauto/data`

Additional audit exports currently use:

- `LOCALAPPDATA/TaxAuto/AuditReports`

### Workspace folders

Fiscal periods create a workspace under the user's Documents folder:

```text
Documents/TaxAuto/<ano>/<mes>/
  input/
    LIVRO_ENTRADA/
    LIVRO_SAIDA/
    DIFAL/
    ST/
    ESTORNO_CREDITO/
    ESTORNO_MERCADORIA_DETERIORADA/
    FOT/
    FRETE_ENTRADA/
    FRETE_SAIDA/
    INEXIGIBILIDADE/
  resultados/
```

The workspace manager also creates internal per-period folders under AppData:

```text
APPDATA/taxauto/data/<ano>/<mes>/
  raw/
  processed/
  output/
```

## Technology Stack

### Frontend

- Angular 20
- Angular Material
- RxJS
- SCSS

### Desktop shell

- Electron 40
- Electron Builder

### Backend

- Python 3.x
- FastAPI
- Uvicorn
- SQLite with `aiosqlite`
- pandas
- openpyxl
- Selenium
- PyInstaller

### Tooling

- ESLint
- Prettier
- Ruff
- Black

## Development Setup

### Prerequisites

The current repository is Windows-oriented. Several scripts and backend dependencies assume Windows APIs and PowerShell.

Recommended prerequisites:

- Node.js 20+ with npm
- Python 3.11+ available on `PATH`
- PowerShell
- Google Chrome installed
- A Windows environment with access to `APPDATA`, `LOCALAPPDATA`, and `Documents`

### Install dependencies

From the repository root:

```powershell
npm install
npm install --prefix app-desktop
```

For the Python backend:

```powershell
cd local-backend
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

That script:

- creates `.venv` if needed;
- upgrades `pip`;
- installs `requirements.txt`;
- installs Ruff and Black.

### Run in development

The main development command is:

```powershell
npm run dev
```

What it does:

- starts Angular dev server on port `4200`;
- waits for it to become available;
- launches Electron;
- Electron then starts the Python backend and passes the local API port to the frontend.

Important note:

- the Angular app is designed to initialize the backend URL through Electron IPC;
- running only `ng serve` is not enough for normal app operation, because `window.electron.getPort()` is required during app startup.

### Build the application

Frontend only:

```powershell
npm run build-front
```

Full desktop build:

```powershell
npm run build
```

This performs:

1. Angular production build.
2. Backend packaging via PyInstaller.
3. Electron packaging via Electron Builder.

Backend packaging script:

- [`local-backend/scripts/build-backend.ps1`](./local-backend/scripts/build-backend.ps1)

## Useful Scripts

Root `package.json`:

- `npm run dev`
  - Angular dev server + Electron.
- `npm run angular-start`
  - Starts Angular only.
- `npm run angular-build`
  - Builds Angular output for Electron packaging.
- `npm run backend-build`
  - Builds the Python backend executable.
- `npm run build-front`
  - Builds the desktop app without bundling backend again.
- `npm run build`
  - Full production build.

Backend scripts:

- [`local-backend/scripts/setup.ps1`](./local-backend/scripts/setup.ps1)
- [`local-backend/scripts/build-backend.ps1`](./local-backend/scripts/build-backend.ps1)

There is also a [`local-backend/scripts/run-api.ps1`](./local-backend/scripts/run-api.ps1), but the repository currently relies mainly on Electron to start the backend during normal development.

## Repository Structure

```text
taxauto-electron/
  app-desktop/       Angular renderer application
  electron/          Electron main/preload process and desktop IPC
  local-backend/     FastAPI backend, automations, data processing, SQLite
  icon/              Application icons
  dist/              Build artifacts
```

More detail:

- `app-desktop/src/app/core`
  - API services, models, config, global services.
- `app-desktop/src/app/shared`
  - Reusable UI components, layouts, validators, and mappers.
- `app-desktop/src/app/features`
  - Product modules such as tax automation, tax data, utilities, and dashboard.
- `local-backend/modules/automation`
  - Browser/ERP automation and file consolidation flows.
- `local-backend/modules/data_process`
  - Audit and period-related use cases.
- `local-backend/shared`
  - Shared entities, repositories, routes, and filesystem helpers.

## Current Implementation Status

Based on the current codebase, these areas look actively implemented and connected:

- cancelled invoices audit flow;
- cancelled invoices automation/report generation;
- merge Excel files utility;
- local management of companies, branches, and branch groups;
- Electron-to-backend startup and local API integration.

These areas look present but still evolving or partially scaffolded:

- apuracao processing flow beyond period creation and frontend screens;
- TaxTrack dashboard, which currently uses mock data;
- some route/service pairs for branch-group update/delete operations;
- some utility scripts and older documentation that no longer perfectly match the current structure.

This is worth keeping in mind when planning roadmap work or documenting feature completeness.

## Why the Architecture Makes Sense

The architecture is a good fit for the problem space because:

- tax operations often depend on local files and internal tools, not cloud-first flows;
- Selenium and filesystem-heavy routines are easier to control in a desktop environment;
- a local backend keeps sensitive fiscal files on the operator machine;
- Electron gives the frontend native dialogs and process orchestration without exposing backend complexity to the user;
- the modular backend allows automation and data-processing features to evolve separately.

## Troubleshooting Notes

- If the app window opens but API calls fail early, verify that Electron was able to start the backend and that the Python virtual environment exists under `local-backend/.venv`.
- If browser automation fails, verify Chrome availability and local access assumptions used by Selenium.
- If builds fail, ensure PowerShell scripts can run and Python dependencies are installed in the backend virtual environment.
- If old reports are missing, inspect `LOCALAPPDATA/TaxAuto/AuditReports`.

## Suggested Next Documentation Improvements

If you want to keep evolving the documentation after this README, the best next additions would be:

1. a backend API reference with request/response examples;
2. a feature maturity matrix by module;
3. a contributor guide for adding new frontend modules and backend use cases;
4. packaging and deployment notes for business users.
