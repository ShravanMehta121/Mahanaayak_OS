/**
 * MAHANAYAK OS — Synchronize System Data Service
 * Provides mock API telemetry synchronization with spinner loading states,
 * chart updates, table refreshes, and toast feedback.
 */

const SyncService = {
  /**
   * Mock API function simulating telemetry fetch from backend server.
   * Replace this inner implementation later with real fetch('/api/v1/telemetry/sync')
   * @returns {Promise<{success: boolean, message: string}>}
   */
  async fetchLatestData() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          message: 'System telemetry and ticket database synchronized.'
        });
      }, 1250);
    });
  },

  /**
   * Executes sync workflow for target button element.
   * @param {HTMLElement} btn 
   */
  async executeSync(btn) {
    if (!btn || btn.disabled) return;

    const originalContent = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Syncing...`;

    try {
      const response = await this.fetchLatestData();

      if (response.success) {
        // Refresh Table Data & Animations
        this.refreshTable();

        // Refresh Chart.js instances if active
        this.refreshCharts();

        // Update Header KPI Counters
        this.refreshKPIs();

        if (window.Toast) {
          window.Toast.success(response.message);
        }
      } else {
        if (window.Toast) {
          window.Toast.error(response.message || 'Sync failed.');
        }
      }
    } catch (err) {
      if (window.Toast) {
        window.Toast.error('Network sync error occurred.');
      }
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalContent;
    }
  },

  refreshTable() {
    const table = document.querySelector('.ticket-table');
    if (table) {
      table.style.opacity = '0.7';
      setTimeout(() => {
        table.style.opacity = '1';
        table.style.transition = 'opacity 200ms ease';
      }, 150);
    }

    // Rebuild all rows from the shared dataset through the single row renderer
    if (window.IssueManager && window.IssueManager.renderTable) {
      window.IssueManager.renderTable();
    }
  },

  refreshCharts() {
    // If global chart instances exist, update them
    if (window.Chart && window.Chart.instances) {
      Object.values(window.Chart.instances).forEach((chart) => {
        chart.update();
      });
    }
  },

  refreshKPIs() {
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
};

document.addEventListener('DOMContentLoaded', () => {
  const syncBtns = document.querySelectorAll('[data-action="sync-data"], .button-purple, .war-room-refresh');

  syncBtns.forEach((btn) => {
    if (btn.dataset.syncBound) return;
    btn.dataset.syncBound = 'true';

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      SyncService.executeSync(btn);
    });
  });
});

window.SyncService = SyncService;
