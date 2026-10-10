document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const sidebarBackdrop = document.querySelector(".sidebar-backdrop");

    function closeSidebar() {
        document.body.classList.remove("sidebar-open");
        if (menuToggle) {
            menuToggle.setAttribute("aria-expanded", "false");
        }
    }

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            const isOpen = document.body.classList.toggle("sidebar-open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });
    }

    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener("click", closeSidebar);
    }

    document.querySelectorAll(".sidebar .nav-links a").forEach(function (link) {
        link.addEventListener("click", closeSidebar);
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });

    const enquiryLink = document.getElementById("enquiryMenuLink");

    if (enquiryLink) {
        enquiryLink.addEventListener("click", function (e) {
            e.preventDefault(); // Page reload hone se rokein
            loadMyEnquiries();
        });
    }
});

function loadMyEnquiries() {
    const contentArea = document.getElementById("dashboard-dynamic-content");

    // Loading state (Light theme friendly)
    contentArea.innerHTML = `<p style="color: #475569; text-align: center; padding: 40px; font-weight: 500;">Loading your enquiries...</p>`;

    fetch('/customers/api/my-enquiries/')
        .then(response => response.json())
        .then(data => {
            if (!data.enquiries || data.enquiries.length === 0) {
                contentArea.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h2 style="color: #0f172a; margin: 0; font-size: 22px; font-weight: 600;">My Enquiries</h2>
                        <button onclick="location.reload()" style="background: #ffffff; color: #334155; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                            ← Back to Dashboard
                        </button>
                    </div>
                    <div style="text-align: center; padding: 40px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; color: #1e293b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <h3 style="margin-bottom: 8px; color: #0f172a;">No Enquiries Found</h3>
                        <p style="color: #64748b; margin: 0;">Aapne abhi tak kisi property ke liye inquiry nahi ki hai.</p>
                    </div>`;
                return;
            }

            let html = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h2 style="color: #0f172a; margin: 0; font-size: 22px; font-weight: 600;">My Enquiries</h2>
                    <button onclick="location.reload()" style="background: #ffffff; color: #334155; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                        ← Back to Dashboard
                    </button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 15px;">`;

            data.enquiries.forEach(enq => {
                let statusColor = enq.status === 'Resolved' ? '#16a34a' : '#f59e0b';
                
                html += `
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; color: #1e293b; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div>
                            <span style="background: ${statusColor}; color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase;">${enq.status}</span>
                            <h3 style="margin: 10px 0 5px; font-size: 18px; color: #0f172a;">Property Type: ${enq.property_type || 'General Enquiry'}</h3>
                            <p style="color: #64748b; font-size: 13px; margin: 0 0 8px;">📞 Phone: ${enq.phone}</p>
                            <p style="color: #334155; font-size: 14px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; margin: 0;">💬 "${enq.message || 'No message'}"</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #64748b; font-size: 12px; margin-bottom: 10px;">Date: ${enq.date}</p>
                            <span style="background: #f1f5f9; color: #475569; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 500; display: inline-block;">Submitted</span>
                        </div>
                    </div>`;
            });

            html += `</div>`;
            contentArea.innerHTML = html;
        })
        .catch(err => {
            console.error("Error loading enquiries:", err);
            contentArea.innerHTML = `<p style="color: #ef4444; text-align: center;">Failed to load enquiries.</p>`;
        });
}

// Function to load site visits
document.addEventListener("DOMContentLoaded", function () {
    // Existing Enquiry Link
    const enquiryLink = document.getElementById("enquiryMenuLink");
    if (enquiryLink) {
        enquiryLink.addEventListener("click", function (e) {
            e.preventDefault();
            loadMyEnquiries();
        });
    }

    // New Site Visit Link (Apne HTML sidebar wale site visit link ka id yahan dein, jaise 'siteVisitMenuLink')
    const visitLink = document.getElementById("siteVisitMenuLink");
    if (visitLink) {
        visitLink.addEventListener("click", function (e) {
            e.preventDefault();
            loadMySiteVisits();
        });
    }
});

// function loadMySiteVisits() {
//     const contentArea = document.getElementById("dashboard-dynamic-content");

//     contentArea.innerHTML = `<p style="color: #475569; text-align: center; padding: 40px; font-weight: 500;">Loading your site visits...</p>`;

//     fetch('/customers/api/my-site-visits/')
//         .then(response => response.json())
//         .then(data => {
//             if (!data.visits || data.visits.length === 0) {
//                 contentArea.innerHTML = `
//                     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
//                         <h2 style="color: #0f172a; margin: 0; font-size: 22px; font-weight: 600;">My Site Visits</h2>
//                         <button onclick="location.reload()" style="background: #ffffff; color: #334155; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
//                             ← Back to Dashboard
//                         </button>
//                     </div>
//                     <div style="text-align: center; padding: 40px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; color: #1e293b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
//                         <h3 style="margin-bottom: 8px; color: #0f172a;">No Site Visits Scheduled</h3>
//                         <p style="color: #64748b; margin: 0;">Aapne abhi tak kisi property visit ke liye schedule nahi banaya hai.</p>
//                     </div>`;
//                 return;
//             }

//             let html = `
//                 <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
//                     <h2 style="color: #0f172a; margin: 0; font-size: 22px; font-weight: 600;">My Site Visits</h2>
//                     <button onclick="location.reload()" style="background: #ffffff; color: #334155; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
//                         ← Back to Dashboard
//                     </button>
//                 </div>
//                 <div style="display: flex; flex-direction: column; gap: 15px;">`;

//             data.visits.forEach(visit => {
//                 let statusColor = visit.status === 'Completed' ? '#16a34a' : '#2563eb';
                
//                 html += `
//                     <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; color: #1e293b; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
//                         <div>
//                             <span style="background: ${statusColor}; color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase;">${visit.status}</span>
//                             <h3 style="margin: 10px 0 5px; font-size: 18px; color: #0f172a;">${visit.property_type}</h3>
//                             <p style="color: #64748b; font-size: 13px; margin: 0 0 8px;">📅 Visit Time: <b>${visit.visit_date}</b></p>
//                             <p style="color: #334155; font-size: 14px; background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; margin: 0;">💬 "${visit.message}"</p>
//                         </div>
//                         <div style="text-align: right;">
//                             <span style="background: #f1f5f9; color: #475569; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 500; display: inline-block;">Scheduled Visit</span>
//                         </div>
//                     </div>`;
//             });

//             html += `</div>`;
//             contentArea.innerHTML = html;
//         })
//         .catch(err => {
//             console.error("Error loading site visits:", err);
//             contentArea.innerHTML = `<p style="color: #ef4444; text-align: center;">Failed to load site visits.</p>`;
//         });
// }

/* =========================================================
   CUSTOMER SITE VISITS
   ========================================================= */

let customerSiteVisitsData = [];


/* =========================================================
   LOAD SITE VISITS PAGE
   ========================================================= */

function loadMySiteVisits() {

    const container = document.getElementById(
        "dashboard-dynamic-content"
    );

    if (!container) {
        return;
    }


    /*
     * site_visits.html ko dynamically load karega.
     *
     * Is URL ke liye next step mein Django view + URL
     * add karenge agar abhi route nahi bana hai.
     */

    fetch("/customers/site-visits-page/", {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })

    .then(response => {

        if (!response.ok) {
            throw new Error(
                "Site Visits page could not be loaded."
            );
        }

        return response.text();

    })

    .then(html => {

        container.innerHTML = html;

        /*
         * HTML load hone ke baad API call.
         */
        loadCustomerSiteVisitData();

    })

    .catch(error => {

        console.error(
            "Site Visits Page Error:",
            error
        );

        container.innerHTML = `
            <div style="
                background:#ffffff;
                padding:50px 20px;
                text-align:center;
                color:#64748b;
            ">
                <div style="
                    width:55px;
                    height:55px;
                    margin:0 auto 15px;
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#fef2f2;
                    color:#dc2626;
                    font-size:22px;
                ">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                </div>

                <h3 style="
                    margin:0 0 6px;
                    color:#334155;
                    font-size:16px;
                ">
                    Unable to Load Site Visits
                </h3>

                <p style="
                    margin:0;
                    font-size:12px;
                ">
                    Please try again.
                </p>
            </div>
        `;

    });

}


/* =========================================================
   LOAD SITE VISIT API DATA
   ========================================================= */

function loadCustomerSiteVisitData() {

    fetch("/customers/api/my-site-visits/", {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })

    .then(response => {

        if (!response.ok) {
            throw new Error(
                "Unable to load site visit data."
            );
        }

        return response.json();

    })

    .then(data => {

        customerSiteVisitsData = Array.isArray(data.visits)
            ? data.visits
            : [];

        renderCustomerSiteVisits(
            customerSiteVisitsData
        );

        setupSiteVisitModal();

    })

    .catch(error => {

        console.error(
            "Site Visit API Error:",
            error
        );

        customerSiteVisitsData = [];

        renderCustomerSiteVisits([]);

    });

}


/* =========================================================
   RENDER SITE VISITS TABLE
   ========================================================= */

function renderCustomerSiteVisits(visits) {

    const tableBody = document.getElementById(
        "siteVisitsTableBody"
    );

    const emptyState = document.getElementById(
        "siteVisitsEmpty"
    );

    const totalElement = document.getElementById(
        "siteVisitTotal"
    );


    if (!tableBody) {
        return;
    }


    /*
     * Total visits
     */
    if (totalElement) {

        totalElement.textContent = visits.length;

    }


    /*
     * Clear old rows.
     *
     * IMPORTANT:
     * Same API record = same table row.
     *
     * Status change ke liye new row create nahi hoti.
     */

    tableBody.innerHTML = "";


    /*
     * No visits
     */

    if (!visits.length) {

        if (emptyState) {
            emptyState.style.display = "block";
        }

        return;

    }


    /*
     * Visits available
     */

    if (emptyState) {
        emptyState.style.display = "none";
    }


    visits.forEach(visit => {

        const row = document.createElement("tr");

        row.innerHTML = `

            <!-- PROPERTY -->
            <td>

                <div class="site-property-info">

                    <strong
                        title="${escapeHtml(
                            visit.property_name || "Property Visit"
                        )}"
                    >
                        ${escapeHtml(
                            visit.property_name || "Property Visit"
                        )}
                    </strong>

                    <span>
                        ${escapeHtml(
                            visit.property_type || "Property"
                        )}
                    </span>

                </div>

            </td>


            <!-- VISIT DATE -->
            <td>

                <div class="site-date-cell">

                    <strong>
                        ${escapeHtml(
                            visit.visit_date || "Not Scheduled"
                        )}
                    </strong>

                    <small>
                        Scheduled Visit
                    </small>

                </div>

            </td>


            <!-- AGENT -->
            <td>

                <div class="site-agent-cell">

                    ${
                        visit.agent_name
                        ? `
                            <div class="site-agent-name">

                                <i class="fa-solid fa-user-tie"></i>

                                ${escapeHtml(
                                    visit.agent_name
                                )}

                            </div>
                        `
                        : `
                            <div class="site-agent-name"
                                style="color:#94a3b8;"
                            >

                                <i class="fa-regular fa-user"></i>

                                Not Assigned

                            </div>
                        `
                    }


                    ${
                        visit.agent_phone
                        ? `
                            <a
                                class="site-agent-phone"
                                href="tel:${escapeHtml(
                                    visit.agent_phone
                                )}"
                            >

                                <i class="fa-solid fa-phone"></i>

                                ${escapeHtml(
                                    visit.agent_phone
                                )}

                            </a>
                        `
                        : ""
                    }

                </div>

            </td>


            <!-- STATUS -->
            <td>

                ${createSiteVisitStatus(
                    visit.status
                )}

            </td>


            <!-- LOCATION -->
            <td>

                <div class="site-location-cell">

                    <span>

                        <i class="fa-solid fa-location-dot"></i>

                        ${escapeHtml(
                            visit.location || "Not Available"
                        )}

                    </span>

                </div>

            </td>


            <!-- ACTION -->
            <td>

                <button
                    type="button"
                    class="site-view-btn"
                    data-visit-id="${escapeHtml(
                        visit.id
                    )}"
                >

                    <i class="fa-regular fa-eye"></i>

                    View

                </button>

            </td>

        `;


        tableBody.appendChild(row);

    });


    /*
     * View buttons
     */

    tableBody
        .querySelectorAll(".site-view-btn")
        .forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    const visitId = this.dataset.visitId;

                    openCustomerSiteVisitModal(
                        visitId
                    );

                }
            );

        });

}


