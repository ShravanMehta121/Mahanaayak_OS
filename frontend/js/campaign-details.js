/**
 * MAHANAYAK OS — Campaign Planner Analytics & Modal Content Data
 * Attaches interactive click behavior to campaign strategy cards on admin/campaign.html.
 */

document.addEventListener('DOMContentLoaded', () => {
  initCampaignCards();
});

function initCampaignCards() {
  const cards = document.querySelectorAll('.campaign-card');

  cards.forEach((card, index) => {
    // Make cards visibly hoverable and clickable
    card.style.cursor = 'pointer';

    card.addEventListener('click', () => {
      openCampaignModal(index);
    });
  });
}

function openCampaignModal(index) {
  if (!window.Modal) return;

  const modals = [
    getExecutiveOutlookModal(),
    getManifestoModal(),
    getResourceAllocatorModal(),
    getCreativeHookModal()
  ];

  const data = modals[index] || modals[0];
  window.Modal.open(data);
}

function getExecutiveOutlookModal() {
  return {
    title: '<i class="fa-solid fa-chart-line brand-accent"></i> Executive Outlook & Strategic AI Audit',
    contentHtml: `
      <div class="modal-section">
        <div class="modal-section-title">Problem Summary & Current Situation</div>
        <div class="modal-card-box">
          <p><strong>Primary Challenge:</strong> Citizen grievance response times in Ward 12 & 14 have escalated by 18.4% due to utility pipeline leakages and delayed PWD road surfacing during monsoon prep.</p>
          <p><strong>AI Sentiment Analysis:</strong> Neutral-Negative (54.2% discontent in water distribution, 28.1% positive on street lighting resolution).</p>
        </div>
      </div>

      <div class="modal-grid-two">
        <div class="modal-card-box">
          <div class="modal-section-title">Affected Constituencies & Demographics</div>
          <ul>
            <li><strong>Shivajinagar & Shanivar Peth:</strong> Middle-income residents, shopkeepers (58,400 voters).</li>
            <li><strong>Wakad & Hinjawadi:</strong> IT professionals, young families (92,100 voters).</li>
            <li><strong>Viman Nagar & Katraj:</strong> Students, commercial trade workers (41,200 voters).</li>
          </ul>
        </div>

        <div class="modal-card-box">
          <div class="modal-section-title">Key Complaints & Root Cause</div>
          <ul>
            <li><strong>Main pipe leakages:</strong> Aging 12-year PVC infrastructure.</li>
            <li><strong>Unpaved road cuts:</strong> Disjointed contractor handovers between PMC and Utilities.</li>
            <li><strong>Political Risk Factor:</strong> High opposition mobilization around urban infrastructure.</li>
          </ul>
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">Recommended AI Speech & Talking Points</div>
        <div class="modal-speech-box">
          "Our administration is shifting Pune from reactive repairs to predictive governance. With MAHANAYAK OS, we track every pipe, every road cut, and every streetlight in real time — guaranteeing 48-hour SLA resolution for every family in this constituency."
        </div>
      </div>

      <div class="modal-grid-three">
        <div class="modal-card-box">
          <div class="modal-stat-num">98.4%</div>
          <div class="modal-stat-label">AI Telemetry Accuracy</div>
        </div>
        <div class="modal-card-box">
          <div class="modal-stat-num">48 Hrs</div>
          <div class="modal-stat-label">Target Resolution SLA</div>
        </div>
        <div class="modal-card-box">
          <div class="modal-stat-num">+14.2%</div>
          <div class="modal-stat-label">Projected Voter Retention</div>
        </div>
      </div>
    `
  };
}

function getManifestoModal() {
  return {
    title: '<i class="fa-solid fa-book-open brand-accent"></i> Manifesto Foundations & Ward Guarantees',
    contentHtml: `
      <div class="modal-grid-two">
        <div class="modal-card-box">
          <div class="modal-section-title">Key Manifesto Promises</div>
          <ul>
            <li><strong>24/7 Water Pressure Guarantee:</strong> Complete pipe grid upgrade across 14 wards within 180 days.</li>
            <li><strong>Zero-Pothole Ward Corridor:</strong> Instant 24-hour asphalt patch dispatch via mobile citizen portal.</li>
            <li><strong>Solar-Powered Smart Lighting:</strong> Installation of 1,200 smart LED poles with CCTV coverage.</li>
          </ul>
        </div>

        <div class="modal-card-box">
          <div class="modal-section-title">Budget & Timeline Breakdown</div>
          <ul>
            <li><strong>Estimated Budget:</strong> ₹42.5 Crore (Allocated via State Urban Dev Grant).</li>
            <li><strong>Implementation Timeline:</strong> Phase I (Wards 1–6): 45 Days | Phase II (Wards 7–14): 90 Days.</li>
            <li><strong>Feasibility Score:</strong> 94.2% (High execution probability).</li>
          </ul>
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">Impact Analysis & Vote Projection</div>
        <div class="modal-card-box">
          <p><strong>Expected Votes Gained:</strong> +18,500 swing voters across key urban polling stations.</p>
          <p><strong>Ward Coverage:</strong> 100% of Pune Metro urban wards covered with real-time issue tracking.</p>
          <p><strong>AI Confidence Score:</strong> 91.8% based on historical ward voter sentiment models.</p>
        </div>
      </div>
    `
  };
}

