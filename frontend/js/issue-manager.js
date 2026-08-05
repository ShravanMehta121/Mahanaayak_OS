/**
 * MAHANAYAK OS — Issue Detail Management Module
 * Supports View, Edit, Role-based field visibility (Admin vs Office),
 * Vertical Activity Timelines, and Live Dashboard Synchronization.
 */

const INITIAL_ISSUES = {
  '#1001': {
    id: '#1001',
    voterId: 'V-2201',
    citizenName: 'Suresh Mehra',
    phone: '+91 98220 11401',
    ward: 'Shivajinagar (Ward 12)',
    department: 'Utilities',
    category: 'Water Infrastructure',
    severity: 'Critical',
    status: 'Open',
    submissionDate: '2026-08-01 09:30 AM',
    assignedOfficer: 'Er. Rajesh Kulkarni',
    address: 'Shivajinagar / Shanivar Peth, Central Pune',
    description: 'Main underground pipe leakage causing low pressure across 40 households and street flooding.',
    remarks: 'Field team dispatched. Replacement PVC section requested from PMC depot.',
    attachments: ['pipe_leakage_photo1.jpg', 'site_inspection_report.pdf'],
    aiSummary: 'Critical infrastructure failure impacting 40+ families. High risk of local water contamination if unresolved within 24 hours.',
    priorityScore: '94.8 / 100',
    escalated: true,
    history: [
      { time: '09:30 AM — Aug 01', title: 'Issue Reported', desc: 'Logged via Citizen App by Suresh Mehra', user: 'System Telemetry', dept: 'Public Desk' },
      { time: '10:15 AM — Aug 01', title: 'Assigned to Department', desc: 'Routed to Utilities Department', user: 'Office Desk', dept: 'Utilities' },
      { time: '11:45 AM — Aug 01', title: 'Status Updated: Open', desc: 'Marked as Critical severity priority', user: 'Admin User', dept: 'Utilities' }
    ]
  },
  '#1002': {
    id: '#1002',
    voterId: 'V-2202',
    citizenName: 'Rahul Malhotra',
    phone: '+91 98220 22502',
    ward: 'Wakad (Ward 04)',
    department: 'Public Works',
    category: 'Road Infrastructure',
    severity: 'High',
    status: 'Pending',
    submissionDate: '2026-08-02 11:15 AM',
    assignedOfficer: 'Inspector Amit Deshmukh',
    address: 'Wakad / Hinjawadi Main Road, Pune',
    description: 'Large 4-foot pothole on main arterial street creating traffic gridlock during peak hours.',
    remarks: 'Asphalt patching crew scheduled for night shift deployment.',
    attachments: ['pothole_image.png'],
    aiSummary: 'High traffic obstruction on IT corridor. Potential traffic delay index +22%.',
    priorityScore: '81.4 / 100',
    escalated: false,
    history: [
      { time: '11:15 AM — Aug 02', title: 'Issue Reported', desc: 'Logged via Traffic Helpline', user: 'Citizen Portal', dept: 'Public Works' },
      { time: '02:00 PM — Aug 02', title: 'Assigned to Inspector', desc: 'Assigned to Amit Deshmukh', user: 'Admin User', dept: 'Public Works' }
    ]
  },
  '#1003': {
    id: '#1003',
    voterId: 'V-2203',
    citizenName: 'Zoya Dhillon',
    phone: '+91 98220 33603',
    ward: 'Kothrud (Ward 08)',
    department: 'Energy',
    category: 'Street Lighting',
    severity: 'Medium',
    status: 'Closed',
    submissionDate: '2026-08-03 04:20 PM',
    assignedOfficer: 'Tech. Sunil Pawar',
    address: 'Kothrud (Near Ideal Colony / Paud Road), Pune',
    description: 'Street light blinking intermittently creating dark spot near residential school crossing.',
    remarks: 'Replaced faulty capacitor and LED bulb. Tested fully operational.',
    attachments: ['repair_complete.jpg'],
    aiSummary: 'Minor electrical component failure. Successfully resolved.',
    priorityScore: '45.0 / 100',
    escalated: false,
    history: [
      { time: '04:20 PM — Aug 03', title: 'Issue Reported', desc: 'Logged via Web Portal', user: 'Zoya Dhillon', dept: 'Energy' },
      { time: '06:00 PM — Aug 03', title: 'Technician Dispatched', desc: 'Sunil Pawar on site', user: 'Office Desk', dept: 'Energy' },
      { time: '08:30 PM — Aug 03', title: 'Issue Resolved & Closed', desc: 'Replaced capacitor and verified lighting', user: 'Tech. Sunil Pawar', dept: 'Energy' }
    ]
  },
  '#1004': {
    id: '#1004',
    voterId: 'V-2204',
    citizenName: 'Gopal Chatterjee',
    phone: '+91 98220 44704',
    ward: 'Viman Nagar (Ward 02)',
    department: 'Health',
    category: 'Sanitation',
    severity: 'Low',
    status: 'Open',
    submissionDate: '2026-08-04 08:10 AM',
    assignedOfficer: 'Sanitation Supt. Patil',
    address: 'Viman Nagar / Pune Airport Area, Pune',
    description: 'Garbage pileup near public park entrance requiring bin clearance.',
    remarks: 'Compactor vehicle routed for morning pickup.',
    attachments: [],
    aiSummary: 'Routine sanitation request. Low health hazard.',
    priorityScore: '32.1 / 100',
    escalated: false,
    history: [
      { time: '08:10 AM — Aug 04', title: 'Issue Reported', desc: 'Logged via Mobile App', user: 'Gopal Chatterjee', dept: 'Health' }
    ]
  },
  '#1005': {
    id: '#1005',
    voterId: 'V-2205',
    citizenName: 'Karan Yadav',
    phone: '+91 98220 55805',
    ward: 'Hadapsar (Ward 11)',
    department: 'Public Works',
    category: 'Pedestrian Safety',
    severity: 'High',
    status: 'Open',
    submissionDate: '2026-08-04 02:45 PM',
    assignedOfficer: 'Eng. Vijay Shinde',
    address: 'Hadapsar / Magarpatta City, Pune',
    description: 'Broken concrete sidewalk slab exposing drain opening near bus stop.',
    remarks: 'Warning barricade placed.',
    attachments: [],
    aiSummary: 'Pedestrian fall risk. High priority for transit safety.',
    priorityScore: '76.8 / 100',
    escalated: true,
    history: [
      { time: '02:45 PM — Aug 04', title: 'Issue Reported', desc: 'Logged via Citizen Helpline', user: 'Karan Yadav', dept: 'Public Works' }
    ]
  },
  '#1006': {
    id: '#1006',
    voterId: 'V-2206',
    citizenName: 'Varun Sen',
    phone: '+91 98220 66906',
    ward: 'Dhankawadi (Ward 14)',
    department: 'Utilities',
    category: 'Water Supply',
    severity: 'Critical',
    status: 'Closed',
    submissionDate: '2026-08-04 06:00 PM',
    assignedOfficer: 'Er. Rajesh Kulkarni',
    address: 'Dhankawadi / Katraj, Pune',
    description: 'No water supply in sector 3 due to booster pump electrical trip.',
    remarks: 'Pump reset and valve recalibrated. Water pressure restored.',
    attachments: [],
    aiSummary: 'Power surge tripped main pump. Fully restored.',
    priorityScore: '89.0 / 100',
    escalated: false,
    history: [
      { time: '06:00 PM — Aug 04', title: 'Issue Reported', desc: 'Logged via Helplink', user: 'Varun Sen', dept: 'Utilities' },
      { time: '08:15 PM — Aug 04', title: 'Issue Closed', desc: 'Booster pump reset', user: 'Er. Rajesh Kulkarni', dept: 'Utilities' }
    ]
  },
  '#1007': {
    id: '#1007',
    voterId: 'V-2207',
    citizenName: 'Kiran Gill',
    phone: '+91 98220 77007',
    ward: 'Pashan (Ward 05)',
    department: 'Energy',
    category: 'Power Grid',
    severity: 'Medium',
    status: 'Pending',
    submissionDate: '2026-08-05 07:15 AM',
    assignedOfficer: 'Tech. Mahesh Rane',
    address: 'Pashan / Sus Road, Pune',
    description: 'Transformer sparking during rain. Needs insulator replacement.',
    remarks: 'Safety isolation switch activated. Crew en route.',
    attachments: [],
    aiSummary: 'Insulator tracking spark. Low fire risk after isolation.',
    priorityScore: '62.4 / 100',
    escalated: false,
    history: [
      { time: '07:15 AM — Aug 05', title: 'Issue Reported', desc: 'Logged via Emergency Desk', user: 'Kiran Gill', dept: 'Energy' }
    ]
  }
};