/* =========================================================
   STATUS BADGE
   ========================================================= */

function createSiteVisitStatus(status) {

    const normalizedStatus = (
        status || "Pending"
    ).trim().toLowerCase();


    let className = "status-pending";

    let displayText = "Pending";


    if (normalizedStatus === "assigned") {

        className = "status-assigned";

        displayText = "Assigned";

    }

    else if (
        normalizedStatus === "under review" ||
        normalizedStatus === "under_review" ||
        normalizedStatus === "review"
    ) {

        className = "status-review";

        displayText = "Under Review";

    }

    else if (normalizedStatus === "approved") {

        className = "status-approved";

        displayText = "Approved";

    }

    else if (normalizedStatus === "rejected") {

        className = "status-rejected";

        displayText = "Rejected";

    }

    else if (normalizedStatus === "completed") {

        className = "status-completed";

        displayText = "Completed";

    }

    else if (normalizedStatus === "cancelled") {

        className = "status-cancelled";

        displayText = "Cancelled";

    }


    return `

        <span class="site-status ${className}">

            <span class="status-dot"></span>

            ${displayText}

        </span>

    `;

}


/* =========================================================
   OPEN SITE VISIT MODAL
   ========================================================= */

function openCustomerSiteVisitModal(visitId) {

    const visit = customerSiteVisitsData.find(
        item => String(item.id) === String(visitId)
    );


    if (!visit) {

        console.error(
            "Site visit not found:",
            visitId
        );

        return;

    }


    const modal = document.getElementById(
        "siteVisitModal"
    );


    if (!modal) {
        return;
    }


    /* =====================================================
       PROPERTY IMAGE
       ONLY HERE
       ===================================================== */

    const propertyImage = document.getElementById(
        "modalPropertyImage"
    );


    if (propertyImage) {

        if (visit.property_image) {

            propertyImage.src =
                visit.property_image;

            propertyImage.style.display =
                "block";

        }

        else {

            propertyImage.removeAttribute("src");

            propertyImage.style.display =
                "none";

        }

    }


    /* =====================================================
       PROPERTY NAME
       ===================================================== */

    const propertyName = document.getElementById(
        "modalPropertyName"
    );


    if (propertyName) {

        propertyName.textContent =
            visit.property_name ||
            "Property Visit";

    }


    /* =====================================================
       PROPERTY TYPE
       ===================================================== */

    const propertyType = document.getElementById(
        "modalPropertyType"
    );


    if (propertyType) {

        propertyType.textContent =
            visit.property_type ||
            "Property";

    }


    /* =====================================================
       STATUS
       ===================================================== */

    const statusElement = document.getElementById(
        "modalVisitStatus"
    );


    if (statusElement) {

        const statusClass = getSiteVisitStatusClass(
            visit.status
        );


        const statusText = getSiteVisitStatusText(
            visit.status
        );


        statusElement.className =
            `site-status ${statusClass}`;


        statusElement.innerHTML = `

            <span class="status-dot"></span>

            ${statusText}

        `;

    }


    /* =====================================================
       DATE
       ===================================================== */

    const dateElement = document.getElementById(
        "modalVisitDate"
    );


    if (dateElement) {

        dateElement.textContent =
            visit.visit_date ||
            "Not Scheduled";

    }


    /* =====================================================
       LOCATION
       ===================================================== */

    const locationElement = document.getElementById(
        "modalVisitLocation"
    );


    if (locationElement) {

        locationElement.textContent =
            visit.location ||
            "Not Available";

    }


    /* =====================================================
       CUSTOMER CONTACT
       ===================================================== */

    const phoneElement = document.getElementById(
        "modalVisitPhone"
    );


    if (phoneElement) {

        phoneElement.textContent =
            visit.phone ||
            "Not Available";

    }


    /* =====================================================
       AGENT NAME
       ===================================================== */

    const agentNameElement = document.getElementById(
        "modalAgentName"
    );


    if (agentNameElement) {

        agentNameElement.textContent =
            visit.agent_name ||
            "Not Assigned";

    }


    /* =====================================================
       AGENT PHONE
       ===================================================== */

    const agentPhoneElement = document.getElementById(
        "modalAgentPhone"
    );


    if (agentPhoneElement) {

        const phoneText =
            agentPhoneElement.querySelector("span");


        if (visit.agent_phone) {

            agentPhoneElement.href =
                `tel:${visit.agent_phone}`;

            agentPhoneElement.style.display =
                "inline-flex";


            if (phoneText) {

                phoneText.textContent =
                    visit.agent_phone;

            }

        }

        else {

            agentPhoneElement.removeAttribute(
                "href"
            );

            agentPhoneElement.style.display =
                "none";


            if (phoneText) {

                phoneText.textContent = "";

            }

        }

    }


    /* =====================================================
       VISIT TYPE
       ===================================================== */

    const visitTypeSection = document.getElementById(
        "modalVisitTypeSection"
    );

    const visitTypeElement = document.getElementById(
        "modalVisitType"
    );


    if (
        visit.visit_type &&
        visit.visit_type.trim()
    ) {

        if (visitTypeSection) {
            visitTypeSection.style.display =
                "block";
        }

        if (visitTypeElement) {
            visitTypeElement.textContent =
                visit.visit_type;
        }

    }

    else {

        if (visitTypeSection) {
            visitTypeSection.style.display =
                "none";
        }

        if (visitTypeElement) {
            visitTypeElement.textContent = "";
        }

    }


    /* =====================================================
       VISIT PURPOSE
       ===================================================== */

    const purposeSection = document.getElementById(
        "modalVisitPurposeSection"
    );

    const purposeElement = document.getElementById(
        "modalVisitPurpose"
    );


    if (
        visit.visit_purpose &&
        visit.visit_purpose.trim()
    ) {

        if (purposeSection) {
            purposeSection.style.display =
                "block";
        }

        if (purposeElement) {
            purposeElement.textContent =
                visit.visit_purpose;
        }

    }

    else {

        if (purposeSection) {
            purposeSection.style.display =
                "none";
        }

        if (purposeElement) {
            purposeElement.textContent = "";
        }

    }


    /* =====================================================
       NOTES
       ===================================================== */

    const notesElement = document.getElementById(
        "modalVisitNotes"
    );


    if (notesElement) {

        notesElement.textContent =
            visit.notes ||
            "No notes available.";

    }


    /* =====================================================
       AGENT VISIT IMAGE
       ===================================================== */

    const visitImageSection =
        document.getElementById(
            "modalVisitImageSection"
        );

    const visitImage =
        document.getElementById(
            "modalVisitImage"
        );


    if (
        visit.visit_image &&
        visitImage &&
        visitImageSection
    ) {

        visitImage.src =
            visit.visit_image;

        visitImageSection.style.display =
            "block";

    }

    else {

        if (visitImage) {

            visitImage.removeAttribute(
                "src"
            );

        }

        if (visitImageSection) {

            visitImageSection.style.display =
                "none";

        }

    }


    /* =====================================================
       OPEN MODAL
       ===================================================== */

    modal.style.display =
        "flex";


    document.body.style.overflow =
        "hidden";

}


