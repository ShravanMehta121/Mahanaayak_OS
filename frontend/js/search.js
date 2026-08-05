/**
 * MAHANAYAK OS — Combined Live Table Search & Multi-Criteria Filtering
 */

document.addEventListener('DOMContentLoaded', () => {
  initTableFiltering();
});

function initTableFiltering() {
  const searchInput = document.getElementById('searchInput');
  const deptFilter = document.getElementById('deptFilter');
  const statusFilter = document.getElementById('statusFilter');
  const severityFilter = document.getElementById('severityFilter');
  const refreshBtn = document.getElementById('refreshTableBtn');
  const table = document.querySelector('.ticket-table');

  if (!table) return;

  function getRows() {
    return Array.from(table.querySelectorAll('tbody tr'));
  }

  function applyCombinedFilters() {
    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const selectedDept = (deptFilter ? deptFilter.value : '').toLowerCase().trim();
    const selectedStatus = (statusFilter ? statusFilter.value : '').toLowerCase().trim();
    const selectedSeverity = (severityFilter ? severityFilter.value : '').toLowerCase().trim();

    getRows().forEach((row) => {
      const textContent = row.textContent.toLowerCase();
      const deptText = (row.children[3] ? row.children[3].textContent : '').toLowerCase().trim();
      const statusText = (row.querySelector('.badge-open, .badge-pending, .badge-closed')
        ? row.querySelector('.badge-open, .badge-pending, .badge-closed').textContent
        : '').toLowerCase().trim();
      const severityText = (row.children[6] ? row.children[6].textContent : '').toLowerCase().trim();

      // Check text search query
      const matchesQuery = !query || textContent.includes(query);

      // Check Department match
      const matchesDept = !selectedDept || deptText.includes(selectedDept);

      // Check Status match
      const matchesStatus = !selectedStatus || statusText.includes(selectedStatus);

      // Check Severity match
      const matchesSeverity = !selectedSeverity || severityText.includes(selectedSeverity);

      if (matchesQuery && matchesDept && matchesStatus && matchesSeverity) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  if (searchInput) searchInput.addEventListener('input', applyCombinedFilters);
  if (deptFilter) deptFilter.addEventListener('change', applyCombinedFilters);
  if (statusFilter) statusFilter.addEventListener('change', applyCombinedFilters);
  if (severityFilter) severityFilter.addEventListener('change', applyCombinedFilters);

  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      if (searchInput) searchInput.value = '';
      if (deptFilter) deptFilter.value = '';
      if (statusFilter) statusFilter.value = '';
      if (severityFilter) severityFilter.value = '';
      applyCombinedFilters();
    });
  }
}

window.frontendSearch = {
  initialize() {
    initTableFiltering();
  }
};