// Store issues in window memory
window.issueData = INITIAL_ISSUES;

document.addEventListener('DOMContentLoaded', () => {
  initIssueActions();
  renderTable();
});

function initIssueActions() {
  const table = document.querySelector('.ticket-table');
  if (!table) return;

  // Delegate click for View and Edit action buttons
  table.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;
    const tr = btn.closest('tr');
    if (!tr) return;

    const idEl = tr.querySelector('.ticket-id');
    const ticketId = idEl ? idEl.textContent.trim() : null;
    if (!ticketId) return;

    if (action === 'view-issue') {
      openIssueViewModal(ticketId);
    } else if (action === 'edit-issue') {
      openIssueEditModal(ticketId);
    } else if (action === 'delete-issue') {
      confirmDeleteIssue(ticketId);
    }
  });
}

function confirmDeleteIssue(id) {
  if (!window.Modal) return;

  const contentHtml = `
    <div style="padding: 16px; text-align: center;">
      <div style="width: 56px; height: 56px; border-radius: 999px; background: rgba(255,90,95,0.15); border: 1px solid rgba(255,90,95,0.4); color: #ff5a5f; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 16px;">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <h3 style="margin: 0 0 8px 0; color: #f4f7ff; font-size: 18px; font-weight: 700;">Delete Complaint Record</h3>
      <p style="margin: 0 0 24px 0; color: rgba(244,247,255,0.75); font-size: 14px;">Are you sure you want to delete complaint ticket <strong style="color: #7be3ff;">${escapeHtml(id)}</strong>? This action cannot be undone.</p>
      
      <div style="display: flex; gap: 12px; justify-content: center;">
        <button type="button" class="action-btn action-view" style="height: 38px; padding: 0 20px; font-size: 13px;" onclick="if(window.Modal) window.Modal.close();">Cancel</button>
        <button type="button" class="action-btn action-delete" style="height: 38px; padding: 0 20px; font-size: 13px; background: #ff5a5f; color: #fff;" onclick="deleteIssue('${escapeHtml(id)}');">Delete</button>
      </div>
    </div>
  `;

  window.Modal.open({
    title: `<i class="fa-solid fa-trash-can" style="color: #ff5a5f;"></i> Confirm Deletion`,
    contentHtml: contentHtml
  });
}