/* =========================================================
   MODAL SETUP
   ========================================================= */

function setupSiteVisitModal() {

    const modal = document.getElementById(
        "siteVisitModal"
    );

    const closeButton = document.getElementById(
        "closeSiteVisitModal"
    );


    if (!modal) {
        return;
    }


    /*
     * Close button
     */

    if (closeButton) {

        closeButton.onclick =
            closeCustomerSiteVisitModal;

    }


    /*
     * Click outside modal
     */

    modal.onclick = function (event) {

        if (
            event.target === modal
        ) {

            closeCustomerSiteVisitModal();

        }

    };


    /*
     * Escape key
     */

    document.addEventListener(
        "keydown",
        customerSiteVisitEscapeHandler
    );

}


/* =========================================================
   ESCAPE KEY
   ========================================================= */

function customerSiteVisitEscapeHandler(event) {

    if (
        event.key === "Escape"
    ) {

        const modal =
            document.getElementById(
                "siteVisitModal"
            );


        if (
            modal &&
            modal.style.display !== "none"
        ) {

            closeCustomerSiteVisitModal();

        }

    }

}


/* =========================================================
   CLOSE MODAL
   ========================================================= */

function closeCustomerSiteVisitModal() {

    const modal =
        document.getElementById(
            "siteVisitModal"
        );


    if (!modal) {
        return;
    }


    modal.style.display =
        "none";


    document.body.style.overflow =
        "";

}


