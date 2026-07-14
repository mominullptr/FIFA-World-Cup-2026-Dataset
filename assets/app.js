document.addEventListener("DOMContentLoaded", () => {
  // Check if DATA_PREVIEWS exists globally
  if (typeof DATA_PREVIEWS === "undefined") {
    console.error("DATA_PREVIEWS data was not loaded.");
    return;
  }

  // Helper to resolve assets path relative to the page
  const getAssetPath = (filename) => {
    return "assets/" + filename;
  };

  // Column name overrides / formatting helpers
  const formatHeaderName = (colName) => {
    return colName
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const previewTable = document.getElementById("preview-table");
  const tabButtons = document.querySelectorAll(".tab-btn");

  const renderTable = (category) => {
    if (!previewTable) return;
    
    // Clear existing
    previewTable.innerHTML = "";
    
    const records = DATA_PREVIEWS[category];
    if (!records || records.length === 0) {
      previewTable.innerHTML = "<thead><tr><th>No Data</th></tr></thead><tbody><tr><td>No preview records available.</td></tr></tbody>";
      return;
    }

    // Get columns
    const columns = Object.keys(records[0]);

    // Create header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    columns.forEach((col) => {
      const th = document.createElement("th");
      th.textContent = formatHeaderName(col);
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    previewTable.appendChild(thead);

    // Create body
    const tbody = document.createElement("tbody");
    records.forEach((record) => {
      const row = document.createElement("tr");
      columns.forEach((col) => {
        const td = document.createElement("td");
        td.textContent = record[col] !== null && record[col] !== undefined ? record[col] : "";
        row.appendChild(td);
      });
      tbody.appendChild(row);
    });
    previewTable.appendChild(tbody);
  };

  // Add click listeners to tabs
  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Deactivate all
      tabButtons.forEach((b) => b.classList.remove("active"));
      // Activate this
      btn.classList.add("active");
      // Get category
      const category = btn.getAttribute("data-category");
      // Render
      renderTable(category);
    });
  });

  // Render initial table (matches)
  const activeTab = document.querySelector(".tab-btn.active");
  if (activeTab) {
    renderTable(activeTab.getAttribute("data-category"));
  }

  // Smooth scroll scroll-to-top function
  const scrollTopBtn = document.getElementById("scroll-top-btn");
  if (scrollTopBtn) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 500) {
        scrollTopBtn.style.opacity = "1";
        scrollTopBtn.style.pointerEvents = "auto";
      } else {
        scrollTopBtn.style.opacity = "0";
        scrollTopBtn.style.pointerEvents = "none";
      }
    });

    scrollTopBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Database Schema zoom modal handling
  const schemaContainer = document.getElementById("schema-container");
  const schemaModal = document.getElementById("schema-modal");
  const schemaClose = document.getElementById("schema-close");

  if (schemaContainer && schemaModal && schemaClose) {
    schemaContainer.addEventListener("click", () => {
      schemaModal.style.display = "block";
      document.body.style.overflow = "hidden"; // Disable scroll when modal is open
    });

    const closeModal = () => {
      schemaModal.style.display = "none";
      document.body.style.overflow = "auto"; // Re-enable scroll
    };

    schemaClose.addEventListener("click", closeModal);
    schemaModal.addEventListener("click", (e) => {
      if (e.target === schemaModal || e.target.classList.contains("modal-content-wrap")) {
        closeModal();
      }
    });

    // Close on escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && schemaModal.style.display === "block") {
        closeModal();
      }
    });
  }

  // BibTeX Citation Clipboard Copy handling
  const copyCitationBtn = document.getElementById("btn-copy-citation");
  const bibtextContent = document.getElementById("bibtex-content");

  if (copyCitationBtn && bibtextContent) {
    copyCitationBtn.addEventListener("click", () => {
      const textToCopy = bibtextContent.textContent;
      
      navigator.clipboard.writeText(textToCopy).then(() => {
        // Successful copy feedback
        const originalHTML = copyCitationBtn.innerHTML;
        copyCitationBtn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="#00f5d4" stroke-width="2.5" width="14" height="14">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span style="color:#00f5d4">Copied!</span>
        `;
        copyCitationBtn.style.borderColor = "rgba(0, 245, 212, 0.4)";
        copyCitationBtn.style.background = "rgba(0, 245, 212, 0.08)";
        
        setTimeout(() => {
          copyCitationBtn.innerHTML = originalHTML;
          copyCitationBtn.style.borderColor = "";
          copyCitationBtn.style.background = "";
        }, 2000);
      }).catch(err => {
        console.error("Failed to copy BibTeX citation: ", err);
      });
    });
  }

  // Lottie Animation Logo Initialization
  const logoContainer = document.getElementById("logo-lottie");
  if (logoContainer && typeof lottie !== "undefined") {
    lottie.loadAnimation({
      container: logoContainer,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: getAssetPath('fifa-world-cup.json')
    });
  }

  // Video Background Loading
  const bgVideo = document.getElementById("bg-video");
  if (bgVideo) {
    const source = document.createElement("source");
    source.src = getAssetPath('From Klickpin.com- Gentle devotional ideas for people who love beauty for creative people to begin the day well-pin-id-627337423130563852.mp4');
    source.type = "video/mp4";
    bgVideo.appendChild(source);
    bgVideo.load();
    bgVideo.play().catch(() => {});
    
    bgVideo.addEventListener("playing", () => {
      bgVideo.classList.add("loaded");
    });

    // Pause video when page is hidden to optimize performance and save battery/CPU
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        bgVideo.pause();
      } else {
        bgVideo.play().catch(() => {});
      }
    });
  }

  // ML predictions loading and rendering
  const predictionsContainer = document.getElementById("predictions-container");
  if (predictionsContainer) {
    fetch(getAssetPath("predictions.json"))
      .then(res => {
        if (!res.ok) throw new Error("Predictions file not found");
        return res.json();
      })
      .then(data => {
        const getFlagPath = (teamName) => {
          const cleanName = teamName.toLowerCase().trim();
          if (cleanName === "spain") return getAssetPath("spain.png");
          if (cleanName === "argentina") return getAssetPath("argentina.png");
          if (cleanName === "france") return getAssetPath("france.png");
          if (cleanName === "england") return getAssetPath("england.png");
          return null;
        };

        predictionsContainer.innerHTML = "";
        
        Object.values(data).forEach(pred => {
          const matchCard = document.createElement("div");
          matchCard.className = "glass-card prediction-match-card";
          matchCard.style.padding = "2rem";
          matchCard.style.position = "relative";
          matchCard.style.overflow = "hidden";
          
          const homeProbPct = Math.round(pred.home_prob * 100);
          const drawProbPct = Math.round(pred.draw_prob * 100);
          const awayProbPct = Math.round(pred.away_prob * 100);
          const advProbPct = Math.round(pred.advancing_prob * 100);
          
          const homeAbbr = pred.home_fifa_code || pred.home_team.slice(0, 3).toUpperCase();
          const awayAbbr = pred.away_fifa_code || pred.away_team.slice(0, 3).toUpperCase();
          
          const homeFlag = getFlagPath(pred.home_team);
          const awayFlag = getFlagPath(pred.away_team);

          const homeFlagHTML = homeFlag 
            ? `<img src="${homeFlag}" alt="${pred.home_team} Flag" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:1px solid rgba(255,255,255,0.15); margin:0 auto 0.75rem auto; display:block;">`
            : `<div class="team-flag-placeholder" style="width:50px; height:50px; border-radius:50%; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); margin:0 auto 0.75rem auto; display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:800; color:var(--text-primary);">${homeAbbr}</div>`;

          const awayFlagHTML = awayFlag 
            ? `<img src="${awayFlag}" alt="${pred.away_team} Flag" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:1px solid rgba(255,255,255,0.15); margin:0 auto 0.75rem auto; display:block;">`
            : `<div class="team-flag-placeholder" style="width:50px; height:50px; border-radius:50%; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); margin:0 auto 0.75rem auto; display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:800; color:var(--text-primary);">${awayAbbr}</div>`;

          matchCard.innerHTML = `
            <div class="match-meta" style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem; color:var(--text-secondary); margin-bottom:1.5rem; border-bottom:1px solid rgba(255,255,255,0.06); padding-bottom:1rem;">
              <span>Match ${pred.match_id} • ${pred.date}</span>
              <span class="venue-badge" style="background:rgba(255,255,255,0.05); padding:2px 8px; border-radius:10px;">${pred.venue.split(",")[0]}</span>
            </div>
            
            <div class="matchup-container" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem; gap:1rem;">
              <div class="team-side home" style="flex:1; text-align:center;">
                ${homeFlagHTML}
                <h4 style="font-family:var(--font-title); font-size:1.15rem; font-weight:700; margin:0 0 0.25rem 0; color:#fff;">${pred.home_team}</h4>
                <div class="team-meta" style="font-size:0.75rem; color:var(--text-secondary);">Rank: ${pred.home_fifa_rank} | Elo: ${Math.round(pred.home_elo)}</div>
              </div>
              
              <div class="score-center" style="text-align:center; padding:0 1rem;">
                <div class="predicted-score" style="font-family:var(--font-title); font-size:2.25rem; font-weight:900; color:var(--primary-gold); letter-spacing:4px; margin-bottom:0.25rem;">
                  ${pred.predicted_home_score} - ${pred.predicted_away_score}
                </div>
                <div class="predicted-score-label" style="font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); font-weight:700;">Predicted Score</div>
                <div class="predicted-xg" style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.5rem;">
                  <span style="color:var(--text-primary); font-weight:600;">${pred.home_predicted_xg.toFixed(2)}</span> vs <span style="color:var(--text-primary); font-weight:600;">${pred.away_predicted_xg.toFixed(2)}</span> xG
                </div>
              </div>
              
              <div class="team-side away" style="flex:1; text-align:center;">
                ${awayFlagHTML}
                <h4 style="font-family:var(--font-title); font-size:1.15rem; font-weight:700; margin:0 0 0.25rem 0; color:#fff;">${pred.away_team}</h4>
                <div class="team-meta" style="font-size:0.75rem; color:var(--text-secondary);">Rank: ${pred.away_fifa_rank} | Elo: ${Math.round(pred.away_elo)}</div>
              </div>
            </div>
            
            <div class="probabilities-container" style="margin-bottom:2rem;">
              <div class="prob-labels" style="display:flex; justify-content:space-between; font-size:0.8rem; color:var(--text-secondary); margin-bottom:0.5rem; font-weight:600;">
                <span>${pred.home_team}: ${homeProbPct}%</span>
                <span>Draw: ${drawProbPct}%</span>
                <span>${pred.away_team}: ${awayProbPct}%</span>
              </div>
              <div class="multi-progress" style="height:10px; border-radius:5px; background:rgba(255,255,255,0.05); display:flex; overflow:hidden;">
                <div class="prog-segment home" style="width:${homeProbPct}%; background:linear-gradient(to right, var(--theme-blue, #3a86ff), #00d2ff);"></div>
                <div class="prog-segment draw" style="width:${drawProbPct}%; background:rgba(255,255,255,0.25);"></div>
                <div class="prog-segment away" style="width:${awayProbPct}%; background:linear-gradient(to right, #ff007f, var(--theme-red, #ff4d4d));"></div>
              </div>
            </div>
            
            <div class="advanced-grid" style="display:grid; grid-template-columns:1.2fr 1fr; gap:1.5rem; border-top:1px solid rgba(255,255,255,0.06); padding-top:1.5rem; font-size:0.85rem;">
              <div class="adv-left">
                <div style="margin-bottom:0.75rem;">
                  <span style="color:var(--text-secondary);">Advancing Team:</span>
                  <strong style="color:var(--theme-green); margin-left:4px;">${pred.advancing_team}</strong> 
                  <span style="color:var(--text-muted); font-size:0.8rem;">(${advProbPct}% prob)</span>
                </div>
                <div>
                  <span style="color:var(--text-secondary);">Referee:</span>
                  <span style="color:var(--text-primary); margin-left:4px;">${pred.referee}</span>
                </div>
              </div>
              <div class="adv-right">
                <div style="font-weight:700; color:var(--text-primary); margin-bottom:0.5rem; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px;">Most Likely Scores:</div>
                <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:4px;">
                  ${pred.most_likely_scores.slice(0, 3).map(scoreItem => {
                    const pct = Math.round(scoreItem.prob * 100);
                    return `
                      <li style="display:flex; justify-content:space-between; color:var(--text-secondary);">
                        <code>${scoreItem.score}</code>
                        <span>${pct}%</span>
                      </li>
                    `;
                  }).join('')}
                </ul>
              </div>
            </div>
          `;
          
          predictionsContainer.appendChild(matchCard);
        });
      })
      .catch(err => {
        console.error("Error loading predictions:", err);
        predictionsContainer.innerHTML = `
          <div class="prediction-error" style="grid-column: 1 / -1; text-align: center; padding: 2rem; background: rgba(255, 77, 77, 0.05); border: 1px solid rgba(255, 77, 77, 0.2); border-radius: 12px; color: var(--theme-red);">
            Failed to load model predictions. Please make sure predictions.json exists in assets.
          </div>
        `;
      });
  }

  // Mobile Menu Toggle
  const menuToggle = document.getElementById("menu-toggle");
  const navMenu = document.getElementById("nav-menu");
  
  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      menuToggle.classList.toggle("active");
      navMenu.classList.toggle("active");
    });
    
    // Close menu when clicking a link
    const navLinks = navMenu.querySelectorAll("a");
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        menuToggle.classList.remove("active");
        navMenu.classList.remove("active");
      });
    });
  }
});

