# Hardware Stock & Sales Management

A Django web application for managing day-to-day operations in a hardware shop. It brings product records, stock movements, sales, suppliers, and customer deposit accounts into one place.

## What it does

- **Product management** — Maintain a catalogue of hardware products, categories, units, and reorder levels.
- **Stock tracking** — Record incoming stock, purchase costs, selling prices, suppliers, and payment methods. Current quantities are calculated from stock entries and recorded sales.
- **Sales recording** — Record sales, check available stock, calculate totals, and apply the project's transport-fee rules.
- **Low-stock monitoring** — Highlight products at or below their configured reorder levels.
- **Supplier records** — Store supplier contact details and track outstanding supplier credit.
- **Customer deposit scheme** — Register customers, record deposits, view balances, and record eligible goods withdrawals against a customer's balance.
- **Dashboard and reports** — View operational summaries such as today's sales, low-stock products, deposits, withdrawals, and supplier credit.

## Built with

- Python
- Django
- SQLite
- HTML and CSS templates
- Bootstrap 5 via `django-crispy-forms`

## Project structure

```text
Hardware-System-Management/
├── hardware_app/       # Products, stock, sales, suppliers, deposits and reports
├── users/              # User-related views and forms
├── hardwareproject/    # Django project configuration
├── manage.py
├── requirements.txt
├── Procfile
└── build.sh
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/DaphineNakandi/Hardware-System-Management.git
cd Hardware-System-Management
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to a new file named `.env` in the project root, then replace the placeholder secret key with a long random value. Keep `DEBUG=True` only for local development.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

The example also sets `ALLOWED_HOSTS` for local development. Keep `.env` private. Do not commit real secret keys or production credentials.

### 5. Set up the database and start the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Access and roles

The application uses Django authentication. Some management views are restricted to users in the **Store Manager** or **Sales Attendant** groups. Create users and assign them to the appropriate group through the Django admin.

## Notes

- The local development database uses SQLite.
- Product quantities are derived from stock entries and sales.
- Customer deposit withdrawals are limited to the product categories configured in the application.
- Transport charges follow the thresholds implemented in the sales workflow.

## Current project status

This repository contains the Django application source. Before deploying it for real shop operations, review the production security settings, configure a production database and static-file hosting, and test the main workflows with non-sensitive sample data.
