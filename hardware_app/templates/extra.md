/* ============================================
   BASE & BACKGROUND - YOUR DARK THEME (KEPT)
   ============================================ */
body {
  background: radial-gradient(circle at top left, #1e293b, #1e293b, #0f172a 60%);
  color: #e2e8f0;
  font-family: 'Montserrat', sans-serif;
  min-height: 100vh;
}

.navbar {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding: 15px 25px;
}

.navbar-brand {
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 1px;
  font-size: 1.3rem;
  text-transform: uppercase;
}

.sidebar {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(12px);
  min-height: 100vh;
  padding: 25px 18px;
  border-right: 1px solid rgba(255,255,255,0.05);
}

.sidebar a {
  display: flex;
  align-items: center;
  color: #cbd5e1;
  padding: 12px 15px;
  text-decoration: none;
  margin-bottom: 10px;
  border-radius: 14px;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.sidebar a i {
  margin-right: 12px;
  font-size: 16px;
}

.sidebar a.active {
  background: linear-gradient(135deg, #f59e0b, #ea580c);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
}

.sidebar a:hover:not(.active) {
  background: rgba(255,255,255,0.05);
  color: white;
  transform: translate(3px);
}

/* ============================================
   REGULAR CARDS - YOUR DARK THEME (KEPT)
   ============================================ */
.card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.35);
  margin-bottom: 20px;
  color: #f8fafc;
  height: 100%;
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-header {
  background: transparent;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  color: #f8fafc;
  font-weight: 600;
}

/* ============================================
   STAT CARDS - NETLIFY SOFT SKY BLUE (UPDATED)
   ============================================ */
.stat-card {
  background: linear-gradient(135deg, rgba(50, 231, 223, 0.12) 0%, rgba(50, 231, 223, 0.06) 100%);
  border: 1px solid rgba(50, 231, 223, 0.25);
  border-radius: 24px;
  padding: 20px;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.stat-card:hover {
   transform: translateY(-5px);
  background: linear-gradient(135deg, rgba(50, 231, 223, 0.2) 0%, rgba(50, 231, 223, 0.1) 100%);
  border-color: rgba(50, 231, 223, 0.45);
  box-shadow: 0 12px 30px rgba(50, 231, 223, 0.15);
}

.stat-card .card-body {
  padding: 0;
}

.stat-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 16px auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(50, 231, 223, 0.2), rgba(50, 231, 223, 0.1));
  color: #32E7DF;
  font-size: 26px;
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon {
 background: linear-gradient(135deg, rgba(50, 231, 223, 0.3), rgba(50, 231, 223, 0.18));
  color: #7df5f0;
  transform: scale(1.05);
}

.stat-card h2, .stat-card h4 {
  color: white;
  font-weight: 800;
  margin-bottom: 8px;
  font-size: 2rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card .text-muted {
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* ============================================
   CUSTOM FORM CARD (KEPT)
   ============================================ */
.custom-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 35px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* ============================================
   CUSTOM CHECKBOX (KEPT)
   ============================================ */
.customer-checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.custom-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #32E7DF;
}

.custom-label {
  color: #cbd5e1;
  font-size: 14px;
}

/* ============================================
   CUSTOM LABELS (KEPT)
   ============================================ */
.custom-label {
  display: block;
  margin-bottom: 10px;
  color: #cbd5e1;
  font-size: 14px;
  font-weight: 500;
}

/* ============================================
   ALERT MESSAGES (KEPT)
   ============================================ */
.alert-danger {
  background: rgba(220, 38, 38, 0.15);
  border: 1px solid rgba(220, 38, 38, 0.3);
  color: #f87171;
  padding: 10px 15px;
  border-radius: 12px;
  margin-top: 10px;
}

.alert-success {
  background: rgba(34, 197, 94, 0.15);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
  padding: 10px 15px;
  border-radius: 12px;
  margin-top: 10px;
}

/* ============================================
   BUTTONS (KEPT YOUR ORANGE/TEAL)
   ============================================ */
.back-btn {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.05);
  padding: 12px 18px;
  border-radius: 16px;
  color: white;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: rgba(255,255,255,0.07);
  color: white;
}

.save-btn {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.9), rgba(14, 165, 233, 0.9));
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 16px;
  font-weight: 700;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(4px);
}