/* =========================================================
   STATUS CLASS
   ========================================================= */

function getSiteVisitStatusClass(status) {

    const normalizedStatus = (
        status || "Pending"
    ).trim().toLowerCase();


    if (normalizedStatus === "assigned") {

        return "status-assigned";

    }


    if (
        normalizedStatus === "under review" ||
        normalizedStatus === "under_review" ||
        normalizedStatus === "review"
    ) {

        return "status-review";

    }


    if (normalizedStatus === "approved") {

        return "status-approved";

    }


    if (normalizedStatus === "rejected") {

        return "status-rejected";

    }


    if (normalizedStatus === "completed") {

        return "status-completed";

    }


    if (normalizedStatus === "cancelled") {

        return "status-cancelled";

    }


    return "status-pending";

}


/* =========================================================
   STATUS TEXT
   ========================================================= */

function getSiteVisitStatusText(status) {

    const normalizedStatus = (
        status || "Pending"
    ).trim().toLowerCase();


    if (normalizedStatus === "assigned") {

        return "Assigned";

    }


    if (
        normalizedStatus === "under review" ||
        normalizedStatus === "under_review" ||
        normalizedStatus === "review"
    ) {

        return "Under Review";

    }


    if (normalizedStatus === "approved") {

        return "Approved";

    }


    if (normalizedStatus === "rejected") {

        return "Rejected";

    }


    if (normalizedStatus === "completed") {

        return "Completed";

    }


    if (normalizedStatus === "cancelled") {

        return "Cancelled";

    }


    return "Pending";

}