function deleteIssue(id) {
  if (window.issueData && window.issueData[id]) {
    delete window.issueData[id];
  }

  renderTable();

  refreshDashboard();

  if (window.Modal) window.Modal.close();
  if (window.Toast) window.Toast.error(`Complaint ticket ${id} has been permanently deleted.`);
}

function getIssue(id) {
  if (window.issueData && window.issueData[id]) {
    return window.issueData[id];
  }
  // Fallback template
  return {
    id: id,
    voterId: 'V-UNKNOWN',
    citizenName: 'Citizen Voter',
    phone: '+91 98000 00000',
    ward: 'Central Ward',
    department: 'Utilities',
    category: 'General Grievance',
    severity: 'Medium',
    status: 'Open',
    submissionDate: new Date().toISOString().replace('T', ' ').substring(0, 16),
    assignedOfficer: 'Unassigned',
    address: 'Pune Constituency',
    description: 'Grievance ticket logged in database.',
    remarks: 'No internal remarks.',
    attachments: [],
    aiSummary: 'Standard ticket recorded in system.',
    priorityScore: '50.0 / 100',
    escalated: false,
    history: [
      { time: 'Just now', title: 'Ticket Loaded', desc: 'Opened in management viewer', user: 'System', dept: 'Operations' }
    ]
  };
}