// Citation Switcher
window.switchCitation = function(event, format) {
  // Remove active class from all sibling buttons
  const tabs = event.currentTarget.parentElement.querySelectorAll(".tab-btn");
  tabs.forEach(tab => tab.classList.remove("active"));
  
  // Add active class to clicked tab
  event.currentTarget.classList.add("active");
  
  // Hide all citation content divs
  const container = event.currentTarget.parentElement.nextElementSibling;
  const contents = container.querySelectorAll(".citation-content");
  contents.forEach(content => content.style.display = "none");
  
  // Show active content
  const activeContent = container.querySelector("#citation-" + format);
  if (activeContent) {
    activeContent.style.display = "block";
  }
};

// Copy Citation function
window.copyCurrentCitation = function() {
  // Find visible citation text
  const visibleContent = Array.from(document.querySelectorAll(".citation-content"))
    .find(content => window.getComputedStyle(content).display !== "none");
  
  if (visibleContent) {
    navigator.clipboard.writeText(visibleContent.innerText.trim()).then(() => {
      const copyBtn = document.getElementById("copy-citation-btn");
      const originalText = copyBtn.innerHTML;
      copyBtn.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" width="12" height="12" style="margin-right:4px; vertical-align:middle;">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>Copied!
      `;
      setTimeout(() => {
        copyBtn.innerHTML = originalText;
      }, 2000);
    }).catch(err => {
      console.error("Failed to copy citation text:", err);
    });
  }
};
