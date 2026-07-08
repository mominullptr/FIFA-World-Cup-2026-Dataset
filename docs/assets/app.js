document.addEventListener("DOMContentLoaded", () => {
  // Check if DATA_PREVIEWS exists globally
  if (typeof DATA_PREVIEWS === "undefined") {
    console.error("DATA_PREVIEWS data was not loaded.");
    return;
  }

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
});