function renderIssueRow(issue) {
  return `
    <tr>
      <td class="ticket-id">${escapeHtml(issue.id)}</td>
      <td class="voter-id">${escapeHtml(issue.voterId)}</td>
      <td>${escapeHtml(issue.citizenName)}</td>
      <td>${escapeHtml(issue.department)}</td>
      <td><span class="issue-desc">${escapeHtml(issue.description)}</span><span class="issue-address">${escapeHtml(issue.address)}</span></td>
      <td><span class="badge ${getStatusBadgeClass(issue.status)}">${escapeHtml(issue.status)}</span></td>
      <td class="${getSeverityClass(issue.severity)}">${escapeHtml(issue.severity)}</td>
      <td class="col-actions">
        <div class="action-group">
          <button data-action="view-issue" class="action-btn action-view" type="button"><i class="fa-solid fa-eye"></i> View</button>
          <button data-action="edit-issue" class="action-btn action-edit" type="button"><i class="fa-solid fa-pen"></i> Edit</button>
          <button data-action="delete-issue" class="action-btn action-delete" type="button"><i class="fa-solid fa-trash-can"></i> Delete</button>
        </div>
      </td>
    </tr>
  `;
}

function renderTable() {
  const tbody = document.querySelector('.ticket-table tbody');
  if (!tbody) return;

  const issues = Object.values(window.issueData || {});
  tbody.innerHTML = issues.map(renderIssueRow).join('');
}

function openIssueViewModal(id) {
  if (!window.Modal) return;

  const issue = getIssue(id);
  const isAdmin = window.AuthService ? window.AuthService.hasRole('admin') : false;

  const timelineHtml = renderTimeline(issue.history || []);

  const contentHtml = `
    <div class="modal-dialog-lg">
      <div class="modal-grid-two">
        <div class="modal-card-box">
          <div class="modal-section-title">Citizen & Location Telemetry</div>
          <div class="modal-stat-num" style="font-size:18px; color:#7be3ff;">${escapeHtml(issue.citizenName)}</div>
          <p style="margin:4px 0;"><strong>Voter ID:</strong> ${escapeHtml(issue.voterId)} | <strong>Phone:</strong> ${escapeHtml(issue.phone)}</p>
          <p style="margin:4px 0;"><strong>State:</strong> ${escapeHtml(issue.state || 'Maharashtra')} | <strong>District:</strong> ${escapeHtml(issue.district || 'Pune')}</p>
          <p style="margin:4px 0;"><strong>City:</strong> ${escapeHtml(issue.city || 'Pune')} | <strong>Ward:</strong> ${escapeHtml(issue.ward)}</p>
          <p style="margin:4px 0;"><strong>Area / Locality:</strong> ${escapeHtml(issue.area || issue.ward)}</p>
          <p style="margin:4px 0;"><strong>Landmark:</strong> ${escapeHtml(issue.landmark || 'N/A')} | <strong>Pincode:</strong> ${escapeHtml(issue.pincode || '411001')}</p>
          <p style="margin:4px 0;"><strong>Street:</strong> ${escapeHtml(issue.street || 'Main Road')}</p>
          <p style="margin:4px 0;"><strong>Complete Address:</strong> ${escapeHtml(issue.address)}</p>
        </div>

        <div class="modal-card-box">
          <div class="modal-section-title">Department & Status Metrics</div>
          <p style="margin:4px 0;"><strong>Department:</strong> ${escapeHtml(issue.department)}</p>
          <p style="margin:4px 0;"><strong>Severity:</strong> <span class="${getSeverityClass(issue.severity)}">${escapeHtml(issue.severity)}</span></p>
          <p style="margin:4px 0;"><strong>Status:</strong> <span class="badge ${getStatusBadgeClass(issue.status)}">${escapeHtml(issue.status)}</span></p>
          <p style="margin:4px 0;"><strong>Assigned Officer:</strong> ${escapeHtml(issue.assignedOfficer)}</p>
          <p style="margin:4px 0;"><strong>Logged:</strong> ${escapeHtml(issue.submissionDate)}</p>
        </div>
      </div>

      <div class="modal-section" style="margin-top:16px;">
        <div class="modal-section-title">Issue Description & Remarks</div>
        <div class="modal-card-box">
          <p><strong>Description:</strong> ${escapeHtml(issue.description)}</p>
          <p style="margin-top:8px;"><strong>Internal Staff Remarks:</strong> ${escapeHtml(issue.remarks || 'None')}</p>
        </div>
      </div>

      ${isAdmin ? `
      <div class="modal-section" style="margin-top:16px;">
        <div class="modal-section-title"><i class="fa-solid fa-brain brand-accent"></i> Admin Intelligence & AI Audit Log</div>
        <div class="modal-card-box" style="background:rgba(29, 200, 238, 0.08); border-color:rgba(29, 200, 238, 0.25);">
          <p><strong>AI Summary:</strong> ${escapeHtml(issue.aiSummary || 'N/A')}</p>
          <div style="display:flex; gap:16px; margin-top:8px;">
            <span><strong>Priority Score:</strong> <strong style="color:#f7b213;">${escapeHtml(issue.priorityScore || 'N/A')}</strong></span>
            <span><strong>Escalated Status:</strong> ${issue.escalated ? '<span style="color:#ff5a5f; font-weight:700;">ESCALATED TO ADMIN</span>' : 'Standard Priority'}</span>
          </div>
        </div>
      </div>
      ` : ''}

      <div class="modal-section" style="margin-top:16px;">
        <div class="modal-section-title">Activity Timeline History</div>
        <div class="modal-card-box">
          ${timelineHtml}
        </div>
      </div>
    </div>
  `;

  window.Modal.open({
    title: `<i class="fa-solid fa-file-invoice brand-accent"></i> Issue Record ${escapeHtml(issue.id)}`,
    contentHtml: contentHtml
  });
}

