document.addEventListener("DOMContentLoaded", function() {
    console.log("Admin Dashboard JS Loaded Successfully!");


    // Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarBackdrop = document.querySelector('.sidebar-backdrop');

    if (sidebarToggle && sidebar) {
        const setSidebarOpen = function(isOpen) {
            const shouldOpen = isOpen && window.innerWidth <= 992;
            sidebar.classList.toggle('active', shouldOpen);
            sidebarToggle.setAttribute('aria-expanded', String(shouldOpen));
            if (sidebarBackdrop) {
                sidebarBackdrop.classList.toggle('is-visible', shouldOpen);
            }
            document.body.classList.toggle('sidebar-open', shouldOpen);
        };

        sidebarToggle.addEventListener('click', function() {
            setSidebarOpen(!sidebar.classList.contains('active'));
        });

        if (sidebarBackdrop) {
            sidebarBackdrop.addEventListener('click', function() {
                setSidebarOpen(false);
            });
        }

        // Close the drawer after navigating, but leave dropdown toggles usable.
        document.querySelectorAll('.sidebar a.nav-link-ajax').forEach(function (link) {
            link.addEventListener('click', function () {
                setSidebarOpen(false);
            });
        });

        window.addEventListener('resize', function() {
            if (window.innerWidth > 992) {
                setSidebarOpen(false);
            }
        });
    }


    // Dark mode toggle logic
    const darkModeIcon = document.querySelector('.fa-moon');
    if (darkModeIcon) {
        darkModeIcon.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            console.log("Theme toggled");
        });
    }

    // --- Properties by Type Donut Chart Dynamic Logic ---
    const propertyDataElement = document.getElementById('property-types-data');
    if (propertyDataElement) {
        try {
            const rawData = propertyDataElement.textContent;
            const propertyTypes = JSON.parse(rawData);

            const propertyLabels = propertyTypes.map(item => item.category__name);
            const propertyCounts = propertyTypes.map(item => item.count);

            console.log("Dynamic Property Labels:", propertyLabels);
            console.log("Dynamic Property Counts:", propertyCounts);

            // Chart.js initialization
            const ctx = document.getElementById('propertyTypeChart');
            if (ctx && propertyLabels.length > 0) {
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: propertyLabels,
                        datasets: [{
                            data: propertyCounts,
                            backgroundColor: [
                                '#3b82f6', 
                                '#10b981', 
                                '#f59e0b', 
                                '#8b5cf6', 
                                '#f97316',
                                '#06b6d4'
                            ],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    boxWidth: 10,
                                    font: { size: 10 }
                                }
                            }
                        },
                        cutout: '75%'
                    }
                });
            }
        } catch (error) {
            console.error("Error parsing property types chart data:", error);
        }
    }
});

// --- Sales Overview Line Chart Logic ---
const salesDataElement = document.getElementById('sales-overview-data');
if (salesDataElement) {
    try {
        const salesCounts = JSON.parse(salesDataElement.textContent);
        console.log("Sales Overview Data:", salesCounts);

        const salesCtx = document.getElementById('salesOverviewChart');
        if (salesCtx) {
            new Chart(salesCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: 'Properties Added',
                        data: salesCounts,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#3b82f6',
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error("Error parsing sales overview data:", error);
    }
}
// 4. Calendar Enquiries Integration Logic
    try {
        const eventsScript = document.getElementById("calendar-events-data");
        if (eventsScript) {
            const enquiriesData = JSON.parse(eventsScript.textContent);
            const calendarDays = document.querySelectorAll(".calendar-grid td, .calendar-day, [data-date]");

            calendarDays.forEach(dayEl => {
                const dateStr = dayEl.getAttribute("data-date");
                if (!dateStr) return;

                const matchingEnquiries = enquiriesData.filter(e => e.date === dateStr);

                if (matchingEnquiries.length > 0) {
                    dayEl.classList.add("has-event");
                    
                    const dot = document.createElement("span");
                    dot.className = "event-dot";
                    dot.style.cssText = "display: block; width: 5px; height: 5px; background: #4f46e5; border-radius: 50%; margin: 2px auto 0;";
                    dayEl.appendChild(dot);

                    dayEl.addEventListener("click", () => {
                        let info = matchingEnquiries.map(e => `${e.title} (${e.status})`).join("\n");
                        alert("Enquiries on " + dateStr + ":\n" + info);
                    });
                }
            });
        }
    } catch (error) {
        console.error("Error in Calendar Integration:", error);
    }


document.addEventListener("DOMContentLoaded", function () {
    const ajaxLinks = document.querySelectorAll('.ajax-link');
    const mainContentArea = document.querySelector('#main-dashboard-content'); // Apne dashboard ke main area ki ID yahan check kar lein

    ajaxLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Page reload hone se rokega

            const url = this.getAttribute('href');

            if (mainContentArea) {
                mainContentArea.innerHTML = "<div class='text-center py-5'><h4>Loading bookings...</h4></div>";
            }

            // AJAX (Fetch) Request
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response error');
                }
                return response.text();
            })
            .then(html => {
                if (mainContentArea) {
                    mainContentArea.innerHTML = html; // Content ko smoothly inject kar dega
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (mainContentArea) {
                    mainContentArea.innerHTML = "<p class='text-danger text-center'>Failed to load content. Please try again.</p>";
                }
            });
        });
    });
});