/* =========================================================
   HTML ESCAPE
   ========================================================= */

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


/* =========================================================
   SIDEBAR SITE VISITS
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const visitLink =
            document.getElementById(
                "siteVisitMenuLink"
            );


        if (visitLink) {

            visitLink.addEventListener(
                "click",
                function (event) {

                    event.preventDefault();

                    loadMySiteVisits();

                }
            );

        }

    }
);


// Function to load bookings
document.addEventListener("DOMContentLoaded", function () {
    const bookingLink = document.getElementById("bookingMenuLink");
    if (bookingLink) {
        bookingLink.addEventListener("click", function (e) {
            e.preventDefault();
            loadMyBookings();
        });
    }
});

function loadMyBookings() {
    const contentArea = document.getElementById("dashboard-dynamic-content");
    contentArea.innerHTML = `<p style="color: #475569; text-align: center; padding: 40px; font-weight: 500;">Loading your bookings...</p>`;

    fetch('/customers/api/my-bookings/')
        .then(response => response.json())
        .then(data => {
            contentArea.innerHTML = data.html;
        })
        .catch(err => {
            console.error("Error loading bookings:", err);
            contentArea.innerHTML = `<p style="color: #ef4444; text-align: center;">Failed to load bookings.</p>`;
        });
}


// 3. Load Support Tickets via AJAX
function loadSupportAjax() {
    fetch(SUPPORT_URL, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("dashboard-dynamic-content").innerHTML = data.html;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('submit', function(e) {
    if (e.target && e.target.id === 'supportForm') {
        e.preventDefault();
        let formData = new FormData(e.target);

        fetch(SUPPORT_URL, {
            method: 'POST',
            body: formData,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadSupportAjax();
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

//Customer Profile
document.addEventListener("DOMContentLoaded", function() {
    
    // Profile menu link click handler
    document.addEventListener('click', function(e) {
        let profileLink = e.target.closest('#profileMenuLink');
        
        if (profileLink) {
            e.preventDefault();
            
            let profileUrl = profileLink.getAttribute('data-url');
            if (!profileUrl) return;
            
            fetch(profileUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                let contentArea = document.getElementById('dashboard-content-area');
                if (contentArea) {
                    contentArea.innerHTML = html;
                }
            })
            .catch(error => {
                console.error('Error loading profile:', error);
            });
        }
    });

});



let savedPropertyModalPreviousOverflow = "";
let savedPropertyModalTrigger = null;

function closeSavedPropertyDetailsModal() {
    const modal = document.getElementById("savedPropertyDetailsModal");
    if (!modal || !modal.classList.contains("is-open")) return;

    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = savedPropertyModalPreviousOverflow;

    if (savedPropertyModalTrigger && savedPropertyModalTrigger.isConnected) {
        savedPropertyModalTrigger.focus();
    }
}

document.addEventListener("click", function (e) {
    const modal = document.getElementById("savedPropertyDetailsModal");
    if (!modal) return;

    if (e.target.closest(".customer-property-modal-close") || e.target === modal) {
        closeSavedPropertyDetailsModal();
        return;
    }

    const thumbnail = e.target.closest(".customer-property-thumbnail");
    if (thumbnail) {
        const image = document.getElementById("savedPropertyModalImage");
        if (image) {
            image.src = thumbnail.dataset.imageSrc;
            image.alt = thumbnail.dataset.imageAlt;
            modal.querySelectorAll(".customer-property-thumbnail").forEach(function (item) {
                item.classList.toggle("is-active", item === thumbnail);
            });
        }
        return;
    }

    const button = e.target.closest(".customer-property-view-btn");
    if (!button) return;

    const property = button.dataset;
    const card = button.closest(".customer-saved-property-card");
    const modalImage = document.getElementById("savedPropertyModalImage");
    const gallery = document.getElementById("savedPropertyModalGallery");
    const setText = function (id, value) {
        const element = document.getElementById(id);
        if (element) element.textContent = value || "-";
    };

    setText("savedPropertyModalName", property.propertyName);
    setText(
        "savedPropertyModalLocation",
        [property.propertyLocation, property.propertyCity].filter(Boolean).join(", ")
    );
    setText("savedPropertyModalStatus", property.propertyStatus);
    setText("savedPropertyModalPrice", "₹ " + (property.propertyPrice || ""));
    setText("savedPropertyModalType", property.propertyCategory);
    setText("savedPropertyModalArea", property.propertyArea);
    setText("savedPropertyModalBedrooms", property.propertyBedrooms);
    setText("savedPropertyModalBathrooms", property.propertyBathrooms);
    setText("savedPropertyModalDescription", property.propertyDescription);
    document.getElementById("savedPropertyModalFeatured").textContent = property.propertyFeatured || "";
    document.getElementById("savedPropertyModalCreated").textContent =
        property.propertyCreated ? "Listed on " + property.propertyCreated : "";

    if (gallery) {
        gallery.replaceChildren();
        const seenImages = new Set();
        const images = card ? card.querySelectorAll(".customer-property-gallery-data [data-image-src]") : [];

        images.forEach(function (sourceImage) {
            const imageSrc = sourceImage.dataset.imageSrc;
            if (!imageSrc || seenImages.has(imageSrc)) return;
            seenImages.add(imageSrc);

            const thumbnail = document.createElement("button");
            thumbnail.type = "button";
            thumbnail.className = "customer-property-thumbnail";
            thumbnail.setAttribute("aria-label", "Show property image");
            thumbnail.dataset.imageSrc = imageSrc;
            thumbnail.dataset.imageAlt = sourceImage.dataset.imageAlt || property.propertyName;

            const thumbnailImage = document.createElement("img");
            thumbnailImage.src = imageSrc;
            thumbnailImage.alt = sourceImage.dataset.imageAlt || property.propertyName;
            thumbnail.appendChild(thumbnailImage);
            gallery.appendChild(thumbnail);
        });

        const firstThumbnail = gallery.querySelector(".customer-property-thumbnail");
        if (firstThumbnail && modalImage) {
            modalImage.src = firstThumbnail.dataset.imageSrc;
            modalImage.alt = firstThumbnail.dataset.imageAlt;
            firstThumbnail.classList.add("is-active");
            gallery.hidden = gallery.children.length < 2;
        } else if (modalImage) {
            modalImage.removeAttribute("src");
            gallery.hidden = true;
        }
    }

    savedPropertyModalTrigger = button;
    savedPropertyModalPreviousOverflow = document.body.style.overflow;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    modal.querySelector(".customer-property-modal-close").focus();
});

document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        closeSavedPropertyDetailsModal();
    }
});


document.addEventListener("click", function (e) {

    const btn = e.target.closest(".customer-booking-view-btn");
    if (!btn) return;

    const d = btn.dataset;

    document.getElementById("bookingModalName").textContent = d.propertyName;
    document.getElementById("bookingModalLocation").innerHTML =
        `<i class="fa-solid fa-location-dot"></i> ${d.propertyLocation}, ${d.propertyCity}`;

    document.getElementById("bookingModalPrice").textContent = "₹ " + d.propertyPrice;

    document.getElementById("bookingModalType").textContent = d.propertyType;
    document.getElementById("bookingModalArea").textContent = d.propertyArea || "-";
    document.getElementById("bookingModalBedrooms").textContent = d.propertyBedrooms || "-";
    document.getElementById("bookingModalBathrooms").textContent = d.propertyBathrooms || "-";

    document.getElementById("bookingModalDate").textContent = d.date;
    document.getElementById("bookingModalId").textContent = d.id;
    document.getElementById("bookingModalStatus").textContent = d.status;

    const img = document.getElementById("bookingModalImage");

    if (d.propertyImage) {
        img.src = d.propertyImage;
        img.style.display = "block";
    } else {
        img.style.display = "none";
    }

    document.getElementById("bookingDetailsModal").style.display = "flex";
});


function closeBookingModal() {
    document.getElementById("bookingDetailsModal").style.display = "none";
}



/* =========================================================
   TOP PROFILE DROPDOWN
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const profile = document.getElementById("userProfileDropdown");
    const dropdown = document.getElementById("profileDropdownMenu");

    if (!profile || !dropdown) {
        console.warn("Profile dropdown elements not found.");
        return;
    }


    /* =====================================================
       OPEN / CLOSE PROFILE DROPDOWN
       ===================================================== */

    profile.addEventListener("click", function (e) {

        /*
         * Dropdown ke andar click ko ignore karein
         */
        if (e.target.closest(".profile-dropdown-menu")) {
            return;
        }

        e.stopPropagation();

        profile.classList.toggle("profile-dropdown-open");

    });


    /* =====================================================
       DROPDOWN KE ANDAR CLICK
       ===================================================== */

    dropdown.addEventListener("click", function (e) {

        e.stopPropagation();

    });


    /* =====================================================
       OUTSIDE CLICK
       ===================================================== */

    document.addEventListener("click", function (e) {

        if (!profile.contains(e.target)) {

            profile.classList.remove(
                "profile-dropdown-open"
            );

        }

    });

});