function openIssueEditModal(id) {
  if (!window.Modal) return;

  const issue = getIssue(id);
  const isAdmin = window.AuthService ? window.AuthService.hasRole('admin') : false;

  const contentHtml = `
    <form id="editIssueForm" class="modal-dialog-lg" onsubmit="event.preventDefault(); saveIssue('${escapeHtml(id)}');">
      <div class="modal-grid-two">
        <div>
          <label class="input-label">Department</label>
          <select id="editDept" class="select-input">
            <option value="Utilities" ${issue.department === 'Utilities' ? 'selected' : ''}>Utilities</option>
            <option value="Public Works" ${issue.department === 'Public Works' ? 'selected' : ''}>Public Works</option>
            <option value="Energy" ${issue.department === 'Energy' ? 'selected' : ''}>Energy</option>
            <option value="Health" ${issue.department === 'Health' ? 'selected' : ''}>Health</option>
            <option value="Municipal Corporation" ${issue.department === 'Municipal Corporation' ? 'selected' : ''}>Municipal Corporation (PMC)</option>
          </select>
        </div>

        <div>
          <label class="input-label">Status Workflow</label>
          <select id="editStatus" class="select-input">
            <option value="Open" ${issue.status === 'Open' ? 'selected' : ''}>Open</option>
            <option value="Assigned" ${issue.status === 'Assigned' ? 'selected' : ''}>Assigned</option>
            <option value="In Progress" ${issue.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
            <option value="Resolved" ${issue.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
            <option value="Closed" ${issue.status === 'Closed' ? 'selected' : ''}>Closed</option>
          </select>
        </div>
      </div>

      <div class="modal-grid-two" style="margin-top:12px;">
        <div>
          <label class="input-label">Severity Level</label>
          <select id="editSeverity" class="select-input">
            <option value="Critical" ${issue.severity === 'Critical' ? 'selected' : ''}>Critical</option>
            <option value="High" ${issue.severity === 'High' ? 'selected' : ''}>High</option>
            <option value="Medium" ${issue.severity === 'Medium' ? 'selected' : ''}>Medium</option>
            <option value="Low" ${issue.severity === 'Low' ? 'selected' : ''}>Low</option>
          </select>
        </div>

        <div>
          <label class="input-label">Assigned Field Officer</label>
          <input id="editOfficer" type="text" class="text-input" value="${escapeHtml(issue.assignedOfficer || '')}" placeholder="Officer name..." />
        </div>
      </div>

      <div style="margin-top:12px;">
        <label class="input-label">Address / Location Landmark</label>
        <input id="editAddress" type="text" class="text-input" value="${escapeHtml(issue.address || '')}" />
      </div>

      <div style="margin-top:12px;">
        <label class="input-label">Issue Description</label>
        <textarea id="editDesc" class="textarea-input">${escapeHtml(issue.description || '')}</textarea>
      </div>

      <div style="margin-top:12px;">
        <label class="input-label">Internal Staff Remarks</label>
        <textarea id="editRemarks" class="textarea-input">${escapeHtml(issue.remarks || '')}</textarea>
      </div>

      <div class="modal-footer" style="margin-top:20px;">
        <button type="button" class="action-button ghost-button" onclick="if(window.Modal) window.Modal.close();">Cancel</button>
        <button type="submit" class="action-button primary-button"><i class="fa-solid fa-floppy-disk"></i> Save Issue Changes</button>
      </div>
    </form>
  `;

  window.Modal.open({
    title: `<i class="fa-solid fa-pen-to-square brand-accent"></i> Edit Issue Record ${escapeHtml(issue.id)}`,
    contentHtml: contentHtml
  });
}