function getResourceAllocatorModal() {
  return {
    title: '<i class="fa-solid fa-layer-group brand-accent"></i> Resource Allocator & Campaign Deployment',
    contentHtml: `
      <div class="modal-grid-three">
        <div class="modal-card-box">
          <div class="modal-stat-num">450+</div>
          <div class="modal-stat-label">Active Field Volunteers</div>
        </div>
        <div class="modal-card-box">
          <div class="modal-stat-num">18</div>
          <div class="modal-stat-label">Mobile Campaign Vans</div>
        </div>
        <div class="modal-card-box">
          <div class="modal-stat-num">14</div>
          <div class="modal-stat-label">Ward Ground Teams</div>
        </div>
      </div>

      <div class="modal-grid-two">
        <div class="modal-card-box">
          <div class="modal-section-title">Ward Allocation Strategy</div>
          <ul>
            <li><strong>High Severity Wards (Ward 2, 5, 11):</strong> 60% volunteer density, daily door-to-door canvas.</li>
            <li><strong>Medium Severity Wards (Ward 1, 3, 8):</strong> 30% volunteer density, weekly town halls.</li>
            <li><strong>Low Severity Wards (Ward 4, 7, 10):</strong> Digital campaign focus and automated SMS alerts.</li>
          </ul>
        </div>

        <div class="modal-card-box">
          <div class="modal-section-title">Risk Matrix & Deployment Schedule</div>
          <ul>
            <li><strong>Schedule:</strong> 6-week intensive deployment culminating 48h before polling.</li>
            <li><strong>Risk Mitigation:</strong> Standby rapid response team for counter-narratives within 30 minutes.</li>
          </ul>
        </div>
      </div>

      <div class="modal-section">
        <button class="action-button primary-button" type="button" onclick="if(window.Toast) window.Toast.success('Campaign Strategy exported as PDF report.');"><i class="fa-solid fa-download"></i> Export Deployment Strategy PDF</button>
      </div>
    `
  };
}

function getCreativeHookModal() {
  return {
    title: '<i class="fa-solid fa-wand-magic-sparkles brand-accent"></i> Creative Hook & AI Campaign Prompts',
    contentHtml: `
      <div class="modal-section">
        <div class="modal-section-title">Campaign Slogans & Taglines</div>
        <div class="modal-card-box">
          <p><strong>Primary Slogan:</strong> "KamBol, KaamBol — Technology Meets Governance."</p>
          <p><strong>Secondary Slogan:</strong> "Your Issue, Our Action — Resolved in 48 Hours."</p>
        </div>
      </div>

      <div class="modal-grid-two">
        <div class="modal-card-box">
          <div class="modal-section-title">Social Media Captions & Hashtags</div>
          <p>"Every pipeline fixed, every street illuminated. Experience transparent leadership with MAHANAYAK OS."</p>
          <p><code>#MahanayakOS #PuneProgress #SmartGovernance #ZeroPotholePune</code></p>
        </div>

        <div class="modal-card-box">
          <div class="modal-section-title">Instagram & Poster Concepts</div>
          <ul>
            <li><strong>Poster 1:</strong> Split screen showing reported issue vs 24h resolved status.</li>
            <li><strong>Reels Concept:</strong> 15-second time-lapse of pothole filling team deployed via app.</li>
          </ul>
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">AI Generative Prompts (Images & Video)</div>
        <div class="modal-card-box">
          <p><strong>AI Image Prompt:</strong> <em>"Ultra-realistic cinematic shot of a modern Indian city ward with clean roads, bright smart LED streetlights, glowing cyan holographic data overlays representing civic governance, 8k resolution."</em></p>
          <p><strong>AI Video Prompt:</strong> <em>"Dynamic drone shot panning across Pune cityscape at dusk transitioning to a sleek AI command war room with multi-screen analytics graphs."</em></p>
        </div>
      </div>
    `
  };
}

window.CampaignDetails = {
  openModal: openCampaignModal
};