//  Site Visit Actions
document.addEventListener('click', function(event) {
    var btn = event.target.closest('.action-btn');
    if (!btn) return; // Agar click .action-btn par nahi hai toh kuch mat karo

    event.preventDefault();
    var url = btn.getAttribute('data-url');
    var row = btn.closest('tr');

    console.log("Vanilla JS caught click! URL:", url);

    if (!url) {
        alert("URL is missing on this button!");
        return;
    }

    // Cookie se CSRF token nikalne ka secure tareeka
    let csrftoken = '';
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) csrftoken = parts.pop().split(';').shift();

    // Fetch API ke zariye AJAX request bhejna
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (row) {
                row.style.transition = 'opacity 0.3s ease';
                row.style.opacity = '0';
                setTimeout(() => row.remove(), 300);
            }
        } else {
            alert(data.message || "Action failed.");
        }
    })
    .catch(error => {
        console.error('AJAX Error:', error);
        alert('Something went wrong. Check console.');
    });
});

// --- Isolated Site Visit Image Modal Handlers ---
function openSiteVisitModal(url) {
    const modal = document.getElementById('siteVisitModal');
    const modalImg = document.getElementById('siteVisitModalImg');
    if (modal && modalImg) {
        modalImg.src = url;
        modal.style.display = 'flex';
    }
}

function closeSiteVisitModal() {
    const modal = document.getElementById('siteVisitModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal when clicking on the dark backdrop background
document.addEventListener('click', function(event) {
    const modal = document.getElementById('siteVisitModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

//Site Visit History Modal Handlers
$(document).off('click', '.action-btn').on('click', '.action-btn', function(e) {
    e.preventDefault();
    var url = $(this).attr('data-url');
    
    if (!url) {
        alert("URL is missing!");
        return;
    }

    // Django template ya DOM se CSRF token nikalne ka safe tareeka
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val() || '{{ csrf_token }}';

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            if(response.success) {
                location.reload(); 
            } else {
                alert(response.message || "Action failed.");
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", error);
            alert("Something went wrong. Please try again.");
        }
    });
});

// Admin Commission Form & Status Update AJAX Handler
$(document).on('submit', '#adminCommissionForm, .updateCommissionForm', function(e) {
    e.preventDefault();
    
    var $form = $(this);
    var url = $form.attr('action');
    var formData = new FormData(this);
    var $container = $('#dashboard-dynamic-content');

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'x-requested-with': 'XMLHttpRequest'
        },
        success: function(response) {
            var parser = new DOMParser();
            var doc = parser.parseFromString(response, 'text/html');
            var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content');

            if (extractedDynamicContent) {
                $container.html(extractedDynamicContent.innerHTML);
            } else {
                $container.html(response);
            }
            console.log("Commission operation successful!");
        },
        error: function(xhr) {
            console.error("Error in commission operation:", xhr.responseText);
            alert("Operation failed. Please try again.");
        }
    });
});







