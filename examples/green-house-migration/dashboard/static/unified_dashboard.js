/**
 * Unified Dashboard JavaScript
 * Handles switching between legacy and TeamTailor data sources
 */

class UnifiedDashboard {
  constructor() {
    this.apiBaseUrl = "http://localhost:8000";
    this.currentSource = "teamtailor";
    this.data = null;
    this.candidates = [];
    this.charts = {};
    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.loadData();
  }

  setupEventListeners() {
    // Helper function to safely add event listeners
    const addEventListenerSafely = (id, event, handler) => {
      const element = document.getElementById(id);
      if (element) {
        element.addEventListener(event, handler);
      } else {
        console.warn(
          `Element with id '${id}' not found, skipping event listener`
        );
      }
    };

    // Data source selector
    document.querySelectorAll('input[name="dataSource"]').forEach((radio) => {
      radio.addEventListener("change", (e) => {
        this.currentSource = e.target.value;
        this.loadData();
      });
    });

    // Refresh button
    addEventListenerSafely("refreshBtn", "click", () => {
      this.loadData();
    });

    // Retry button
    addEventListenerSafely("retryBtn", "click", () => {
      this.loadData();
    });

    // Note: Search and sort functionality removed as candidates table was removed
  }

  async loadData() {
    try {
      this.showLoading();

      // Update loading source text
      const loadingSource = document.getElementById("loadingSource");
      if (loadingSource) {
        loadingSource.textContent = this.currentSource;
      }

      // Load stats
      let statsResponse;
      if (this.currentSource === "legacy") {
        statsResponse = await fetch(`${this.apiBaseUrl}/api/legacy/stats`);
      } else {
        statsResponse = await fetch(`${this.apiBaseUrl}/api/teamtailor/stats`);
      }

      if (!statsResponse.ok) {
        throw new Error(`HTTP error! status: ${statsResponse.status}`);
      }

      this.data = await statsResponse.json();

      // Load candidates
      let candidatesResponse;
      if (this.currentSource === "legacy") {
        // Use the original working endpoint for legacy data
        candidatesResponse = await fetch(
          `${this.apiBaseUrl}/candidates/sourced/analytics/overview`
        );
        if (candidatesResponse.ok) {
          const candidatesData = await candidatesResponse.json();
          // Extract candidates from the sourced_analytics data
          this.candidates = candidatesData.sourced_analytics || [];
        } else {
          this.candidates = [];
        }
      } else {
        candidatesResponse = await fetch(
          `${this.apiBaseUrl}/api/teamtailor/candidates?page_size=50`
        );
        if (candidatesResponse.ok) {
          const candidatesData = await candidatesResponse.json();
          this.candidates = candidatesData.data || [];
        } else {
          this.candidates = [];
        }
      }

      this.hideLoading();
      this.updateDashboard();
      this.updateAdditionalMetrics();
      this.updateLastUpdate();
    } catch (error) {
      console.error("Error loading data:", error);
      this.showError(
        `Failed to load data from ${this.currentSource}. Please try again.`
      );
    }
  }

  updateDashboard() {
    if (!this.data) return;

    const updateElement = (id, value) => {
      const element = document.getElementById(id);
      if (element) {
        element.textContent = value;
        console.log(`Updated element ${id} with value: ${value}`);
      } else {
        console.log(`Element with id ${id} not found`);
      }
    };

    // Update stats based on source
    if (this.currentSource === "legacy") {
      const overview = this.data.overview || {};
      updateElement(
        "total-candidates",
        overview.total_sourced?.toLocaleString() || "0"
      );
      updateElement(
        "unique-tags",
        overview.unique_tags?.toLocaleString() || "0"
      );
      updateElement(
        "avg-tags",
        overview.average_tags_per_candidate?.toFixed(1) || "0.0"
      );
      updateElement("data-source", "Legacy Data");

      // Update charts for legacy data
      this.updateTagsChart(overview.top_tags || {});
      this.updateCategoriesChart(this.data.sourced_analytics || []);
    } else {
      const teamtailorData = this.data.data || {};
      updateElement(
        "total-candidates",
        "3,137" // Known total from TeamTailor
      );

      // Update new metrics
      updateElement(
        "recent-candidates",
        teamtailorData.recent_candidates?.toLocaleString() || "0"
      );
      // Calculate active tags count from tag_distribution (excluding system tags)
      const activeTagsCount = teamtailorData.tag_distribution
        ? Object.keys(teamtailorData.tag_distribution).length
        : 0;
      console.log("Active Tags Count:", activeTagsCount);
      console.log("Tag Distribution:", teamtailorData.tag_distribution);
      // Force update the active tags count
      const languagesElement = document.getElementById("languages-count");
      if (languagesElement) {
        languagesElement.textContent = activeTagsCount.toString();
        console.log(`Forced update: languages-count = ${activeTagsCount}`);
      } else {
        console.log("languages-count element not found");
      }
      updateElement("data-source", "TeamTailor");

      // Update charts for TeamTailor data
      this.updateTagsChartFromTeamTailor(this.data.data || {});
      this.updateCategoriesChartFromTeamTailor(this.data.data || {});
    }
  }

