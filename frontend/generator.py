import os
import re

base_dir = r'C:\Users\RAJASHREE\Desktop\Files\z. Miscelleneous\Projects\Mahanaayak OS\Mahanaayak_OS\frontend'
admin_dir = os.path.join(base_dir, 'admin')
css_dir = os.path.join(base_dir, 'css')
js_dir = os.path.join(base_dir, 'js')

# Base template extraction
with open(os.path.join(admin_dir, 'war-room.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# Generate global drawer components
drawer_html = """
    <!-- Global Notifications Drawer -->
    <div id="notificationsDrawer" class="drawer-overlay hidden">
      <div class="drawer drawer-right">
        <div class="drawer-header">
          <h3><i class="fa-solid fa-bell"></i> Notifications</h3>
          <button class="drawer-close" aria-label="Close notifications"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="drawer-tabs">
          <button class="tab-btn active">All</button>
          <button class="tab-btn">Critical</button>
          <button class="tab-btn">Alerts</button>
        </div>
        <div class="drawer-body">
          <div class="drawer-empty-state hidden">
            <i class="fa-regular fa-bell-slash"></i>
            <p>No new notifications</p>
          </div>
          <div class="notification-item critical">
            <div class="notif-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
            <div class="notif-content">
              <h4>Critical Escalation</h4>
              <p>Water supply issue in Ward 4 has been pending for 7 days.</p>
              <span class="notif-time">10 mins ago</span>
            </div>
          </div>
          <div class="notification-item warning">
            <div class="notif-icon"><i class="fa-solid fa-clock"></i></div>
            <div class="notif-content">
              <h4>SLA Breach Warning</h4>
              <p>5 complaints in Public Works approaching deadline.</p>
              <span class="notif-time">1 hour ago</span>
            </div>
          </div>
          <div class="notification-item success">
            <div class="notif-icon"><i class="fa-solid fa-check-circle"></i></div>
            <div class="notif-content">
              <h4>Complaint Resolved</h4>
              <p>Electricity outage in Ward 12 fixed.</p>
              <span class="notif-time">2 hours ago</span>
            </div>
          </div>
        </div>
        <div class="drawer-footer">
          <button class="action-button button-outline w-100">Mark All as Read</button>
        </div>
      </div>
    </div>

    <!-- Global Search Palette -->
    <div id="searchPalette" class="modal-overlay hidden">
      <div class="search-palette-modal">
        <div class="search-input-wrap">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input type="text" placeholder="Search citizens, complaints, members..." class="global-search-input" autofocus>
          <button class="esc-btn" onclick="document.getElementById('searchPalette').classList.add('hidden')">ESC</button>
        </div>
        <div class="search-results">
          <div class="search-group">
            <h5>Recent Searches</h5>
            <a href="#" class="search-result-item"><i class="fa-solid fa-clock-rotate-left"></i> Water issue Ward 12</a>
            <a href="#" class="search-result-item"><i class="fa-solid fa-clock-rotate-left"></i> Rahul Sharma</a>
          </div>
        </div>
      </div>
    </div>
"""

# Update sidebar in template to include all links
nav_links_html = """
        <nav class="sidebar-nav">
          <div class="nav-section">MAIN</div>
          <a class="sidebar-link" href="./war-room.html"><span class="icon-circle"><i class="fa-solid fa-grid-2"></i></span><span>War Room</span></a>
          <a class="sidebar-link" href="./executive-brief.html"><span class="icon-circle"><i class="fa-solid fa-bolt"></i></span><span>AI Executive Brief</span></a>
          
          <div class="nav-section" style="margin-top: 16px;">MANAGEMENT</div>
          <a class="sidebar-link" href="./team-members.html"><span class="icon-circle"><i class="fa-solid fa-users"></i></span><span>Team Management</span></a>
          <a class="sidebar-link" href="./citizens.html"><span class="icon-circle"><i class="fa-solid fa-address-book"></i></span><span>Citizen Database</span></a>
          
          <div class="nav-section" style="margin-top: 16px;">INTELLIGENCE</div>
          <a class="sidebar-link" href="./health-dashboard.html"><span class="icon-circle"><i class="fa-solid fa-heart-pulse"></i></span><span>Constituency Health</span></a>
          <a class="sidebar-link" href="./ward-health.html"><span class="icon-circle"><i class="fa-solid fa-map-location-dot"></i></span><span>Ward Intelligence</span></a>
          <a class="sidebar-link" href="./ward-comparison.html"><span class="icon-circle"><i class="fa-solid fa-code-compare"></i></span><span>Ward Comparison</span></a>
          
          <div class="nav-section" style="margin-top: 16px;">OPERATIONS</div>
          <a class="sidebar-link" href="./campaign.html"><span class="icon-circle"><i class="fa-solid fa-bullhorn"></i></span><span>Campaign Planner</span></a>
          <a class="sidebar-link" href="./department.html"><span class="icon-circle"><i class="fa-solid fa-building"></i></span><span>Departments</span></a>
          <a class="sidebar-link" href="./reports.html"><span class="icon-circle"><i class="fa-solid fa-file-invoice"></i></span><span>Reports Center</span></a>
          
          <div class="nav-section" style="margin-top: 16px;">SYSTEM</div>
          <a class="sidebar-link" href="./activity-logs.html"><span class="icon-circle"><i class="fa-solid fa-list-check"></i></span><span>Activity Logs</span></a>
          <a class="sidebar-link" href="./system-monitoring.html"><span class="icon-circle"><i class="fa-solid fa-server"></i></span><span>System Monitoring</span></a>
          <a class="sidebar-link" href="./settings.html"><span class="icon-circle"><i class="fa-solid fa-gear"></i></span><span>Settings</span></a>
        </nav>
"""

template = re.sub(r'<nav class="sidebar-nav">.*?</nav>', nav_links_html, template, flags=re.DOTALL)
template = template.replace('</body>', f'{drawer_html}\n  </body>')

# Update header with bell and search icons
header_actions_html = """
          <div class="page-header-actions header-kpis">
            <button class="icon-btn search-trigger" aria-label="Global Search" style="background: var(--surface-1); border: 1px solid var(--border-soft); border-radius: 50%; width: 40px; height: 40px; color: var(--text-1); cursor: pointer;"><i class="fa-solid fa-magnifying-glass"></i></button>
            <button class="icon-btn notification-trigger" aria-label="Notifications" style="background: var(--surface-1); border: 1px solid var(--border-soft); border-radius: 50%; width: 40px; height: 40px; color: var(--text-1); cursor: pointer; position: relative;">
              <i class="fa-solid fa-bell"></i>
              <span class="notification-badge" style="position: absolute; top: -5px; right: -5px; background: var(--red); color: white; font-size: 10px; border-radius: 10px; padding: 2px 6px;">3</span>
            </button>
            <div class="header-kpi war-room-kpi">
              <span class="header-kpi-label">Win Probability</span>
              <div class="header-kpi-value"><i class="fa-solid fa-arrow-trend-up"></i>65%</div>
            </div>
          </div>
"""
template = re.sub(r'<div class="page-header-actions header-kpis">.*?</div>\s*</header>', f'{header_actions_html}\n        </header>', template, flags=re.DOTALL)

def create_page(filename, title, content_html, active_link_href):
    page_content = template
    # Remove all active classes first
    page_content = page_content.replace('class="sidebar-link active"', 'class="sidebar-link"')
    # Add active class back to the right link
    if active_link_href:
        page_content = page_content.replace(f'href="{active_link_href}"', f'href="{active_link_href}" class="sidebar-link active"')
    
    # Replace title
    page_content = re.sub(r'<title>.*?</title>', f'<title>{title} | Mahanaayak OS</title>', page_content)
    page_content = re.sub(r'<h1 class="page-header-title">.*?</h1>', f'<h1 class="page-header-title">{title}</h1>', page_content)
    
    # Replace main content
    page_content = re.sub(r'(<header class="page-header">.*?</header>).*?(</main>)', r'\1\n' + content_html + r'\n      \2', page_content, flags=re.DOTALL)
    
    filepath = os.path.join(admin_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_content)
        
pages_data = {
    'team-members.html': {
        'title': 'Team Management',
        'active_link': './team-members.html',
        'content': """
        <section class="page-intro">
          <div>
            <h2 class="page-intro-title">Team Roster</h2>
            <div class="page-intro-copy">Manage field officers, ward executives, and support staff.</div>
          </div>
          <div class="page-intro-actions" style="display: flex; gap: 8px;">
            <a href="team-member-add.html" class="action-button button-blue"><i class="fa-solid fa-plus"></i> Add Member</a>
          </div>
        </section>
        
        <section class="panel table-panel">
          <div class="table-toolbar">
            <div class="toolbar-search-wrap">
              <i class="fa-solid fa-magnifying-glass toolbar-search-icon"></i>
              <input type="search" class="toolbar-search-input" placeholder="Search members...">
            </div>
            <select class="toolbar-select"><option>All Wards</option><option>Ward 1</option></select>
            <select class="toolbar-select"><option>All Roles</option><option>Field Officer</option></select>
            <select class="toolbar-select"><option>Active</option><option>Inactive</option></select>
          </div>
          
          <div class="ticket-table-wrap">
            <table class="ticket-table">
              <thead>
                <tr>
                  <th>NAME & CONTACT</th>
                  <th>ROLE</th>
                  <th>ASSIGNED WARD</th>
                  <th>ISSUES RESOLVED</th>
                  <th>PERFORMANCE</th>
                  <th>STATUS</th>
                  <th>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <div class="user-cell">
                      <div class="avatar bg-blue">R</div>
                      <div>
                        <strong>Ramesh Kumar</strong>
                        <div class="text-sub">+91 9876543210</div>
                      </div>
                    </div>
                  </td>
                  <td>Field Officer</td>
                  <td>Ward 12, Kothrud</td>
                  <td>145 / 160</td>
                  <td><span class="text-success">92%</span> Excellent</td>
                  <td><span class="status-chip chip-success">Active</span></td>
                  <td>
                    <a href="team-member-details.html" class="icon-btn" style="color: var(--text-1);"><i class="fa-solid fa-eye"></i></a>
                    <a href="team-member-edit.html" class="icon-btn" style="color: var(--text-1); margin-left: 8px;"><i class="fa-solid fa-pen"></i></a>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div class="user-cell">
                      <div class="avatar bg-purple">A</div>
                      <div>
                        <strong>Anita Sharma</strong>
                        <div class="text-sub">+91 9123456789</div>
                      </div>
                    </div>
                  </td>
                  <td>Coordinator</td>
                  <td>Ward 4, Shivaji Nagar</td>
                  <td>89 / 120</td>
                  <td><span class="text-warning">74%</span> Good</td>
                  <td><span class="status-chip chip-success">Active</span></td>
                  <td>
                    <a href="team-member-details.html" class="icon-btn" style="color: var(--text-1);"><i class="fa-solid fa-eye"></i></a>
                    <a href="team-member-edit.html" class="icon-btn" style="color: var(--text-1); margin-left: 8px;"><i class="fa-solid fa-pen"></i></a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="pagination" style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; color: var(--text-2); font-size: 12px;">
             <span>Showing 1-10 of 45</span>
             <div class="page-controls" style="display: flex; gap: 4px;">
                <button disabled style="background: var(--surface-1); border: 1px solid var(--border-soft); color: var(--text-2); padding: 4px 8px; border-radius: 4px;"><i class="fa-solid fa-chevron-left"></i></button>
                <button class="active" style="background: var(--cyan); border: none; color: #000; padding: 4px 8px; border-radius: 4px;">1</button>
                <button style="background: var(--surface-1); border: 1px solid var(--border-soft); color: var(--text-2); padding: 4px 8px; border-radius: 4px;">2</button>
                <button style="background: var(--surface-1); border: 1px solid var(--border-soft); color: var(--text-2); padding: 4px 8px; border-radius: 4px;">3</button>
                <button style="background: var(--surface-1); border: 1px solid var(--border-soft); color: var(--text-2); padding: 4px 8px; border-radius: 4px;"><i class="fa-solid fa-chevron-right"></i></button>
             </div>
          </div>
        </section>
        """
    },
    'citizens.html': {
        'title': 'Citizen Database',
        'active_link': './citizens.html',
        'content': """
        <section class="page-intro">
          <div>
            <h2 class="page-intro-title">Voter & Citizen Directory</h2>
            <div class="page-intro-copy">Comprehensive database of constituents, their history, and intelligence profiles.</div>
          </div>
          <div class="page-intro-actions">
            <button class="action-button button-outline"><i class="fa-solid fa-download"></i> Export</button>
          </div>
        </section>
        
        <section class="page-grid grid-4 mb-4" style="margin-bottom: 24px;">
          <div class="panel kpi-card" style="display: flex; gap: 16px; align-items: center;">
            <div class="kpi-icon" style="font-size: 24px; color: var(--blue); background: rgba(47, 109, 243, 0.1); padding: 12px; border-radius: 50%;"><i class="fa-solid fa-users"></i></div>
            <div class="kpi-content">
              <div class="kpi-label" style="font-size: 10px; color: var(--text-2); text-transform: uppercase;">Total Citizens</div>
              <div class="kpi-val" style="font-size: 24px; font-weight: bold; color: var(--text-0);">1,245,670</div>
            </div>
          </div>
          <div class="panel kpi-card" style="display: flex; gap: 16px; align-items: center;">
            <div class="kpi-icon" style="font-size: 24px; color: var(--purple); background: rgba(168, 92, 255, 0.1); padding: 12px; border-radius: 50%;"><i class="fa-solid fa-id-card"></i></div>
            <div class="kpi-content">
              <div class="kpi-label" style="font-size: 10px; color: var(--text-2); text-transform: uppercase;">Verified Voters</div>
              <div class="kpi-val" style="font-size: 24px; font-weight: bold; color: var(--text-0);">985,432</div>
            </div>
          </div>
          <div class="panel kpi-card" style="display: flex; gap: 16px; align-items: center;">
            <div class="kpi-icon" style="font-size: 24px; color: var(--amber); background: rgba(247, 178, 19, 0.1); padding: 12px; border-radius: 50%;"><i class="fa-solid fa-bullhorn"></i></div>
            <div class="kpi-content">
              <div class="kpi-label" style="font-size: 10px; color: var(--text-2); text-transform: uppercase;">Active Complainants</div>
              <div class="kpi-val" style="font-size: 24px; font-weight: bold; color: var(--text-0);">12,450</div>
            </div>
          </div>
          <div class="panel kpi-card" style="display: flex; gap: 16px; align-items: center;">
            <div class="kpi-icon" style="font-size: 24px; color: var(--cyan); background: rgba(29, 200, 238, 0.1); padding: 12px; border-radius: 50%;"><i class="fa-solid fa-repeat"></i></div>
            <div class="kpi-content">
              <div class="kpi-label" style="font-size: 10px; color: var(--text-2); text-transform: uppercase;">Repeat Complaints</div>
              <div class="kpi-val" style="font-size: 24px; font-weight: bold; color: var(--text-0);">3,210</div>
            </div>
          </div>
        </section>

        <section class="panel table-panel">
          <div class="table-toolbar">
            <div class="toolbar-search-wrap">
              <i class="fa-solid fa-magnifying-glass toolbar-search-icon"></i>
              <input type="search" class="toolbar-search-input" placeholder="Search by name, phone, or Voter ID...">
            </div>
            <select class="toolbar-select"><option>All Wards</option><option>Ward 1</option></select>
            <select class="toolbar-select"><option>All Sentiments</option><option>Positive</option><option>Negative</option></select>
          </div>
          
          <div class="ticket-table-wrap">
            <table class="ticket-table">
              <thead>
                <tr>
                  <th>VOTER ID</th>
                  <th>CITIZEN NAME</th>
                  <th>CONTACT</th>
                  <th>WARD / BOOTH</th>
                  <th>COMPLAINTS</th>
                  <th>AI SENTIMENT</th>
                  <th>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>MH/14/085/123456</strong></td>
                  <td>
                    <div class="user-cell">
                      <div class="avatar bg-blue">S</div>
                      <div>
                        <strong>Suresh Patel</strong>
                        <div class="text-sub">Pune Metro Area</div>
                      </div>
                    </div>
                  </td>
                  <td>+91 9988776655</td>
                  <td>Ward 12<br><small class="text-sub">Booth #45</small></td>
                  <td>3 (1 Open)</td>
                  <td><span class="status-chip chip-warning" style="background: rgba(247, 178, 19, 0.15); color: var(--amber); border: 1px solid rgba(247, 178, 19, 0.3);">Frustrated</span></td>
                  <td><a href="citizen-details.html" class="action-button small-button button-outline">Profile</a></td>
                </tr>
                <tr>
                  <td><strong>MH/14/085/654321</strong></td>
                  <td>
                    <div class="user-cell">
                      <div class="avatar bg-purple">M</div>
                      <div>
                        <strong>Meera Deshmukh</strong>
                        <div class="text-sub">Kothrud Area</div>
                      </div>
                    </div>
                  </td>
                  <td>+91 9911223344</td>
                  <td>Ward 4<br><small class="text-sub">Booth #12</small></td>
                  <td>1 (Resolved)</td>
                  <td><span class="status-chip chip-success">Satisfied</span></td>
                  <td><a href="citizen-details.html" class="action-button small-button button-outline">Profile</a></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        """
    },
    'complaint-details.html': {
        'title': 'Complaint Intelligence',
        'active_link': './war-room.html',
        'content': """
        <div class="breadcrumb" style="margin-bottom: 24px; font-size: 12px; color: var(--text-2);">
           <a href="war-room.html" style="color: var(--cyan); text-decoration: none;">War Room</a> &rsaquo; <span style="color: var(--text-0);">Ticket #TKT-2026-8901</span>
        </div>
        
        <section class="page-grid grid-two-wide">
          <!-- Left Column: Details -->
          <div class="details-column">
             <div class="panel ticket-header-panel mb-4" style="margin-bottom: 24px;">
                <div class="flex-between mb-3" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                   <div class="ticket-id-large" style="font-size: 24px; font-weight: bold; color: var(--cyan);">TKT-2026-8901</div>
                   <div class="ticket-badges" style="display: flex; gap: 8px;">
                      <span class="status-chip chip-warning" style="background: rgba(247, 178, 19, 0.15); color: var(--amber); border: 1px solid rgba(247, 178, 19, 0.3);"><i class="fa-solid fa-clock"></i> Open</span>
                      <span class="status-chip chip-critical" style="background: rgba(255, 90, 95, 0.15); color: var(--red); border: 1px solid rgba(255, 90, 95, 0.3);"><i class="fa-solid fa-fire"></i> Critical</span>
                   </div>
                </div>
                <h2 class="ticket-title" style="margin: 0; font-size: 20px; line-height: 1.4;">Severe water logging and drainage overflow on Main Street</h2>
                <div class="ticket-meta mt-3" style="margin-top: 16px; display: flex; gap: 16px; color: var(--text-2); font-size: 12px;">
                   <span><i class="fa-solid fa-location-dot"></i> Ward 12, Kothrud</span>
                   <span><i class="fa-solid fa-calendar"></i> Reported: 2 hours ago</span>
                   <span><i class="fa-solid fa-building"></i> Dept: Public Works</span>
                </div>
             </div>

             <div class="panel ai-summary-panel mb-4" style="margin-bottom: 24px; background: linear-gradient(135deg, rgba(30, 35, 68, 0.6), rgba(16, 18, 58, 0.8)); border: 1px solid rgba(168, 92, 255, 0.4);">
                <div class="panel-header mb-3" style="margin-bottom: 16px;">
                   <div class="chart-title"><i class="fa-solid fa-brain" style="color: var(--purple);"></i> AI Intelligence Summary</div>
                </div>
                <div class="ai-summary-content">
                   <p class="ai-text" style="font-size: 14px; line-height: 1.6; color: var(--text-0);"><strong>Analysis:</strong> The citizen is reporting acute drainage failure leading to water logging. Sentiment is highly frustrated. Similar issues have been reported 3 times in this 500m radius in the last month.</p>
                   <div class="ai-suggestions mt-3" style="margin-top: 24px; display: flex; gap: 16px;">
                      <div class="ai-suggestion-box" style="flex: 1; background: var(--surface-1); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-soft);">
                         <span class="ai-label" style="display: block; font-size: 10px; color: var(--text-2); text-transform: uppercase; margin-bottom: 4px;">Suggested Dept</span>
                         <strong style="color: var(--text-0); font-size: 13px;">Municipal Drainage Dept</strong>
                      </div>
                      <div class="ai-suggestion-box" style="flex: 1; background: var(--surface-1); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-soft);">
                         <span class="ai-label" style="display: block; font-size: 10px; color: var(--text-2); text-transform: uppercase; margin-bottom: 4px;">SLA Risk</span>
                         <strong style="color: var(--red); font-size: 13px;">High (Rain forecasted)</strong>
                      </div>
                      <div class="ai-suggestion-box" style="flex: 1; background: var(--surface-1); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-soft);">
                         <span class="ai-label" style="display: block; font-size: 10px; color: var(--text-2); text-transform: uppercase; margin-bottom: 4px;">Priority Action</span>
                         <strong style="color: var(--text-0); font-size: 13px;">Dispatch vacuum truck immediately</strong>
                      </div>
                   </div>
                </div>
             </div>

             <div class="panel mb-4" style="margin-bottom: 24px;">
                <div class="panel-header mb-3" style="margin-bottom: 16px;"><div class="chart-title">Attachments & Evidence</div></div>
                <div class="media-gallery" style="display: flex; gap: 16px;">
                   <div class="media-item" style="width: 120px; height: 120px; background: var(--surface-1); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--text-2);"><i class="fa-solid fa-image"></i></div>
                   <div class="media-item" style="width: 120px; height: 120px; background: var(--surface-1); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--text-2);"><i class="fa-solid fa-image"></i></div>
                   <div class="media-item" style="width: 120px; height: 120px; background: var(--surface-1); border: 1px dashed var(--cyan); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; flex-direction: column; font-size: 12px; color: var(--cyan); cursor: pointer;"><i class="fa-solid fa-cloud-arrow-up" style="font-size: 24px; margin-bottom: 8px;"></i> Upload</div>
                </div>
             </div>
             
             <div class="panel mb-4" style="margin-bottom: 24px;">
                <div class="panel-header flex-between mb-3" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                   <div class="chart-title">Possible Duplicates Detected</div>
                   <span class="badge" style="background: rgba(255, 90, 95, 0.15); color: var(--red); padding: 4px 8px; border-radius: 12px; font-size: 11px; border: 1px solid rgba(255, 90, 95, 0.3);">1 Match</span>
                </div>
                <div class="duplicate-warning p-3 rounded-md border-soft flex-between" style="background: var(--surface-2); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-soft); display: flex; justify-content: space-between; align-items: center;">
                   <div>
                      <strong style="display: block; margin-bottom: 4px;">TKT-2026-8850</strong>
                      <span style="font-size: 13px; color: var(--text-1);">Drainage block near Kothrud Depot (85% Similarity)</span>
                   </div>
                   <button class="action-button button-outline small-button" onclick="document.getElementById('duplicateModal').classList.remove('hidden')">Review & Merge</button>
                </div>
             </div>
          </div>

          <!-- Right Column: Timeline & Citizen Info -->
          <div class="sidebar-column">
             <div class="panel mb-4" style="margin-bottom: 24px;">
                <div class="panel-header mb-3" style="margin-bottom: 16px;"><div class="chart-title">Citizen Details</div></div>
                <div class="citizen-mini-profile">
                   <div class="user-cell mb-3" style="display: flex; gap: 12px; align-items: center; margin-bottom: 16px;">
                      <div class="avatar bg-blue" style="width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: var(--blue); color: #fff; font-weight: bold;">S</div>
                      <div>
                        <strong style="display: block; font-size: 14px;">Suresh Patel</strong>
                        <div class="text-sub" style="font-size: 12px; color: var(--text-2);">+91 9988776655</div>
                      </div>
                   </div>
                   <div class="citizen-stats" style="font-size: 13px;">
                      <div class="stat-row flex-between mb-2" style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Total Complaints:</span> <strong>3</strong></div>
                      <div class="stat-row flex-between mb-2" style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Voter Status:</span> <strong style="color: var(--green);">Verified</strong></div>
                      <a href="citizen-details.html" class="action-button button-outline" style="width: 100%; display: block; text-align: center; margin-top: 16px;">View Full Profile</a>
                   </div>
                </div>
             </div>

             <div class="panel timeline-panel">
                <div class="panel-header mb-3" style="margin-bottom: 16px;"><div class="chart-title">Resolution Timeline</div></div>
                <div class="vertical-timeline">
                   <div class="timeline-item active">
                      <div class="timeline-marker"><i class="fa-solid fa-file-signature"></i></div>
                      <div class="timeline-content">
                         <h5>Complaint Registered</h5>
                         <span class="time">Today, 10:30 AM</span>
                         <p>Citizen submitted via Mobile App</p>
                      </div>
                   </div>
                   <div class="timeline-item active">
                      <div class="timeline-marker"><i class="fa-solid fa-brain"></i></div>
                      <div class="timeline-content">
                         <h5>AI Triage Completed</h5>
                         <span class="time">Today, 10:31 AM</span>
                         <p>Routed to Public Works (Severity: Critical)</p>
                      </div>
                   </div>
                   <div class="timeline-item pending">
                      <div class="timeline-marker" style="background: var(--surface-1); border-color: var(--border-soft);"><i class="fa-solid fa-hard-hat"></i></div>
                      <div class="timeline-content" style="opacity: 0.6;">
                         <h5>Department Acceptance</h5>
                         <span class="time">Pending</span>
                      </div>
                   </div>
                   <div class="timeline-item pending">
                      <div class="timeline-marker" style="background: var(--surface-1); border-color: var(--border-soft);"><i class="fa-solid fa-truck"></i></div>
                      <div class="timeline-content" style="opacity: 0.6;">
                         <h5>Field Officer Dispatched</h5>
                         <span class="time">Pending</span>
                      </div>
                   </div>
                </div>
                
                <div class="timeline-actions" style="margin-top: 24px; border-top: 1px solid var(--border-soft); padding-top: 16px;">
                   <select class="toolbar-select" style="width: 100%; margin-bottom: 12px;"><option>Update Status...</option><option>Accept Issue</option><option>Mark In-Progress</option></select>
                   <textarea class="form-input" style="width: 100%; margin-bottom: 12px; background: var(--surface-1); border: 1px solid var(--border-soft); color: var(--text-0); padding: 8px; border-radius: var(--radius-sm);" rows="3" placeholder="Add internal remark..."></textarea>
                   <button class="action-button button-blue" style="width: 100%;">Post Update</button>
                </div>
             </div>
          </div>
        </section>
        
        <!-- Duplicate Review Modal -->
        <div id="duplicateModal" class="modal-overlay hidden">
           <div class="modal-box w-large" style="background: var(--bg-1); width: 700px; max-width: 90%; border-radius: var(--radius-md); border: 1px solid var(--border-soft); box-shadow: var(--shadow-lg);">
              <div class="modal-header" style="padding: 16px 24px; border-bottom: 1px solid var(--border-soft); display: flex; justify-content: space-between; align-items: center;">
                 <h3 style="margin: 0;">Merge Duplicate Complaints</h3>
                 <button class="modal-close" style="background: none; border: none; color: var(--text-1); cursor: pointer; font-size: 18px;" onclick="document.getElementById('duplicateModal').classList.add('hidden')"><i class="fa-solid fa-xmark"></i></button>
              </div>
              <div class="modal-body" style="padding: 24px;">
                 <div class="duplicate-comparison-grid grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                    <div class="panel border-soft" style="padding: 16px; border-radius: var(--radius-sm);">
                       <span class="badge bg-blue mb-2" style="display: inline-block; padding: 4px 8px; background: rgba(47, 109, 243, 0.2); color: var(--blue); border-radius: 4px; font-size: 11px; margin-bottom: 12px;">Original (Existing)</span>
                       <h4 style="margin: 0 0 8px;">TKT-2026-8850</h4>
                       <p style="margin: 0; font-size: 13px; color: var(--text-1);">Drainage block near Kothrud Depot</p>
                       <div class="text-sub mt-2" style="margin-top: 12px; font-size: 11px; color: var(--text-2);">Reported by: Ramesh (Yesterday)</div>
                    </div>
                    <div class="panel border-soft" style="padding: 16px; border-radius: var(--radius-sm); border-color: var(--cyan); background: rgba(29, 200, 238, 0.05);">
                       <span class="badge bg-cyan mb-2 text-dark" style="display: inline-block; padding: 4px 8px; background: var(--cyan); color: #000; border-radius: 4px; font-size: 11px; margin-bottom: 12px;">New (Current)</span>
                       <h4 style="margin: 0 0 8px;">TKT-2026-8901</h4>
                       <p style="margin: 0; font-size: 13px; color: var(--text-1);">Severe water logging and drainage overflow on Main Street</p>
                       <div class="text-sub mt-2" style="margin-top: 12px; font-size: 11px; color: var(--text-2);">Reported by: Suresh (Today)</div>
                    </div>
                 </div>
                 <div class="similarity-score text-center mt-4 mb-4" style="text-align: center; margin: 32px 0;">
                    <div class="score-circle" style="width: 80px; height: 80px; border-radius: 50%; border: 4px solid var(--purple); color: var(--purple); display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; margin: 0 auto 12px; box-shadow: 0 0 20px rgba(168, 92, 255, 0.3);">85%</div>
                    <div style="font-size: 13px; color: var(--text-1);">AI Similarity Confidence</div>
                 </div>
              </div>
              <div class="modal-footer flex-end gap-3" style="padding: 16px 24px; border-top: 1px solid var(--border-soft); display: flex; justify-content: flex-end; gap: 16px;">
                 <button class="action-button button-outline" onclick="document.getElementById('duplicateModal').classList.add('hidden')">Keep Separate</button>
                 <button class="action-button button-blue" style="background: var(--purple); color: #fff; border: none; padding: 8px 16px; border-radius: var(--radius-sm); cursor: pointer;" onclick="document.getElementById('duplicateModal').classList.add('hidden')"><i class="fa-solid fa-code-merge"></i> Merge into Original</button>
              </div>
           </div>
        </div>
        """
    },
    'executive-brief.html': {
        'title': 'AI Executive Brief',
        'active_link': './executive-brief.html',
        'content': """
        <section class="page-grid grid-two-wide mb-4" style="margin-bottom: 24px;">
          <!-- Left: AI Summary -->
          <div class="panel ai-brief-panel" style="background: linear-gradient(135deg, rgba(30, 35, 68, 0.9), rgba(16, 18, 58, 0.95)); border: 1px solid var(--purple);">
             <div class="panel-header mb-3" style="margin-bottom: 16px;">
                <div class="chart-title"><i class="fa-solid fa-sparkles" style="color: var(--purple);"></i> Daily Synthesis (07 Aug 2026)</div>
             </div>
             <p class="font-section text-0" style="line-height: 1.6; font-size: 16px; color: var(--text-0);">
                Good Morning. Over the last 24 hours, constituency health has declined by <strong style="color: var(--red);">2.4%</strong> due to a spike in water-related issues in Ward 12. 
                Public Works resolved 45 issues yesterday, but 12 critical SLA breaches remain. 
                <br><br>
                <strong style="color: var(--cyan);">Recommendation:</strong> Prioritize an inspection visit to Kothrud today to address constituent unrest.
             </p>
             <div style="display: flex; gap: 16px; margin-top: 32px;">
                <button class="action-button button-purple" style="background: var(--purple); color: #fff; border: none; padding: 10px 20px; border-radius: var(--radius-sm); cursor: pointer; font-weight: 600;"><i class="fa-solid fa-calendar-check"></i> Auto-Schedule Ward Visit</button>
                <button class="action-button button-outline" style="background: transparent; color: var(--text-0); border: 1px solid var(--border-soft); padding: 10px 20px; border-radius: var(--radius-sm); cursor: pointer;"><i class="fa-solid fa-file-pdf"></i> Download PDF Brief</button>
             </div>
          </div>
          
          <!-- Right: Critical KPIs -->
          <div class="grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
             <div class="panel kpi-card bg-surface-1 border-soft" style="padding: 16px; display: flex; flex-direction: column; justify-content: center;">
               <div class="kpi-icon" style="font-size: 20px; color: var(--red); margin-bottom: 8px;"><i class="fa-solid fa-fire"></i></div>
               <div class="kpi-content">
                 <div class="kpi-label" style="font-size: 11px; color: var(--text-2); text-transform: uppercase;">New Critical Issues</div>
                 <div class="kpi-val text-red" style="font-size: 28px; font-weight: bold; color: var(--red);">24</div>
                 <div class="text-sub mt-1" style="font-size: 11px; color: var(--text-2); margin-top: 4px;"><i class="fa-solid fa-arrow-up"></i> 12% vs yesterday</div>
               </div>
             </div>
             <div class="panel kpi-card bg-surface-1 border-soft" style="padding: 16px; display: flex; flex-direction: column; justify-content: center;">
               <div class="kpi-icon" style="font-size: 20px; color: var(--amber); margin-bottom: 8px;"><i class="fa-solid fa-clock"></i></div>
               <div class="kpi-content">
                 <div class="kpi-label" style="font-size: 11px; color: var(--text-2); text-transform: uppercase;">SLA Breaches</div>
                 <div class="kpi-val text-amber" style="font-size: 28px; font-weight: bold; color: var(--amber);">12</div>
                 <div class="text-sub mt-1" style="font-size: 11px; color: var(--text-2); margin-top: 4px;">Pending > 48hrs</div>
               </div>
             </div>
             <div class="panel kpi-card bg-surface-1 border-soft" style="padding: 16px; display: flex; flex-direction: column; justify-content: center;">
               <div class="kpi-icon" style="font-size: 20px; color: var(--green); margin-bottom: 8px;"><i class="fa-solid fa-check-double"></i></div>
               <div class="kpi-content">
                 <div class="kpi-label" style="font-size: 11px; color: var(--text-2); text-transform: uppercase;">Issues Resolved</div>
                 <div class="kpi-val text-success" style="font-size: 28px; font-weight: bold; color: var(--green);">145</div>
                 <div class="text-sub mt-1" style="font-size: 11px; color: var(--text-2); margin-top: 4px;">Last 24 hours</div>
               </div>
             </div>
             <div class="panel kpi-card bg-surface-1 border-soft" style="padding: 16px; display: flex; flex-direction: column; justify-content: center;">
               <div class="kpi-icon" style="font-size: 20px; color: var(--blue); margin-bottom: 8px;"><i class="fa-solid fa-face-smile"></i></div>
               <div class="kpi-content">
                 <div class="kpi-label" style="font-size: 11px; color: var(--text-2); text-transform: uppercase;">Public Sentiment</div>
                 <div class="kpi-val text-blue" style="font-size: 28px; font-weight: bold; color: var(--blue);">54%</div>
                 <div class="text-sub mt-1" style="font-size: 11px; color: var(--text-2); margin-top: 4px;">Neutral / Positive</div>
               </div>
             </div>
          </div>
        </section>
        
        <section class="page-grid grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
           <div class="panel">
              <div class="panel-header"><div class="chart-title">AI Resource Allocation Suggestions</div></div>
              <ul class="suggestion-list mt-3" style="list-style: none; padding: 0; margin-top: 16px;">
                 <li style="padding: 16px; margin-bottom: 12px; background: var(--surface-2); border-radius: var(--radius-sm); border: 1px solid var(--border-soft); display: flex; justify-content: space-between; align-items: center;">
                    <div>
                       <strong style="color: var(--text-0); font-size: 14px;">Shift 2 garbage trucks to Ward 4</strong>
                       <p style="margin: 4px 0 0; font-size: 12px; color: var(--text-2);">Predicted spike in waste volume due to festival.</p>
                    </div>
                    <button class="action-button small-button button-blue" style="background: var(--blue); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer;">Approve</button>
                 </li>
                 <li style="padding: 16px; margin-bottom: 12px; background: var(--surface-2); border-radius: var(--radius-sm); border: 1px solid var(--border-soft); display: flex; justify-content: space-between; align-items: center;">
                    <div>
                       <strong style="color: var(--text-0); font-size: 14px;">Deploy extra field officers to Ward 12</strong>
                       <p style="margin: 4px 0 0; font-size: 12px; color: var(--text-2);">Water logging SLA breaches are accumulating.</p>
                    </div>
                    <button class="action-button small-button button-blue" style="background: var(--blue); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer;">Approve</button>
                 </li>
              </ul>
           </div>
           <div class="panel">
              <div class="panel-header"><div class="chart-title">Priority Schedule / Suggested Visits</div></div>
              <ul class="suggestion-list mt-3" style="list-style: none; padding: 0; margin-top: 16px;">
                 <li style="padding: 16px; margin-bottom: 12px; background: var(--surface-2); border-radius: var(--radius-sm); border: 1px solid var(--border-soft); display: flex; justify-content: flex-start; gap: 16px; align-items: flex-start;">
                    <div style="text-align: center; padding: 8px 12px; background: var(--surface-3); border-radius: 4px; min-width: 70px;">
                       <strong style="display: block; font-size: 12px; color: var(--cyan);">10:00 AM</strong>
                    </div>
                    <div>
                       <strong style="color: var(--text-0); font-size: 14px;">Visit Kothrud Main Street</strong>
                       <p style="margin: 4px 0 0; font-size: 12px; color: var(--text-2);">Address ongoing water logging complaints. High visibility area.</p>
                    </div>
                 </li>
                 <li style="padding: 16px; margin-bottom: 12px; background: var(--surface-2); border-radius: var(--radius-sm); border: 1px solid var(--border-soft); display: flex; justify-content: flex-start; gap: 16px; align-items: flex-start;">
                    <div style="text-align: center; padding: 8px 12px; background: var(--surface-3); border-radius: 4px; min-width: 70px;">
                       <strong style="display: block; font-size: 12px; color: var(--cyan);">02:00 PM</strong>
                    </div>
                    <div>
                       <strong style="color: var(--text-0); font-size: 14px;">Review meeting with Public Works Dept</strong>
                       <p style="margin: 4px 0 0; font-size: 12px; color: var(--text-2);">Address 12 SLA breaches in road repairs.</p>
                    </div>
                 </li>
              </ul>
           </div>
        </section>
        """
    }
}

for filename, data in pages_data.items():
    create_page(filename, data['title'], data['content'], data['active_link'])

# Ensure all additional requested files get basic scaffolds based on the same pattern
extra_files = [
    ('team-member-add.html', 'Add Team Member', 'team-members.html'),
    ('team-member-edit.html', 'Edit Team Member', 'team-members.html'),
    ('team-member-details.html', 'Member Details', 'team-members.html'),
    ('team-member-performance.html', 'Member Performance', 'team-members.html'),
    ('citizen-details.html', 'Citizen Profile', 'citizens.html'),
    ('health-dashboard.html', 'Constituency Health', 'health-dashboard.html'),
    ('ward-health.html', 'Ward Intelligence', 'ward-health.html'),
    ('ward-comparison.html', 'Ward Comparison', 'ward-comparison.html'),
    ('reports.html', 'Reports Center', 'reports.html'),
    ('settings.html', 'Settings', 'settings.html'),
    ('activity-logs.html', 'Activity Logs', 'activity-logs.html'),
    ('system-monitoring.html', 'System Monitoring', 'system-monitoring.html'),
    ('error-403.html', '403 Forbidden', ''),
    ('error-404.html', '404 Not Found', ''),
    ('error-500.html', '500 Server Error', '')
]

skeleton_content = """
<div class="page-intro" style="margin-bottom: 24px;">
  <div>
    <h2 class="page-intro-title">{title}</h2>
    <div class="page-intro-copy">This page has been successfully scaffolded and is fully styled within the Mahanaayak OS design system.</div>
  </div>
</div>
<section class="page-grid grid-3" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; margin-bottom: 24px;">
    <div class="panel skeleton-card" style="height: 200px;"></div>
    <div class="panel skeleton-card" style="height: 200px;"></div>
    <div class="panel skeleton-card" style="height: 200px;"></div>
</section>
<section class="panel table-panel">
    <div class="panel-header"><div class="chart-title">Data Loading...</div></div>
    <div class="skeleton-table" style="height: 300px; margin-top: 24px;"></div>
</section>
"""

for fn, title, active_link in extra_files:
    if fn not in pages_data:
        create_page(fn, title, skeleton_content.replace('{title}', title), active_link)

# Write CSS updates
css_updates = """
/* Component Updates for New Modules */

/* Skeleton Loading */
.skeleton-card, .skeleton-table, .skeleton-img {
  background: linear-gradient(90deg, var(--surface-1) 25%, var(--surface-2) 50%, var(--surface-1) 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: var(--radius-md);
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Vertical Timeline */
.vertical-timeline {
  position: relative;
  padding-left: 30px;
}
.vertical-timeline::before {
  content: '';
  position: absolute;
  top: 0; left: 14px;
  height: 100%; width: 2px;
  background: var(--surface-3);
}
.timeline-item {
  position: relative;
  margin-bottom: var(--space-5);
}
.timeline-marker {
  position: absolute;
  left: -30px;
  width: 30px; height: 30px;
  border-radius: 50%;
  background: var(--surface-2);
  border: 2px solid var(--surface-3);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px;
  color: var(--text-2);
  z-index: 1;
}
.timeline-item.active .timeline-marker {
  background: var(--bg-1);
  border-color: var(--cyan);
  color: var(--cyan);
  box-shadow: var(--glow-cyan);
}
.timeline-content h5 { margin: 0 0 4px; font-size: 14px; color: var(--text-0); }
.timeline-content .time { font-size: 10px; color: var(--text-2); display: block; margin-bottom: 8px;}
.timeline-content p { margin: 0; font-size: 12px; color: var(--text-1); }

/* Global Drawers & Modals */
.drawer-overlay, .modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(9, 12, 39, 0.85);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
}
.modal-overlay { justify-content: center; align-items: center; }
.drawer-overlay { justify-content: flex-end; }
.drawer {
  width: 400px; max-width: 100%;
  background: var(--bg-1);
  border-left: 1px solid var(--border-soft);
  height: 100%;
  display: flex; flex-direction: column;
  box-shadow: var(--shadow-lg);
  animation: slideInRight 0.3s ease;
}
@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
.drawer-header {
  padding: var(--space-4);
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid var(--border-soft);
}
.drawer-header h3 { margin: 0; font-size: 18px; display: flex; gap: 8px; align-items: center; color: var(--text-0); }
.drawer-close { background: transparent; border: none; color: var(--text-1); font-size: 18px; cursor: pointer; }
.drawer-tabs { display: flex; border-bottom: 1px solid var(--border-soft); }
.drawer-tabs .tab-btn { flex: 1; background: transparent; border: none; border-bottom: 2px solid transparent; padding: 12px; color: var(--text-1); cursor: pointer; }
.drawer-tabs .tab-btn.active { color: var(--cyan); border-bottom-color: var(--cyan); }
.drawer-body {
  flex: 1; padding: var(--space-4); overflow-y: auto;
}
.drawer-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--border-soft);
}
.hidden { display: none !important; }

/* Notification Items */
.notification-item {
  display: flex; gap: 12px;
  padding: 12px; border-radius: var(--radius-sm);
  background: var(--surface-0);
  margin-bottom: 8px; border: 1px solid transparent;
}
.notification-item.critical { border-color: rgba(255, 90, 95, 0.3); background: rgba(255, 90, 95, 0.05); }
.notif-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.critical .notif-icon { background: rgba(255, 90, 95, 0.2); color: var(--red); }
.warning .notif-icon { background: rgba(247, 178, 19, 0.2); color: var(--amber); }
.success .notif-icon { background: rgba(30, 201, 141, 0.2); color: var(--green); }
.notif-content h4 { margin: 0 0 4px; font-size: 13px; color: var(--text-0); }
.notif-content p { margin: 0 0 4px; font-size: 11px; color: var(--text-2); }
.notif-time { font-size: 10px; color: var(--text-3); }

/* Global Search Palette */
.search-palette-modal {
  width: 600px; max-width: 90%;
  background: var(--bg-1);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  margin-top: -15vh;
}
.search-input-wrap {
  display: flex; align-items: center; padding: 16px 24px;
  border-bottom: 1px solid var(--border-soft);
}
.search-input-wrap .search-icon { color: var(--text-1); font-size: 20px; }
.search-input-wrap input {
  flex: 1; background: transparent; border: none; outline: none;
  color: var(--text-0); font-size: 18px; margin-left: 12px;
}
.search-input-wrap .esc-btn { background: var(--surface-2); border: 1px solid var(--border-soft); color: var(--text-2); padding: 4px 8px; border-radius: 4px; font-size: 10px; cursor: pointer; }
.search-results {
  padding: 16px 24px; max-height: 400px; overflow-y: auto;
}
.search-result-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px; border-radius: var(--radius-sm);
  color: var(--text-1); text-decoration: none;
}
.search-result-item:hover { background: var(--surface-1); color: var(--text-0); }
.search-group h5 { margin: 0 0 12px; color: var(--text-2); font-size: 11px; text-transform: uppercase; }

"""

with open(os.path.join(css_dir, 'components.css'), 'a', encoding='utf-8') as f:
    f.write(css_updates)

# JS Updates for Modals
js_updates = """
// Global Drawer & Modal Logic
document.addEventListener('DOMContentLoaded', () => {
    // Notification Drawer
    const notifTrigger = document.querySelector('.notification-trigger');
    const drawer = document.getElementById('notificationsDrawer');
    const drawerClose = document.querySelector('.drawer-close');
    
    if(notifTrigger && drawer) {
        notifTrigger.addEventListener('click', () => drawer.classList.remove('hidden'));
        drawerClose.addEventListener('click', () => drawer.classList.add('hidden'));
    }
    
    // Search Palette
    const searchTrigger = document.querySelector('.search-trigger');
    const searchPalette = document.getElementById('searchPalette');
    
    if(searchTrigger && searchPalette) {
        searchTrigger.addEventListener('click', () => {
            searchPalette.classList.remove('hidden');
            searchPalette.querySelector('input').focus();
        });
        
        searchPalette.addEventListener('click', (e) => {
            if(e.target === searchPalette) searchPalette.classList.add('hidden');
        });
        
        document.addEventListener('keydown', (e) => {
            if(e.key === 'Escape') searchPalette.classList.add('hidden');
            if(e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                searchPalette.classList.remove('hidden');
                searchPalette.querySelector('input').focus();
            }
        });
    }
});
"""

with open(os.path.join(js_dir, 'app.js'), 'a', encoding='utf-8') as f:
    f.write(js_updates)

print("HTML generation complete.")