function saveIssue(id) {
  const issue = getIssue(id);

  const dept = document.getElementById('editDept') ? document.getElementById('editDept').value : issue.department;
  const status = document.getElementById('editStatus') ? document.getElementById('editStatus').value : issue.status;
  const severity = document.getElementById('editSeverity') ? document.getElementById('editSeverity').value : issue.severity;
  const officer = document.getElementById('editOfficer') ? document.getElementById('editOfficer').value : issue.assignedOfficer;
  const address = document.getElementById('editAddress') ? document.getElementById('editAddress').value : issue.address;
  const desc = document.getElementById('editDesc') ? document.getElementById('editDesc').value : issue.description;
  const remarks = document.getElementById('editRemarks') ? document.getElementById('editRemarks').value : issue.remarks;

  const prevStatus = issue.status;

  issue.department = dept;
  issue.status = status;
  issue.severity = severity;
  issue.assignedOfficer = officer;
  issue.address = address;
  issue.description = desc;
  issue.remarks = remarks;

  // Add event to history
  if (prevStatus !== status) {
    issue.history.unshift({
      time: 'Just now',
      title: `Status Updated: ${status}`,
      desc: `Status updated from ${prevStatus} to ${status}`,
      user: window.AuthService ? window.AuthService.getCurrentUser()?.username : 'Staff User',
      dept: dept
    });
  }

  // Update in dataset
  window.issueData[id] = issue;

  // Update table row in DOM
  updateTableRowInDOM(id, issue);

  // Recalculate header KPI counters
  refreshDashboard();

  if (window.Modal) window.Modal.close();
  if (window.Toast) window.Toast.success(`Issue ${id} updated successfully.`);
}

function updateTableRowInDOM(id, issue) {
  if (window.issueData) window.issueData[id] = issue;
  renderTable();
}

function refreshDashboard() {
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

function renderTimeline(history) {
  if (!history || !history.length) {
    return '<div style="color:var(--text-2); font-size:12px;">No activity logged yet.</div>';
  }

  const items = history.map((item) => `
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-time">${escapeHtml(item.time)}</div>
      <div class="timeline-title">${escapeHtml(item.title)}</div>
      <div class="timeline-desc">${escapeHtml(item.desc)}</div>
      <div class="timeline-user">By: ${escapeHtml(item.user)} (${escapeHtml(item.dept)})</div>
    </div>
  `).join('');

  return `<div class="timeline-container">${items}</div>`;
}

function getStatusBadgeClass(status) {
  const s = (status || '').toLowerCase();
  if (s.includes('open')) return 'badge-open';
  if (s.includes('pending') || s.includes('assigned') || s.includes('progress')) return 'badge-pending';
  if (s.includes('closed') || s.includes('resolved')) return 'badge-closed';
  return 'badge-open';
}

function getSeverityClass(severity) {
  const s = (severity || '').toLowerCase();
  if (s.includes('critical')) return 'badge-critical';
  if (s.includes('high')) return 'badge-high';
  if (s.includes('medium')) return 'badge-medium';
  if (s.includes('low')) return 'badge-low';
  return 'badge-medium';
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

window.IssueManager = {
  openView: openIssueViewModal,
  openEdit: openIssueEditModal,
  save: saveIssue,
  refresh: refreshDashboard,
  renderRow: renderIssueRow,
  renderTable: renderTable,
  updateRow: updateTableRowInDOM
};