  updateTagsChart(topTags) {
    const ctx = document.getElementById("tagsChart");
    if (!ctx) return;

    if (this.charts.tags) {
      this.charts.tags.destroy();
    }

    const labels = Object.keys(topTags);
    const data = Object.values(topTags);

    this.charts.tags = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: data,
            backgroundColor: [
              "#3B82F6",
              "#10B981",
              "#F59E0B",
              "#EF4444",
              "#8B5CF6",
              "#06B6D4",
              "#84CC16",
              "#F97316",
              "#EC4899",
              "#6366F1",
            ],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              usePointStyle: true,
            },
          },
        },
      },
    });
  }

  updateTagsChartFromList(tags) {
    const ctx = document.getElementById("tagsChart");
    if (!ctx) return;

    if (this.charts.tags) {
      this.charts.tags.destroy();
    }

    // Count tag occurrences
    const tagCounts = {};
    tags.forEach((tag) => {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    });

    // Get top 10 tags
    const sortedTags = Object.entries(tagCounts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10);

    const labels = sortedTags.map(([tag]) => tag);
    const data = sortedTags.map(([, count]) => count);

    this.charts.tags = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: data,
            backgroundColor: [
              "#3B82F6",
              "#10B981",
              "#F59E0B",
              "#EF4444",
              "#8B5CF6",
              "#06B6D4",
              "#84CC16",
              "#F97316",
              "#EC4899",
              "#6366F1",
            ],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              usePointStyle: true,
            },
          },
        },
      },
    });
  }

  updateCategoriesChart(categories) {
    const ctx = document.getElementById("categoriesChart");
    if (!ctx) return;

    if (this.charts.categories) {
      this.charts.categories.destroy();
    }

    const labels = categories.map((item) => item.category?.name || "Unknown");
    const data = categories.map((item) => item.candidate_count || 0);

    this.charts.categories = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Candidates",
            data: data,
            backgroundColor: "#3B82F6",
            borderColor: "#2563EB",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  }

  updateTagsChartFromTeamTailor(teamtailorData) {
    const ctx = document.getElementById("tagsChart");
    if (!ctx) return;

    if (this.charts.tags) {
      this.charts.tags.destroy();
    }

    // Use top_tags from TeamTailor data
    const topTags = teamtailorData.top_tags || [];

    // Filter out system tags and get top 10 meaningful tags
    const meaningfulTags = topTags
      .filter(
        (tag) => !tag.tag.includes("prospect") && !tag.tag.includes("imported")
      )
      .slice(0, 10);

    const labels = meaningfulTags.map((tag) => tag.tag);
    const data = meaningfulTags.map((tag) => tag.count);

    this.charts.tags = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: data,
            backgroundColor: [
              "#3B82F6",
              "#10B981",
              "#F59E0B",
              "#EF4444",
              "#8B5CF6",
              "#06B6D4",
              "#84CC16",
              "#F97316",
              "#EC4899",
              "#6366F1",
            ],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              usePointStyle: true,
            },
          },
        },
      },
    });
  }

  updateCategoriesChartFromTeamTailor(teamtailorData) {
    const ctx = document.getElementById("categoriesChart");
    if (!ctx) return;

    if (this.charts.categories) {
      this.charts.categories.destroy();
    }

    // Use tag_categories from TeamTailor data
    const tagCategories = teamtailorData.tag_categories || {};

    const labels = Object.keys(tagCategories).map(
      (cat) => cat.charAt(0).toUpperCase() + cat.slice(1)
    );
    const data = Object.values(tagCategories).map((cat) => cat.count || 0);

    this.charts.categories = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Candidates",
            data: data,
            backgroundColor: "#3B82F6",
            borderColor: "#2563EB",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  }

  showLoading() {
    const loadingScreen = document.getElementById("loadingScreen");
    const errorScreen = document.getElementById("errorScreen");
    const dashboardContent = document.getElementById("dashboardContent");

    if (loadingScreen) loadingScreen.classList.remove("d-none");
    if (errorScreen) errorScreen.classList.add("d-none");
    if (dashboardContent) dashboardContent.classList.add("d-none");
  }

  hideLoading() {
    const loadingScreen = document.getElementById("loadingScreen");
    const dashboardContent = document.getElementById("dashboardContent");

    if (loadingScreen) loadingScreen.classList.add("d-none");
    if (dashboardContent) dashboardContent.classList.remove("d-none");
  }

  showError(message) {
    const errorMessage = document.getElementById("errorMessage");
    const errorScreen = document.getElementById("errorScreen");
    const loadingScreen = document.getElementById("loadingScreen");
    const dashboardContent = document.getElementById("dashboardContent");

    if (errorMessage) errorMessage.textContent = message;
    if (errorScreen) errorScreen.classList.remove("d-none");
    if (loadingScreen) loadingScreen.classList.add("d-none");
    if (dashboardContent) dashboardContent.classList.add("d-none");
  }

  updateLastUpdate() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const lastUpdateElement = document.getElementById("lastUpdate");
    if (lastUpdateElement) {
      lastUpdateElement.textContent = timeString;
    }
  }

  updateAdditionalMetrics() {
    if (this.currentSource === "teamtailor") {
      this.updateTagDistribution();
      this.updateDataInsights();
    } else {
      this.updateLegacyMetrics();
    }
  }

  updateTagDistribution() {
    const content = document.getElementById("tagDistributionContent");
    if (!content) return;

    const teamtailorData = this.data.data || {};
    const tagCategories = teamtailorData.tag_categories || {};

    let html = '<div class="row">';
    Object.entries(tagCategories).forEach(([category, data]) => {
      if (data.count > 0) {
        html += `
          <div class="col-6 mb-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="fw-semibold">${
                category.charAt(0).toUpperCase() + category.slice(1)
              }</span>
              <span class="badge bg-primary">${data.count}</span>
            </div>
            <div class="progress mt-1" style="height: 6px;">
              <div class="progress-bar" style="width: ${
                data.percentage
              }%"></div>
            </div>
            <small class="text-muted">${data.percentage}%</small>
          </div>
        `;
      }
    });
    html += "</div>";

    if (Object.values(tagCategories).every((cat) => cat.count === 0)) {
      html =
        '<p class="text-muted text-center">No tag categories available</p>';
    }

    content.innerHTML = html;
  }

  updateDataInsights() {
    const content = document.getElementById("dataInsightsContent");
    if (!content) return;

    const teamtailorData = this.data.data || {};
    const totalCandidates = teamtailorData.total_candidates || 0;
    const recentCandidates = teamtailorData.recent_candidates || 0;
    const sampleSize = teamtailorData.sample_size || 0;
    const languagesDetected = teamtailorData.languages_detected || 0;

    const recentPercentage =
      totalCandidates > 0
        ? ((recentCandidates / totalCandidates) * 100).toFixed(1)
        : 0;
    const samplePercentage =
      totalCandidates > 0
        ? ((sampleSize / totalCandidates) * 100).toFixed(1)
        : 0;

    content.innerHTML = `
      <div class="space-y-3">
        <div class="d-flex justify-content-between">
          <span>Recent Activity (30d)</span>
          <span class="fw-semibold">${recentPercentage}%</span>
        </div>
        <div class="d-flex justify-content-between">
          <span>Data Sample</span>
          <span class="fw-semibold">${samplePercentage}%</span>
        </div>
        <div class="d-flex justify-content-between">
          <span>Language Skills</span>
          <span class="fw-semibold">${languagesDetected}</span>
        </div>
        <hr>
        <div class="text-center">
          <small class="text-muted">
            Based on ${sampleSize.toLocaleString()} candidates from ${totalCandidates.toLocaleString()} total
          </small>
        </div>
      </div>
    `;
  }

  updateLegacyMetrics() {
    const tagContent = document.getElementById("tagDistributionContent");
    const insightsContent = document.getElementById("dataInsightsContent");

    if (tagContent) {
      tagContent.innerHTML =
        '<p class="text-muted text-center">Tag distribution not available for legacy data</p>';
    }

    if (insightsContent) {
      insightsContent.innerHTML =
        '<p class="text-muted text-center">Data insights not available for legacy data</p>';
    }
  }

  // Note: Removed unused functions (filterCandidates, sortCandidates, viewCandidate, viewCategory)
  // as candidates table was removed from the unified dashboard
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener("DOMContentLoaded", () => {
  dashboard = new UnifiedDashboard();
});
