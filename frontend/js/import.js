/**
 * MAHANAYAK OS — Bulk CSV Importer Module
 * Parses CSV files, validates headers/rows, populates the Ground Issue Database,
 * and updates Open/Pending counters in real time.
 */

document.addEventListener('DOMContentLoaded', () => {
  initCSVImporter();
});

function initCSVImporter() {
  const importBtns = document.querySelectorAll('[data-action="import-csv"], .button-green');

  importBtns.forEach((btn) => {
    // Avoid double binding
    if (btn.dataset.importBound) return;
    btn.dataset.importBound = 'true';

    btn.addEventListener('click', () => {
      openCSVFileDialog();
    });
  });
}

function openCSVFileDialog() {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '.csv';

  fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      if (window.Toast) window.Toast.error('Only .csv files are supported.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const csvText = event.target.result;
      processCSVContent(csvText);
    };
    reader.onerror = () => {
      if (window.Toast) window.Toast.error('Failed to read CSV file.');
    };
    reader.readAsText(file);
  });

  fileInput.click();
}

function processCSVContent(csvText) {
  if (!csvText || !csvText.trim()) {
    if (window.Toast) window.Toast.error('CSV file is empty.');
    return;
  }

  let rows = [];

  if (window.Papa) {
    const parsed = window.Papa.parse(csvText, { header: true, skipEmptyLines: true });
    if (parsed.errors && parsed.errors.length && !parsed.data.length) {
      if (window.Toast) window.Toast.error('Invalid CSV format.');
      return;
    }
    rows = parsed.data;
  } else {
    // Vanilla CSV parser fallback
    rows = parseVanillaCSV(csvText);
  }

  if (!rows || !rows.length) {
    if (window.Toast) window.Toast.error('No data records found in CSV.');
    return;
  }

  // Validate Required Headers
  const firstRow = rows[0];
  const requiredHeaders = ['Ticket ID', 'Voter ID', 'Voter Name', 'Department', 'Description', 'Address', 'Status', 'Severity'];

  const normalizedKeys = Object.keys(firstRow).map((k) => k.trim().toLowerCase());
  const missingHeaders = requiredHeaders.filter(
    (header) => !normalizedKeys.includes(header.toLowerCase())
  );

  if (missingHeaders.length > 0) {
    if (window.Toast) {
      window.Toast.error(`Wrong CSV headers! Missing: ${missingHeaders.join(', ')}`);
    }
    return;
  }

  // Find table body
  const tbody = document.querySelector('.ticket-table tbody');
  if (!tbody) {
    if (window.Toast) window.Toast.error('Issue database table not found on page.');
    return;
  }

  let importedCount = 0;
  let skippedCount = 0;
  const imported = [];

  rows.forEach((row) => {
    const ticketId = getRowVal(row, 'Ticket ID');
    const voterId = getRowVal(row, 'Voter ID');
    const voterName = getRowVal(row, 'Voter Name');
    const dept = getRowVal(row, 'Department');
    const desc = getRowVal(row, 'Description');
    const address = getRowVal(row, 'Address');
    const status = getRowVal(row, 'Status');
    const severity = getRowVal(row, 'Severity');

    if (!ticketId || !voterName || !dept || !status) {
      skippedCount++;
      return;
    }

    imported.push({
      id: ticketId,
      voterId: voterId || 'V-N/A',
      citizenName: voterName,
      department: dept,
      description: desc,
      address: address,
      status: status,
      severity: severity
    });
    importedCount++;
  });

  if (importedCount > 0 && window.issueData) {
    // Register imported issues in the shared dataset, placed first so they render at the top.
    const reordered = {};
    imported.forEach((issue) => {
      reordered[issue.id] = issue;
    });
    Object.keys(window.issueData).forEach((id) => {
      if (!reordered[id]) reordered[id] = window.issueData[id];
    });
    window.issueData = reordered;
  }

  if (importedCount > 0) {
    if (window.IssueManager && window.IssueManager.renderTable) {
      window.IssueManager.renderTable();
    }
    updateKPICounters();
    if (window.Toast) {
      window.Toast.success(`Successfully imported ${importedCount} issues from CSV.${skippedCount > 0 ? ` (${skippedCount} invalid rows skipped)` : ''}`);
    }
  } else {
    if (window.Toast) window.Toast.warning('No valid rows imported from CSV.');
  }
}

function getRowVal(rowObj, headerName) {
  const key = Object.keys(rowObj).find((k) => k.trim().toLowerCase() === headerName.toLowerCase());
  return key && rowObj[key] ? rowObj[key].trim() : '';
}

function parseVanillaCSV(csvText) {
  const lines = csvText.split(/\r?\n/).filter((l) => l.trim());
  if (lines.length < 2) return [];

  const headers = lines[0].split(',').map((h) => h.trim().replace(/^"|"$/g, ''));
  const records = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map((v) => v.trim().replace(/^"|"$/g, ''));
    if (values.length === headers.length) {
      const obj = {};
      headers.forEach((h, idx) => {
        obj[h] = values[idx];
      });
      records.push(obj);
    }
  }
  return records;
}

function updateKPICounters() {
  const tbody = document.querySelector('.ticket-table tbody');
  if (!tbody) return;

  const rows = Array.from(tbody.querySelectorAll('tr'));
  let openCount = 0;
  let pendingCount = 0;

  rows.forEach((row) => {
    const badge = row.querySelector('.badge-open, .badge-pending, .badge-closed');
    if (badge) {
      const txt = badge.textContent.trim().toLowerCase();
      if (txt === 'open') openCount++;
      if (txt === 'pending') pendingCount++;
    }
  });

  const kpis = document.querySelectorAll('.header-kpi');
  kpis.forEach((kpi) => {
    const label = kpi.querySelector('.header-kpi-label');
    const val = kpi.querySelector('.header-kpi-value');
    if (label && val) {
      const txt = label.textContent.trim().toLowerCase();
      if (txt.includes('open')) val.textContent = openCount;
      if (txt.includes('pending')) val.textContent = pendingCount;
    }
  });
}

window.CSVImporter = {
  importCSV: openCSVFileDialog,
  processContent: processCSVContent
};
