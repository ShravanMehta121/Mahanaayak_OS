/**
 * MAHANAYAK OS — Chart.js Engine & Analytics Renderer
 * Renders smooth interactive charts with chartjs-plugin-datalabels, 
 * doughnut center total metrics, 58% cutout, and responsive layouts.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (window.Chart && window.ChartDataLabels) {
    Chart.register(window.ChartDataLabels);
  }
  initWarRoomCharts();
  initDepartmentCharts();
});

// Plugin to draw center text inside Doughnut charts
const centerTextPlugin = {
  id: 'centerTextPlugin',
  afterDraw(chart) {
    if (chart.config.type !== 'doughnut') return;
    const centerConfig = chart.config.options.plugins.centerText;
    if (!centerConfig) return;

    const { ctx, chartArea } = chart;
    if (!chartArea) return;
    const { top, bottom, left, right } = chartArea;

    ctx.save();

    const text = centerConfig.text || '';
    const label = centerConfig.label || '';

    const centerX = (left + right) / 2;
    const centerY = (top + bottom) / 2;

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Draw main value
    ctx.font = 'bold 22px "Segoe UI", sans-serif';
    ctx.fillStyle = '#7be3ff';
    ctx.fillText(text, centerX, centerY - 6);

    // Draw sublabel
    ctx.font = '9px "Segoe UI", sans-serif';
    ctx.fillStyle = '#adb3d2';
    ctx.fillText(label, centerX, centerY + 14);

    ctx.restore();
  }
};

if (window.Chart) {
  Chart.register(centerTextPlugin);
}

function initWarRoomCharts() {
  const severityEl = document.getElementById('severityChart');
  const deptEl = document.getElementById('deptChart');
  const statusEl = document.getElementById('statusChart');

  if (!severityEl && !deptEl && !statusEl) return;

  const commonPieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 800,
      easing: 'easeOutQuart'
    },
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: '#adb3d2',
          boxWidth: 10,
          boxHeight: 10,
          font: { size: 10, family: 'Segoe UI' },
          padding: 8
        }
      },
      tooltip: {
        backgroundColor: '#10123a',
        titleColor: '#f4f7ff',
        bodyColor: '#adb3d2',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        padding: 10
      },
      datalabels: {
        color: '#ffffff',
        font: { weight: 'bold', size: 10 },
        formatter: (value, ctx) => {
          const datasets = ctx.chart.data.datasets;
          if (datasets.length) {
            const total = datasets[0].data.reduce((a, b) => a + b, 0);
            const percentage = Math.round((value / total) * 100);
            return percentage > 6 ? `${percentage}%` : '';
          }
          return value;
        }
      }
    }
  };

  // 1. Severity Doughnut
  if (severityEl && window.Chart) {
    if (Chart.getChart(severityEl)) Chart.getChart(severityEl).destroy();

    new Chart(severityEl, {
      type: 'doughnut',
      data: {
        labels: ['Critical', 'High', 'Medium', 'Low'],
        datasets: [{
          data: [20, 28, 34, 18],
          backgroundColor: ['#ff5a5f', '#f7b213', '#a85cff', '#2f6df3'],
          borderWidth: 2,
          borderColor: '#14163e',
          hoverOffset: 6
        }]
      },
      options: {
        ...commonPieOptions,
        cutout: '58%',
        plugins: {
          ...commonPieOptions.plugins,
          centerText: { text: '100', label: 'TICKETS' }
        }
      }
    });
  }

  // 2. Department Doughnut
  if (deptEl && window.Chart) {
    if (Chart.getChart(deptEl)) Chart.getChart(deptEl).destroy();

    new Chart(deptEl, {
      type: 'doughnut',
      data: {
        labels: ['Utilities', 'Public Works', 'Energy', 'Health', 'Municipal Corp (PMC)'],
        datasets: [{
          data: [28, 22, 21, 21, 8],
          backgroundColor: ['#a85cff', '#1dc8ee', '#1ec98d', '#ff5a5f', '#7e86a8'],
          borderWidth: 2,
          borderColor: '#14163e',
          hoverOffset: 6
        }]
      },
      options: {
        ...commonPieOptions,
        cutout: '58%',
        plugins: {
          ...commonPieOptions.plugins,
          centerText: { text: '5 DEPT', label: 'LOAD' }
        }
      }
    });
  }

  // 3. Status Doughnut
  if (statusEl && window.Chart) {
    if (Chart.getChart(statusEl)) Chart.getChart(statusEl).destroy();

    new Chart(statusEl, {
      type: 'doughnut',
      data: {
        labels: ['Open', 'Pending', 'Closed'],
        datasets: [{
          data: [55, 22, 23],
          backgroundColor: ['#1ec98d', '#f7b213', '#ff5a5f'],
          borderWidth: 2,
          borderColor: '#14163e',
          hoverOffset: 6
        }]
      },
      options: {
        ...commonPieOptions,
        cutout: '58%',
        plugins: {
          ...commonPieOptions.plugins,
          centerText: { text: '77%', label: 'ACTIVE' }
        }
      }
    });
  }
}

function initDepartmentCharts() {
  const barEl = document.getElementById('deptBarChart');
  const lineEl = document.getElementById('turnaroundLineChart');
  const radarEl = document.getElementById('severityRadarChart');

  if (!barEl && !lineEl && !radarEl) return;

  const chartBase = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 800,
      easing: 'easeOutQuart'
    },
    plugins: {
      legend: {
        labels: { color: '#adb3d2', font: { size: 10, family: 'Segoe UI' } }
      },
      tooltip: {
        backgroundColor: '#10123a',
        titleColor: '#f4f7ff',
        bodyColor: '#adb3d2',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1
      },
      datalabels: { display: false }
    },
    scales: {
      x: {
        ticks: { color: '#adb3d2', font: { size: 10 } },
        grid: { color: 'rgba(255,255,255,0.04)' }
      },
      y: {
        ticks: { color: '#adb3d2', font: { size: 10 } },
        grid: { color: 'rgba(255,255,255,0.04)' }
      }
    }
  };

  // 1. Horizontal Stacked Bar
  if (barEl && window.Chart) {
    if (Chart.getChart(barEl)) Chart.getChart(barEl).destroy();

    new Chart(barEl, {
      type: 'bar',
      data: {
        labels: ['Public Works', 'Utilities', 'Municipal Corp (PMC)', 'Energy', 'Health'],
        datasets: [
          { label: 'Unassigned/Open', data: [10, 4, 1, 7, 2], backgroundColor: '#f7b213', borderRadius: 4, stack: 'stack1' },
          { label: 'In Progress/Pending', data: [1, 6, 0, 2, 0], backgroundColor: '#2f6df3', borderRadius: 4, stack: 'stack1' },
          { label: 'Resolved/Closed', data: [2, 2, 0, 1, 8], backgroundColor: '#1ec98d', borderRadius: 4, stack: 'stack1' }
        ]
      },
      options: {
        ...chartBase,
        indexAxis: 'y',
        plugins: {
          ...chartBase.plugins,
          legend: {
            position: 'bottom',
            labels: { color: '#adb3d2', boxWidth: 12, font: { size: 10 } }
          }
        },
        scales: {
          x: { stacked: true, ticks: { color: '#adb3d2', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' } },
          y: { stacked: true, ticks: { color: '#adb3d2', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.04)' } }
        }
      }
    });
  }

  // 2. Line Chart
  if (lineEl && window.Chart) {
    if (Chart.getChart(lineEl)) Chart.getChart(lineEl).destroy();

    new Chart(lineEl, {
      type: 'line',
      data: {
        labels: ['Public Works', 'Utilities', 'Municipal Corp (PMC)', 'Energy', 'Health'],
        datasets: [{
          label: 'Actual Resolution Speed (Days)',
          data: [0.9, 0.9, 0.2, 0.9, 0.2],
          borderColor: '#1dc8ee',
          backgroundColor: 'rgba(29, 200, 238, 0.12)',
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#1dc8ee',
          pointRadius: 4
        }]
      },
      options: {
        ...chartBase,
        plugins: {
          ...chartBase.plugins,
          legend: { position: 'bottom', labels: { color: '#adb3d2', font: { size: 10 } } }
        }
      }
    });
  }

  // 3. Radar Chart
  if (radarEl && window.Chart) {
    if (Chart.getChart(radarEl)) Chart.getChart(radarEl).destroy();

    new Chart(radarEl, {
      type: 'radar',
      data: {
        labels: ['Public Works', 'Utilities', 'Municipal Corp (PMC)', 'Energy', 'Health'],
        datasets: [
          {
            label: 'Critical Risk',
            data: [8, 5, 2, 6, 3],
            borderColor: '#ff5a5f',
            backgroundColor: 'rgba(255, 90, 95, 0.18)',
            pointBackgroundColor: '#ff5a5f'
          },
          {
            label: 'High Risk',
            data: [6, 8, 3, 4, 5],
            borderColor: '#f7b213',
            backgroundColor: 'rgba(247, 178, 19, 0.18)',
            pointBackgroundColor: '#f7b213'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: chartBase.plugins,
        scales: {
          r: {
            angleLines: { color: 'rgba(255,255,255,0.08)' },
            grid: { color: 'rgba(255,255,255,0.08)' },
            pointLabels: { color: '#adb3d2', font: { size: 10 } },
            ticks: { display: false }
          }
        }
      }
    });
  }
}

window.frontendCharts = {
  initialize() {
    initWarRoomCharts();
    initDepartmentCharts();
  }
};