.save-btn:hover {
  background: linear-gradient(135deg, #38bdf8, #0ea5e9);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(56, 189, 248, 0.3);
  color: white;
}

/* ============================================
   FORM ELEMENTS (KEPT)
   ============================================ */
.errorlist {
  color: #f87171;
  list-style: none;
  padding-left: 0;
  font-size: 13px;
  margin-top: 5px;
}

input:invalid, select:invalid {
  border-color: #f87171;
}

.form-text {
  color: #94a3b8;
  font-size: 12px;
}

.text-muted, small.text-muted, .form-text {
  color: #94a3b8 !important;
}

.errorlist li {
  color: #f87171;
  list-style: none;
  padding-left: 0;
}

.invalid-feedback, .error-message {
  color: #f87171;
  font-size: 13px;
  margin-top: 5px;
}

.row.mb-4 .col-md-md-3 {
  display: flex;
  margin-bottom: 20px;
}

/* ============================================
   SELECT OPTIONS (KEPT)
   ============================================ */
select option {
  background: #0f172a;
  color: white;
}

/* ============================================
   BALANCE BADGE (KEPT)
   ============================================ */
.balance-badge {
  background: rgba(50, 231, 223, 0.15);
  color: #32E7DF;
  padding: 8px 14px;
  border-radius: 12px;
  font-weight: 600;
  display: inline-block;
}

/* ============================================
   LOW STOCK BADGE (KEPT)
   ============================================ */
.low-stock-badge {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: inline-block;
}

/* ============================================
   DELETE PAGE (KEPT)
   ============================================ */
.delete-icon {
  width: 90px;
  height: 90px;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  font-size: 40px;
}

.delete-warning-box {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 18px;
  padding: 18px;
  color: #e2e8f0;
  font-weight: 600;
  word-break: break-word;
}

/* ============================================
   INFO BOX (KEPT)
   ============================================ */
.info-box {
  background: rgba(50, 231, 223, 0.08);
  border: 1px solid rgba(50, 231, 223, 0.2);
  color: #d1faf7;
  padding: 18px;
  border-radius: 18px;
  font-size: 14px;
}

/* ============================================
   RECEIPT CARD (KEPT)
   ============================================ */
.receipt-card {
  width: 100%;
  max-width: 500px;
  background: rgba(30, 41, 59, 0.75);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 40px;
  backdrop-filter: blur(14px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.35);
  color: #f8fafc;
}

.receipt-title {
  font-weight: 700;
  color: #fbbf24;
  letter-spacing: 1px;
}

.receipt-subtitle {
  color: #94a3b8;
  margin: 0;
  font-size: 14px;
}

.receipt-divider {
  height: 1px;
  background: rgba(255,255,255,0.06);
  margin: 20px 0;
}

.receipt-info {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.receipt-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #cbd5e1;
}

.amount-text {
  font-size: 2.3rem;
  font-weight: 700;
  color: #fbbf24;
}

@media print {
  body {
    background: white;
  }
  .sidebar,
  .navbar,
  .btn {
    display: none;
  }
  .receipt-card {
    box-shadow: none;
    border: none;
    background: white;
    color: black;
  }
  .receipt-title {
    color: black;
  }
}

/* ============================================
   PRODUCT LIST PAGE (KEPT)
   ============================================ */
.add-btn {
  background: rgba(245,158,11,0.12);
  border: 1px solid rgba(245,158,11,0.2);
  color: #fbbf24;
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.add-btn:hover {
  background: rgba(245,158,11,0.18);
  color: #fbbf24;
}

/* ============================================
   TABLES (KEPT DARK)
   ============================================ */
.table-panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 25px;
  backdrop-filter: blur(12px);
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  color: #e2e8f0;
}

.custom-table thead {
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.custom-table th {
  padding: 18px;
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

.custom-table td {
  padding: 18px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.custom-table tbody tr:hover {
  background: rgba(255,255,255,0.03);
}

.table {
  color: #e2e8f0;
}

.table thead th {
  border-bottom: 1px solid rgba(255,255,255,0.08);
  color: #94a3b8;
  font-weight: 600;
  font-size: 13px;
}

.table td {
  border-color: rgba(255,255,255,0.04);
  padding: 16px;
  vertical-align: middle;
}

.table tbody tr:hover {
  background: rgba(255,255,255,0.03);
}

/* ============================================
   ACTION BUTTONS (KEPT)
   ============================================ */
.action-btn {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: rgba(245,158,11,0.12);
  border: 1px solid rgba(245,158,11,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fbbf24;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(245,158,11,0.2);
  color: white;
}

.secondary-btn {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.05);
  color: #cbd5e1;
}

.delete-btn {
  color: #f87171;
}

.low-stock {
  background: rgba(239,68,68,0.12);
  color: #f87171;
  padding: 6px 12px;
  border-radius: 12px;
  font-weight: 600;
  display: inline-block;
}

/* ============================================
   RECORD DEPOSIT PAGE (KEPT)
   ============================================ */
.custom-form-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 35px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.balance-card {
  background: rgba(245,158,11,0.08);
  border: 1px solid rgba(245,158,11,0.15);
  border-radius: 24px;
  padding: 25px;
}

.balance-label {
  color: #94a3b8;
  margin-bottom: 10px;
  font-size: 14px;
}

.balance-amount {
  color: #fbbf24;
  font-weight: 700;
  margin: 0;
}

.custom-input {
  width: 100%;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 14px 16px;
  color: white;
  outline: none;
  transition: all 0.3s ease;
}

.custom-input:focus {
  background: rgba(255,255,255,0.06);
  border-color: rgba(245,158,11,0.3);
  box-shadow: 0 0 0 3px rgba(245,158,11,0.08);
}

.custom-input::placeholder {
  color: #64748b;
}

.cancel-btn {
  text-decoration: none;
  background: rgba(255,255,255,0.04);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255,255,255,0.05);
  color: #cbd5e1;
  padding: 14px 24px;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: rgba(255,255,255,0.08);
  color: white;
}

/* ============================================
   REPORTS PAGE (KEPT)
   ============================================ */
.report-stat-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
  padding: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(12px);
  height: 100%;
  transition: all 0.3s ease;
}

.report-stat-card:hover {
  transform: translateY(-3px);
  background: rgba(255,255,255,0.05);
}

.report-label {
  color: #94a3b8;
  margin-bottom: 8px;
  font-size: 14px;
}

.report-stat-card h3 {
  color: white;
  font-weight: 700;
  font-size: 24px;
}

.report-icon {
  width: 55px;
  height: 55px;
  border-radius: 18px;
  background: rgba(245,158,11,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fbbf24;
  font-size: 22px;
}

.report-table-panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 25px;
  backdrop-filter: blur(12px);
}

.report-table {
  width: 100%;
  border-collapse: collapse;
  color: #e2e8f0;
}

.report-table thead {
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.report-table th {
  padding: 18px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 600;
}

.report-table td {
  padding: 18px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.report-table tbody tr:hover {
  background: rgba(255,255,255,0.03);
}

/* ============================================
   SALES LIST PAGE (KEPT)
   ============================================ */
.sales-stat-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
  padding: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(12px);
  height: 100%;
}

.sales-label {
  color: #94a3b8;
  margin-bottom: 8px;
  font-size: 14px;
}

.sales-stat-card h3 {
  color: white;
  font-weight: 700;
}

.sales-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(245,158,11,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fbbf24;
  font-size: 22px;
}

.sales-table-panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 28px;
  padding: 25px;
  backdrop-filter: blur(12px);
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
  color: #e2e8f0;
}

.sales-table thead {
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.sales-table th {
  padding: 18px;
  font-size: 13px;
  color: #94a3b8;
  font-weight: 600;
}

.sales-table td {
  padding: 18px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.sales-table tbody tr:hover {
  background: rgba(255,255,255,0.03);
}

.payment-badge {
  background: rgba(59,130,246,0.12);
  color: #60a5fa;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.free-badge {
  background: rgba(34,197,94,0.12);
  color: #4ade80;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.distance-badge {
  background: rgba(34,197,94,0.12);
  color: #4ade80;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 10px;
  margin-left: 5px;
}

/* ============================================
   STOCK HISTORY PAGE (KEPT)
   ============================================ */
.history-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.history-card .card-header {
  background: transparent;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  color: #f8fafc;
  font-weight: 600;
}

.history-card .table {
  color: #e2e8f0;
}

.history-card .table thead th {
  border-bottom: 1px solid rgba(255,255,255,0.08);
  color: #94a3b8;
}

.history-card .table td {
  border-color: rgba(255,255,255,0.04);
}

.stock-positive {
  color: #4ade80;
  font-weight: 600;
}

.stock-negative {
  color: #f87171;
  font-weight: 600;
}

/* ============================================
   PAGE HEADER (UPDATED FOR BETTER VISIBILITY)
   ============================================ */
.text-light {
  color: #f8fafc !important;
}

h2.fw-bold.text-light {
  color: white !important;
  font-weight: 800;
}

p.text-muted {
  color: #94a3b8 !important;
}

/* ============================================
   RESPONSIVE ADJUSTMENTS
   ============================================ */
@media (max-width: 768px) {
  .stat-card {
    padding: 16px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 22px;
  }
  
  .stat-card h2, .stat-card h4 {
    font-size: 1.5rem;
  }
  
  .custom-card {
    padding: 20px;
  }
}