// document.addEventListener("DOMContentLoaded", function() {
//     // 1. Mobile Sidebar Toggle
//     const menuBtn = document.getElementById("menu-btn");
//     const sidebar = document.getElementById("sidebar");

//     if (menuBtn && sidebar) {
//         menuBtn.addEventListener("click", () => {
//             sidebar.classList.toggle("hidden");
//             sidebar.classList.toggle("absolute");
//             sidebar.classList.toggle("z-50");
//             sidebar.classList.toggle("h-full");
//         });
//     }
    
//     console.log("Agent Dashboard Script Initialized Successfully!");
// });

// //My Properties Page

// document.addEventListener("click", function(e) {
//     const link = e.target.closest('#agentPropertiesLink, .ajax-sidebar-link');
    
//     if (link) {
//         e.preventDefault();
        
//         // URL chahe data-url me ho ya href me, dono handle ho jayenge
//         const url = link.getAttribute('data-url') || link.getAttribute('href');
//         if (!url || url === '#') return;

//         const container = document.getElementById('dashboard-dynamic-content');
//         if (!container) {
//             console.error("Error: 'dashboard-dynamic-content' container nahi mila!");
//             return;
//         }

//         // Loading spinner dikhayein
//         container.innerHTML = `
//             <div class="flex items-center justify-center h-64">
//                 <div class="text-center">
//                     <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
//                     <p class="text-xs text-slate-500">Loading content...</p>
//                 </div>
//             </div>
//         `;
        
//         fetch(url, {
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => response.text())
//         .then(html => {
//             // Agar galti se view poora layout bhej de, toh sirf dynamic content extract kar lo
//             const parser = new DOMParser();
//             const doc = parser.parseFromString(html, 'text/html');
//             const extractedDynamicContent = doc.getElementById('dashboard-dynamic-content');
            
//             if (extractedDynamicContent) {
//                 container.innerHTML = extractedDynamicContent.innerHTML;
//             } else {
//                 container.innerHTML = html;
//             }
//         })
//         .catch(error => {
//             console.error('AJAX Error:', error);
//             container.innerHTML = `
//                 <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
//                     <p class="font-bold">Failed to load page.</p>
//                     <p>Please try again or check your connection.</p>
//                 </div>
//             `;
//         });
//     }
// });

// //Agent Dashboard Add Property Page
// $(document).ready(function() {
//     $(document).on('click', '.nav-link-ajax, #agentPropertiesLink, .ajax-sidebar-link', function(e) {
//         e.preventDefault();

//         var url = $(this).attr('href') || $(this).data('url');
//         if (!url || url === '#') return;

//         $('#dashboard-dynamic-content').html(`
//             <div class="flex items-center justify-center h-64">
//                 <div class="text-center">
//                     <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
//                     <p class="text-xs text-slate-500">Loading content...</p>
//                 </div>
//             </div>
//         `);

//         $.ajax({
//             url: url,
//             type: "GET",
//             headers: {'x-requested-with': 'XMLHttpRequest'},
//             success: function(response) {
//                 // Agar server ne poora layout bhej diya hai, toh sirf dynamic content nikal lo
//                 var parser = new DOMParser();
//                 var doc = parser.parseFromString(response, 'text/html');
//                 var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content');

//                 if (extractedDynamicContent) {
//                     $('#dashboard-dynamic-content').html(extractedDynamicContent.innerHTML);
//                 } else {
//                     $('#dashboard-dynamic-content').html(response);
//                 }
//             },
//             error: function(xhr, status, error) {
//                 $('#dashboard-dynamic-content').html(`
//                     <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
//                         <p class="font-bold">Failed to load page.</p>
//                         <p>Please try again or check your connection.</p>
//                     </div>
//                 `);
//             }
//         });
//     });
// });

// // Agent Dashboard Site Visits Page

// $(document).ready(function() {
//     // 1. Sidebar & Navigation AJAX Handler
//     $(document).on('click', '.nav-link-ajax, #agentPropertiesLink, .ajax-sidebar-link, #nav-site-visits', function(e) {
//         e.preventDefault();

//         var url = $(this).attr('href') || $(this).data('url') || (typeof siteVisitsUrl !== 'undefined' ? siteVisitsUrl : '');
//         if (!url || url === '#') return;

//         var $container = $('#dashboard-dynamic-content');
//         if ($container.length === 0) {
//             console.error("Error: 'dashboard-dynamic-content' container nahi mila!");
//             return;
//         }

//         $container.html(`
//             <div class="flex items-center justify-center h-64">
//                 <div class="text-center">
//                     <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
//                     <p class="text-xs text-slate-500">Loading...</p>
//                 </div>
//             </div>
//         `);

//         $.ajax({
//             url: url,
//             type: "GET",
//             headers: {'x-requested-with': 'XMLHttpRequest'},
//             success: function(response) {
//                 var parser = new DOMParser();
//                 var doc = parser.parseFromString(response, 'text/html');
//                 var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content') || doc.getElementById('dashboard-main-content');

//                 if (extractedDynamicContent) {
//                     $container.html(extractedDynamicContent.innerHTML);
//                 } else {
//                     $container.html(response);
//                 }
//             },
//             error: function(xhr, status, error) {
//                 console.error('AJAX Error:', error);
//                 $container.html(`
//                     <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
//                         <p class="font-bold">Failed to load content.</p>
//                         <p>Please try again or check your connection.</p>
//                     </div>
//                 `);
//             }
//         });
//     });

//     // 2. Site Visit Form AJAX Submission Handler
//     $(document).on('submit', '#siteVisitForm', function(e) {
//         e.preventDefault();
        
//         var formData = new FormData(this);
//         var $container = $('#dashboard-dynamic-content'); // Sahi container ID
//         var formActionUrl = $(this).attr('action') || window.location.href;
        
//         $.ajax({
//             url: formActionUrl,
//             type: 'POST',
//             data: formData,
//             processData: false,
//             contentType: false,
//             headers: {
//                 'x-requested-with': 'XMLHttpRequest'
//             },
//             success: function(response) {
//                 var parser = new DOMParser();
//                 var doc = parser.parseFromString(response, 'text/html');
//                 var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content') || doc.getElementById('dashboard-main-content');

//                 if (extractedDynamicContent) {
//                     $container.html(extractedDynamicContent.innerHTML);
//                 } else {
//                     $container.html(response);
//                 }
//                 console.log("Site visit submitted and history updated successfully!");
//             },
//             error: function(xhr) {
//                 console.log("Error in site visit submission:", xhr.responseText);
//             }
//         });
//     });
// });

// // 3. Edit Visit Button Click Handler (AJAX GET)
// $(document).on('click', '.edit-visit-btn', function(e) {
//     e.preventDefault();
//     e.stopImmediatePropagation();
    
//     var rawUrl = $(this).attr('href');
//     if (!rawUrl || rawUrl === '#') return false;

//     // URL me forcefully ajax=true jod rahe hain taaki view kabhi confuse na ho
//     var url = rawUrl.includes('?') ? rawUrl + '&ajax=true' : rawUrl + '?ajax=true';

//     var $container = $('#dashboard-dynamic-content');
//     if ($container.length === 0) return false;

//     $container.html(`
//         <div class="flex items-center justify-center h-64">
//             <div class="text-center">
//                 <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
//                 <p class="text-xs text-slate-500">Loading edit form...</p>
//             </div>
//         </div>
//     `);

//     $.ajax({
//         url: url,
//         type: "GET",
//         success: function(response) {
//             // Ab server sirf edit_site_visit.html bhejega, isliye seedha inject kar dein
//             $container.html(response);
//         },
//         error: function(xhr) {
//             console.error('Error loading edit form:', xhr.responseText);
//             $container.html(`
//                 <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">
//                     <p class="font-bold">Failed to load edit form.</p>
//                 </div>
//             `);
//         }
//     });
    
//     return false;
// });

// // 4. Edit Site Visit Form Submission Handler (AJAX POST) - Delegated for Dynamic Forms
// $(document).on('submit', '#editSiteVisitForm', function(e) {
//     e.preventDefault();
//     e.stopImmediatePropagation();
    
//     var formData = new FormData(this);
//     var $container = $('#dashboard-dynamic-content');
//     var formActionUrl = $(this).attr('action') || window.location.href;
    
//     $.ajax({
//         url: formActionUrl,
//         type: 'POST',
//         data: formData,
//         processData: false,
//         contentType: false,
//         headers: {
//             'x-requested-with': 'XMLHttpRequest'
//         },
//         success: function(response) {
//             var parser = new DOMParser();
//             var doc = parser.parseFromString(response, 'text/html');
//             var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content') || doc.getElementById('dashboard-main-content');

//             if (extractedDynamicContent) {
//                 $container.html(extractedDynamicContent.innerHTML);
//             } else {
//                 $container.html(response);
//             }
//             console.log("Site visit updated successfully!");
//         },
//         error: function(xhr) {
//             console.error("Error updating site visit:", xhr.responseText);
//             alert("Failed to update site visit. Please check the form data.");
//         }
//     });
    
//     return false;
// });

// // 5. Cancel Edit Button Handler
// $(document).on('click', '#cancelEditBtn', function(e) {
//     e.preventDefault();
//     // Wapas site visits list par redirect/load kar dega
//     if (typeof siteVisitsUrl !== 'undefined') {
//         $('#nav-site-visits').trigger('click');
//     } else {
//         location.reload();
//     }
// });

// // Delete Site Visit Handler (AJAX POST)
// $(document).on('click', '.delete-visit-btn', function(e) {
//     e.preventDefault();
//     e.stopImmediatePropagation();
    
//     if (!confirm("Are you sure you want to delete this site visit?")) {
//         return false;
//     }
    
//     // Yahan change kiya hai: data-url ki jagah href use kar rahe hain taaki template se match kare
//     var rawUrl = $(this).attr('href');
//     if (!rawUrl || rawUrl === '#') return false;

//     // View me is_ajax / query parameter detection ke liye ?ajax=true jod rahe hain
//     var url = rawUrl.includes('?') ? rawUrl + '&ajax=true' : rawUrl + '?ajax=true';

//     var $container = $('#dashboard-dynamic-content');
//     if ($container.length === 0) return false;
    
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: {
//             'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
//         },
//         headers: {
//             'x-requested-with': 'XMLHttpRequest'
//         },
//         success: function(response) {
//             var parser = new DOMParser();
//             var doc = parser.parseFromString(response, 'text/html');
//             var extractedDynamicContent = doc.getElementById('dashboard-dynamic-content') || doc.getElementById('dashboard-main-content');

//             if (extractedDynamicContent) {
//                 $container.html(extractedDynamicContent.innerHTML);
//             } else {
//                 $container.html(response);
//             }
//             console.log("Site visit deleted successfully!");
//         },
//         error: function(xhr) {
//             console.error("Error deleting site visit:", xhr.responseText);
//             alert("Failed to delete site visit.");
//         }
//     });
    
//     return false;
// });

// //Profile Page (AJAX Link Handler)
// document.addEventListener('click', function(e) {
//     const link = e.target.closest('.ajax-link');
//     if (link) {
//         e.preventDefault();
//         let href = link.getAttribute('href');
//         if (!href || href === '#') return;
        
//         let absoluteUrl = href.startsWith('http') ? href : window.location.origin + (href.startsWith('/') ? href : '/' + href);
        
//         const container = document.getElementById('dashboard-dynamic-content');
//         if (!container) return;

//         container.innerHTML = `
//             <div class="flex items-center justify-center h-64">
//                 <div class="text-center">
//                     <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
//                     <p class="text-xs text-slate-500">Loading...</p>
//                 </div>
//             </div>
//         `;
        
//         fetch(absoluteUrl, {
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => response.text())
//         .then(html => {
//             const parser = new DOMParser();
//             const doc = parser.parseFromString(html, 'text/html');
//             const extractedDynamicContent = doc.getElementById('dashboard-dynamic-content');
            
//             if (extractedDynamicContent) {
//                 container.innerHTML = extractedDynamicContent.innerHTML;
//             } else {
//                 container.innerHTML = html;
//             }
//         })
//         .catch(error => console.error('Error loading page:', error));
//     }
// });

// // Edit Profile Form AJAX Submission (With Auto-Reload for Top Header Sync)
// document.addEventListener('submit', function(e) {
//     const form = e.target.closest('form');
//     // Check karein ki yeh sirf profile edit form hai ya nahi
//     if (form && form.getAttribute('action') && form.getAttribute('action').includes('profile')) {
//         e.preventDefault();
        
//         const formData = new FormData(form);
//         let url = form.getAttribute('action') || window.location.href;
//         let absoluteUrl = url.startsWith('http') ? url : window.location.origin + (url.startsWith('/') ? url : '/' + url);
        
//         fetch(absoluteUrl, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
//             }
//         })
//         .then(response => {
//             // Profile update hote hi page reload ho jayega taaki Top Header aur Sidebar mein naya naam/image sync ho jaye
//             location.reload();
//         })
//         .catch(error => console.error('Error submitting form:', error));
//     }
// });

// // Logout Modal
// $(document).ready(function() {
//     // 1. Logout Modal Open Handler
//     $(document).on('click', '#logoutTrigger', function(e) {
//         e.preventDefault();
//         e.stopImmediatePropagation();
//         $('#logoutModal').removeClass('hidden');
//     });

//     // 2. Cancel Button Handler
//     $(document).on('click', '#cancelLogout', function(e) {
//         e.preventDefault();
//         $('#logoutModal').addClass('hidden');
//     });

//     // 3. Close modal on backdrop click
//     $(document).on('click', '#logoutModal', function(e) {
//         if ($(e.target).is('#logoutModal')) {
//             $(this).addClass('hidden');
//         }
//     });
// });


// // Settings Submenu Toggle
// $(document).on('click', '#settingsToggle', function(e) {
//     e.preventDefault();
//     var $submenu = $('#settingsSubmenu');
//     var $chevron = $('#settingsChevron');
    
//     $submenu.toggleClass('hidden');
//     $chevron.toggleClass('rotate-180');
// });

// // Change Password Form AJAX Submission
// $(document).on('submit', '#changePasswordForm', function(e) {
//     e.preventDefault();
    
//     var $form = $(this);
//     var formData = new FormData(this);
//     var $container = $('#dashboard-dynamic-content');
    
//     $.ajax({
//         url: $form.attr('action'),
//         type: 'POST',
//         data: formData,
//         processData: false,
//         contentType: false,
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest',
//             'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
//         },
//         success: function(response) {
//             var parser = new DOMParser();
//             var doc = parser.parseFromString(response, 'text/html');
//             var extractedContent = doc.getElementById('dashboard-dynamic-content');
            
//             if (extractedContent) {
//                 $container.html(extractedContent.innerHTML);
//             } else {
//                 $container.html(`
//                     <div class="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 text-center max-w-xl mx-auto">
//                         <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3 text-lg">
//                             <i class="fa-solid fa-check"></i>
//                         </div>
//                         <h3 class="text-sm font-bold text-slate-900 mb-1">Password Changed Successfully!</h3>
//                         <p class="text-xs text-slate-500">Your account password has been updated securely.</p>
//                     </div>
//                 `);
//             }
//         },
//         error: function(xhr) {
//             var parser = new DOMParser();
//             var doc = parser.parseFromString(xhr.responseText, 'text/html');
//             var extractedContent = doc.getElementById('dashboard-dynamic-content');
//             if (extractedContent) {
//                 $container.html(extractedContent.innerHTML);
//             } else {
//                 $container.html(xhr.responseText);
//             }
//         }
//     });
// });


// document.addEventListener("DOMContentLoaded", function () {
//     const wrapper = document.querySelector('.notif-wrapper');
//     if (!wrapper) return;

//     const btn = wrapper.querySelector('.notif-btn');
//     const dropdown = wrapper.querySelector('.notif-dropdown');

//     btn.addEventListener('click', function (e) {
//         e.stopPropagation();
//         dropdown.classList.toggle('hidden');
//     });

//     document.addEventListener('click', function (e) {
//         if (!wrapper.contains(e.target)) {
//             dropdown.classList.add('hidden');
//         }
//     });

//     // --- MARK ALL READ AJAX LOGIC ---
//     const markAllBtn = document.getElementById('mark-all-read-btn'); // Apne button ki class/id yahan check kar lein
//     if (markAllBtn) {
//         markAllBtn.addEventListener('click', function (e) {
//             e.preventDefault();
            
//             // Yeh URL aap admin ya agent ke anusaar change kar sakte hain
//             const markReadUrl = wrapper.dataset.markUrl || '/mark-ajax-read/'; 

//             fetch(markReadUrl, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken'),
//                     'Content-Type': 'application/json'
//                 }
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     // Page refresh ya notification count/styles update kar dein
//                     location.reload();
//                 } else {
//                     console.error('Failed to mark notifications as read');
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//         });
//     }
// });

// // CSRF token nikalne ke liye helper function (agar pehle se nahi hai)
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }



// // =====================================================
// // NEXT SITE VISIT - MODAL + AJAX SUBMISSION
// // =====================================================
// console.log("NEXT VISIT JS LOADED");
// $(document).on('click', '.next-visit-btn', function(e) {
//     console.log("NEXT VISIT BUTTON CLICKED");
//     e.preventDefault();
//     e.stopImmediatePropagation();

//     var $button = $(this);

//     var visitId = $button.data('visit-id');
//     var customerName = $button.data('customer-name') || '';
//     var propertyName = $button.data('property-name') || '';
//     var currentPropertyId = $button.data('property-id') || '';
//     var nextVisitUrl = $button.data('url');

//     var $modal = $('#nextVisitModal');
//     var $form = $('#nextVisitForm');

//     if ($modal.length === 0 || $form.length === 0) {
//         console.error('Next Visit modal or form not found.');
//         return false;
//     }

//     if (!nextVisitUrl) {
//         console.error('Next Visit URL not found.');
//         alert('Unable to open Next Visit. Please refresh the page and try again.');
//         return false;
//     }

//     // Form reset
//     $form[0].reset();

//     // Back date/time ko block karo
// var $dateInput = $('#nextVisitDate');

// if ($dateInput.length) {

//     var now = new Date();

//     var year = now.getFullYear();
//     var month = String(now.getMonth() + 1).padStart(2, '0');
//     var day = String(now.getDate()).padStart(2, '0');
//     var hours = String(now.getHours()).padStart(2, '0');
//     var minutes = String(now.getMinutes()).padStart(2, '0');

//     var currentDateTime =
//         year + '-' +
//         month + '-' +
//         day + 'T' +
//         hours + ':' +
//         minutes;

//     $dateInput.attr('min', currentDateTime);
// }

//     // Previous visit ID set
//     $('#nextVisitId').val(visitId);

//     // Customer name
//     $('#nextVisitCustomerName').text(customerName);

//     // Property name
//     if (propertyName) {
//         $('#nextVisitPropertyName').text('Property: ' + propertyName);
//     } else {
//         $('#nextVisitPropertyName').text('');
//     }

//     // Property dropdown
//     // Property dropdown
// var $propertySelect = $('#nextVisitProperty');
// var $propertySource = $('#visitProperties-' + visitId);

// if ($propertySelect.length) {

//     // Modal dropdown clear
//     $propertySelect.empty();

//     // Default option
//     $propertySelect.append(
//         '<option value="">-- Select Property --</option>'
//     );

//     // Agent ki available properties load karo
//     if ($propertySource.length) {

//         $propertySource.find('option').each(function() {
//             $propertySelect.append($(this).clone());
//         });

//     }

//     // Previous/current property ko default select karo
//     if (currentPropertyId) {
//         $propertySelect.val(String(currentPropertyId));
//     }
// }

//     // Store backend URL in form
//     $form.attr('action', nextVisitUrl);

//     // Open modal
//     $modal.removeClass('hidden');

//     return false;
// });


// // Close Next Visit Modal
// $(document).on('click', '#closeNextVisitModal, #cancelNextVisitBtn', function(e) {
//     e.preventDefault();

//     var $modal = $('#nextVisitModal');
//     var $form = $('#nextVisitForm');

//     if ($form.length) {
//         $form[0].reset();
//     }

//     $('#nextVisitId').val('');
//     $('#nextVisitCustomerName').text('');
//     $('#nextVisitPropertyName').text('');

//     $modal.addClass('hidden');
// });


// // Close modal when clicking outside modal box
// $(document).on('click', '#nextVisitModal', function(e) {

//     if (e.target === this) {

//         var $modal = $('#nextVisitModal');
//         var $form = $('#nextVisitForm');

//         if ($form.length) {
//             $form[0].reset();
//         }

//         $('#nextVisitId').val('');
//         $('#nextVisitCustomerName').text('');
//         $('#nextVisitPropertyName').text('');

//         $modal.addClass('hidden');
//     }
// });


// // Submit Next Visit Form
// // $(document).on('submit', '#nextVisitForm', function(e) {
// //     e.preventDefault();
// //     e.stopImmediatePropagation();

// //     var form = this;
// //     var $form = $(form);
// //     var $submitButton = $('#submitNextVisitBtn');
// //     var $modal = $('#nextVisitModal');
// //     var $container = $('#dashboard-dynamic-content');

// //     var formActionUrl = $form.attr('action');

// //     if (!formActionUrl) {
// //         alert('Next Visit URL not found. Please refresh the page and try again.');
// //         return false;
// //     }

// //     var formData = new FormData(form);

// //     // Button loading state
// //     var originalButtonText = $submitButton.text();

// //     $submitButton
// //         .prop('disabled', true)
// //         .html(`
// //             <i class="fa-solid fa-spinner fa-spin mr-2"></i>
// //             Submitting...
// //         `);

// //     $.ajax({
// //         url: formActionUrl,
// //         type: 'POST',
// //         data: formData,
// //         processData: false,
// //         contentType: false,
// //         headers: {
// //             'X-Requested-With': 'XMLHttpRequest'
// //         },

// //         success: function(response) {

// //             // Backend JSON response
// //             if (response.success) {

// //                 console.log('Next visit submitted successfully!');

// //                 // Close modal
// //                 $modal.addClass('hidden');

// //                 // Reset form
// //                 form.reset();
// //                 $('#nextVisitId').val('');
// //                 $('#nextVisitCustomerName').text('');
// //                 $('#nextVisitPropertyName').text('');

// //                 // Reload Site Visits content
// //                 var siteVisitsUrl = null;

// //                 if (typeof window.siteVisitsUrl !== 'undefined') {
// //                     siteVisitsUrl = window.siteVisitsUrl;
// //                 }

// //                 // Agar global siteVisitsUrl available hai
// //                 if (siteVisitsUrl) {

// //                     $container.html(`
// //                         <div class="flex items-center justify-center h-64">
// //                             <div class="text-center">
// //                                 <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>
// //                                 <p class="text-xs text-slate-500">
// //                                     Updating site visits...
// //                                 </p>
// //                             </div>
// //                         </div>
// //                     `);

// //                     $.ajax({
// //                         url: siteVisitsUrl,
// //                         type: 'GET',
// //                         headers: {
// //                             'X-Requested-With': 'XMLHttpRequest'
// //                         },

// //                         success: function(refreshResponse) {

// //                             var parser = new DOMParser();
// //                             var doc = parser.parseFromString(
// //                                 refreshResponse,
// //                                 'text/html'
// //                             );

// //                             var extractedContent =
// //                                 doc.getElementById('dashboard-dynamic-content') ||
// //                                 doc.getElementById('dashboard-main-content');

// //                             if (extractedContent) {
// //                                 $container.html(
// //                                     extractedContent.innerHTML
// //                                 );
// //                             } else {
// //                                 $container.html(refreshResponse);
// //                             }
// //                         },

// //                         error: function(xhr) {

// //                             console.error(
// //                                 'Error refreshing site visits:',
// //                                 xhr.responseText
// //                             );

// //                             alert(
// //                                 'Next visit submitted successfully, but the visit list could not be refreshed.'
// //                             );
// //                         }
// //                     });

// //                 } else {

// //                     // Fallback: current Site Visits navigation click
// //                     var $siteVisitsLink = $('#nav-site-visits');

// //                     if ($siteVisitsLink.length) {
// //                         $siteVisitsLink.trigger('click');
// //                     } else {
// //                         location.reload();
// //                     }
// //                 }

// //             } else {

// //                 alert(
// //                     response.message ||
// //                     'Failed to submit next visit.'
// //                 );
// //             }
// //         },

// //         error: function(xhr) {

// //             console.error(
// //                 'Error submitting next visit:',
// //                 xhr.responseText
// //             );

// //             var message =
// //                 'Failed to submit next visit. Please try again.';

// //             // Backend JSON error handle
// //             try {
// //                 var errorResponse = JSON.parse(xhr.responseText);

// //                 if (errorResponse.message) {
// //                     message = errorResponse.message;
// //                 }
// //             } catch (error) {
// //                 console.error(
// //                     'Could not parse error response.'
// //                 );
// //             }

// //             alert(message);
// //         },

// //         complete: function() {

// //             // Button normal state
// //             $submitButton
// //                 .prop('disabled', false)
// //                 .text(originalButtonText);
// //         }
// //     });

// //     return false;
// // });



// // =====================================================
// // SUBMIT NEXT VISIT
// // =====================================================

// $(document).on('submit', '#nextVisitForm', function(e) {

//     e.preventDefault();
//     e.stopImmediatePropagation();

//     var form = this;
//     var $form = $(form);
//     var $submitButton = $('#submitNextVisitBtn');
//     var $modal = $('#nextVisitModal');

//     var formActionUrl = $form.attr('action');

//     if (!formActionUrl) {

//         alert(
//             'Next Visit URL not found. Please refresh the page and try again.'
//         );

//         return false;
//     }

//     var formData = new FormData(form);

//     var originalButtonText =
//         $submitButton.text();

//     $submitButton
//         .prop('disabled', true)
//         .html(`
//             <i class="fa-solid fa-spinner fa-spin mr-2"></i>
//             Scheduling...
//         `);

//     $.ajax({

//         url: formActionUrl,

//         type: 'POST',

//         data: formData,

//         processData: false,

//         contentType: false,

//         headers: {
//             'X-Requested-With': 'XMLHttpRequest'
//         },

//         success: function(response) {

//             if (response.success) {

//                 console.log(
//                     'Next visit scheduled successfully!'
//                 );

//                 // Close modal
//                 $modal.addClass('hidden');

//                 // Reset form
//                 form.reset();

//                 $('#nextVisitId').val('');
//                 $('#nextVisitCustomerName').text('');
//                 $('#nextVisitPropertyName').text('');

//                 // Get Site Visit URL
//                 var siteVisitsUrl = null;

//                 var $siteVisitsLink =
//                     $('#agentSiteVisitsLink');

//                 if ($siteVisitsLink.length) {

//                     siteVisitsUrl =
//                         $siteVisitsLink.data('url') ||
//                         $siteVisitsLink.attr('href');

//                 }

//                 if (
//                     !siteVisitsUrl &&
//                     typeof window.siteVisitsUrl !== 'undefined'
//                 ) {

//                     siteVisitsUrl =
//                         window.siteVisitsUrl;
//                 }

//                 // Refresh Site Visits
//                 if (siteVisitsUrl) {

//                     $('#dashboard-dynamic-content').html(`
//                         <div class="flex items-center justify-center h-64">
//                             <div class="text-center">
//                                 <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>

//                                 <p class="text-xs text-slate-500">
//                                     Updating site visits...
//                                 </p>
//                             </div>
//                         </div>
//                     `);

//                     $.ajax({

//                         url: siteVisitsUrl,

//                         type: 'GET',

//                         headers: {
//                             'X-Requested-With':
//                                 'XMLHttpRequest'
//                         },

//                         success: function(refreshResponse) {

//                             var parser =
//                                 new DOMParser();

//                             var doc =
//                                 parser.parseFromString(
//                                     refreshResponse,
//                                     'text/html'
//                                 );

//                             var extractedContent =
//                                 doc.getElementById(
//                                     'dashboard-dynamic-content'
//                                 ) ||
//                                 doc.getElementById(
//                                     'dashboard-main-content'
//                                 );

//                             if (extractedContent) {

//                                 $('#dashboard-dynamic-content')
//                                     .html(
//                                         extractedContent.innerHTML
//                                     );

//                             } else {

//                                 $('#dashboard-dynamic-content')
//                                     .html(
//                                         refreshResponse
//                                     );
//                             }

//                         },

//                         error: function(xhr) {

//                             console.error(
//                                 'Error refreshing site visits:',
//                                 xhr.responseText
//                             );

//                             alert(
//                                 'Next visit scheduled successfully, but the visit list could not be refreshed.'
//                             );

//                         }

//                     });

//                 } else {

//                     location.reload();

//                 }

//             } else {

//                 alert(
//                     response.message ||
//                     'Failed to schedule next visit.'
//                 );

//             }

//         },

//         error: function(xhr) {

//             console.error(
//                 'Error submitting next visit:',
//                 xhr.responseText
//             );

//             var message =
//                 'Failed to schedule next visit. Please try again.';

//             try {

//                 var errorResponse =
//                     JSON.parse(
//                         xhr.responseText
//                     );

//                 if (errorResponse.message) {

//                     message =
//                         errorResponse.message;

//                 }

//             } catch (error) {

//                 console.error(
//                     'Could not parse error response.'
//                 );

//             }

//             alert(message);

//         },

//         complete: function() {

//             $submitButton
//                 .prop('disabled', false)
//                 .text(originalButtonText);

//         }

//     });

//     return false;
// });




// // =====================================================
// // VIEW SITE VISIT MODAL
// // =====================================================

// $(document).on('click', '.view-visit-btn', function(e) {
//     e.preventDefault();
//     e.stopImmediatePropagation();

//     var $button = $(this);

//     var customerName = $button.attr('data-customer-name') || 'Unknown Customer';
//     var propertyName = $button.attr('data-property-name') || 'Property Not Specified';
//     var location = $button.attr('data-location') || 'Not specified';
//     var notes = $button.attr('data-notes') || 'No notes available.';
//     var status = $button.attr('data-status') || 'Pending';
//     var visitType = $button.attr('data-visit-type') || 'Site Visit';
//     var visitDate = $button.attr('data-visit-date') || 'Date not available';
//     var image = $button.attr('data-image') || '';

//     $('#viewVisitCustomer').text(customerName);
//     $('#viewVisitProperty').text(propertyName);
//     $('#viewVisitType').text(visitType);
//     $('#viewVisitDate').text(visitDate);
//     $('#viewVisitLocation').text(location);
//     $('#viewVisitNotes').text(notes);

//     var $status = $('#viewVisitStatus');

//     $status
//         .removeClass(
//             'text-emerald-400 bg-emerald-950/50 border-emerald-800 ' +
//             'text-rose-400 bg-rose-950/50 border-rose-800 ' +
//             'text-amber-400 bg-amber-950/50 border-amber-800'
//         );

//     $status.text(status);

//     if (status === 'Approved') {

//         $status.addClass(
//             'text-emerald-400 bg-emerald-950/50 border border-emerald-800'
//         );

//     } else if (status === 'Rejected') {

//         $status.addClass(
//             'text-rose-400 bg-rose-950/50 border border-rose-800'
//         );

//     } else {

//         $status.addClass(
//             'text-amber-400 bg-amber-950/50 border border-amber-800'
//         );
//     }

//     if (image) {

//         $('#viewVisitImage')
//             .attr('src', image);

//         $('#viewVisitImageContainer')
//             .removeClass('hidden');

//     } else {

//         $('#viewVisitImage')
//             .attr('src', '');

//         $('#viewVisitImageContainer')
//             .addClass('hidden');
//     }

//     $('#viewVisitModal')
//         .removeClass('hidden');

//     return false;
// });


// // Close View Modal

// $(document).on(
//     'click',
//     '#closeViewVisitModal, #closeViewVisitBtn',
//     function(e) {

//         e.preventDefault();

//         $('#viewVisitModal')
//             .addClass('hidden');

//     }
// );


// // Close View Modal on backdrop

// $(document).on(
//     'click',
//     '#viewVisitModal',
//     function(e) {

//         if (e.target === this) {

//             $('#viewVisitModal')
//                 .addClass('hidden');

//         }

//     }
// );



// // =====================================================
// // AGENT PROFILE DROPDOWN
// // =====================================================

// document.addEventListener("DOMContentLoaded", function () {

//     const profileBtn = document.getElementById("agentProfileBtn");
//     const profileDropdown = document.getElementById("agentProfileDropdown");

//     if (!profileBtn || !profileDropdown) return;

//     // Profile click -> dropdown open/close
//     profileBtn.addEventListener("click", function (e) {

//         e.stopPropagation();

//         profileDropdown.classList.toggle("hidden");

//     });


//     // Dropdown ke bahar click -> close
//     document.addEventListener("click", function (e) {

//         if (
//             !profileBtn.contains(e.target) &&
//             !profileDropdown.contains(e.target)
//         ) {
//             profileDropdown.classList.add("hidden");
//         }

//     });

// });

// =====================================================
// AGENT DASHBOARD JS
// =====================================================


// =====================================================
// 1. MOBILE SIDEBAR TOGGLE
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menu-btn");
    const sidebar = document.getElementById("sidebar");

    if (menuBtn && sidebar) {

        menuBtn.addEventListener("click", function () {

            sidebar.classList.toggle("hidden");
            sidebar.classList.toggle("absolute");
            sidebar.classList.toggle("z-50");
            sidebar.classList.toggle("h-full");

        });

    }

    console.log(
        "Agent Dashboard Script Initialized Successfully!"
    );

});


// =====================================================
// 2. DASHBOARD CHART / SCRIPT REINITIALIZATION
// =====================================================
//
// Jab AJAX ke through dashboard dobara load hota hai,
// innerHTML ke andar ke <script> automatically execute
// nahi hote.
//
// Ye function loaded dashboard ke scripts ko dobara
// execute karta hai.
//
// =====================================================

function reinitializeDashboardScripts(container) {

    if (!container) {
        return;
    }

    const scripts =
        container.querySelectorAll("script");

    if (!scripts.length) {
        return;
    }

    scripts.forEach(function (oldScript) {

        try {

            const newScript =
                document.createElement("script");

            // Script attributes preserve karo
            Array.from(
                oldScript.attributes
            ).forEach(function (attribute) {

                newScript.setAttribute(
                    attribute.name,
                    attribute.value
                );

            });

            // External JS file
            if (oldScript.src) {

                newScript.src =
                    oldScript.src;

            } else {

                // Inline JS
                newScript.textContent =
                    oldScript.textContent;

            }

            oldScript.parentNode.replaceChild(
                newScript,
                oldScript
            );

        } catch (error) {

            console.error(
                "Dashboard script reinitialization error:",
                error
            );

        }

    });

}


// =====================================================
// 3. DASHBOARD CONTENT EXTRACTOR
// =====================================================

function extractDashboardContent(response) {

    const parser =
        new DOMParser();

    const doc =
        parser.parseFromString(
            response,
            "text/html"
        );

    let extractedContent =
        doc.getElementById(
            "dashboard-dynamic-content"
        );

    if (!extractedContent) {

        extractedContent =
            doc.getElementById(
                "dashboard-main-content"
            );

    }

    return extractedContent
        ? extractedContent.innerHTML
        : response;

}


// =====================================================
// 4. LOAD DASHBOARD CONTENT
// =====================================================

function loadAgentDashboardPage(url) {

    if (!url || url === "#") {
        return;
    }

    const container =
        document.getElementById(
            "dashboard-dynamic-content"
        );

    if (!container) {

        console.error(
            "Error: dashboard-dynamic-content container nahi mila!"
        );

        return;
    }


    // ---------------------------------------------
    // Loading
    // ---------------------------------------------

    container.innerHTML = `

        <div class="flex items-center justify-center h-64">

            <div class="text-center">

                <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>

                <p class="text-xs text-slate-500">
                    Loading...
                </p>

            </div>

        </div>

    `;


    // ---------------------------------------------
    // AJAX Request
    // ---------------------------------------------

    $.ajax({

        url: url,

        type: "GET",

        headers: {
            "X-Requested-With":
                "XMLHttpRequest"
        },


        success: function (response) {

            try {

                const html =
                    extractDashboardContent(
                        response
                    );


                // ---------------------------------
                // Content replace
                // ---------------------------------

                container.innerHTML =
                    html;


                // ---------------------------------
                // IMPORTANT:
                // Re-run dashboard scripts
                // ---------------------------------

                setTimeout(function () {

    reinitializeDashboardScripts(container);

    if (typeof window.initMonthlyPerformanceChart === "function") {
        window.initMonthlyPerformanceChart();
    }

    console.log(
        "Dashboard content loaded and scripts reinitialized."
    );

}, 50);

                // ---------------------------------
                // Close mobile sidebar
                // ---------------------------------

                const sidebar =
                    document.getElementById(
                        "sidebar"
                    );

                if (
                    sidebar &&
                    window.innerWidth < 1024
                ) {

                    sidebar.classList.add(
                        "hidden"
                    );

                    sidebar.classList.remove(
                        "absolute"
                    );

                    sidebar.classList.remove(
                        "z-50"
                    );

                    sidebar.classList.remove(
                        "h-full"
                    );

                }


                // ---------------------------------
                // Close profile dropdown
                // ---------------------------------

                const profileDropdown =
                    document.getElementById(
                        "agentProfileDropdown"
                    );

                if (profileDropdown) {

                    profileDropdown.classList.add(
                        "hidden"
                    );

                }


                // ---------------------------------
                // Scroll to content
                // ---------------------------------

                container.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });


            } catch (error) {

                console.error(
                    "Dashboard response parsing error:",
                    error
                );

                container.innerHTML = `

                    <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">

                        <p class="font-bold">
                            Failed to load page.
                        </p>

                        <p>
                            Invalid server response.
                        </p>

                    </div>

                `;

            }

        },


        error: function (xhr, status, error) {

            console.error(
                "Dashboard AJAX Error:",
                error
            );

            console.error(
                "Response:",
                xhr.responseText
            );


            container.innerHTML = `

                <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">

                    <p class="font-bold">
                        Failed to load page.
                    </p>

                    <p>
                        Please try again or check your connection.
                    </p>

                </div>

            `;

        }

    });

}


// =====================================================
// 5. COMMON DASHBOARD NAVIGATION
// =====================================================
//
// IMPORTANT:
// Pehle 3 alag navigation handlers the.
// Ab sirf ONE common handler hai.
//
// =====================================================

$(document).on(
    "click",
    ".ajax-sidebar-link, .nav-link-ajax, #agentPropertiesLink, #nav-site-visits",
    function (e) {

        e.preventDefault();
        e.stopPropagation();

        const link =
            this;

        const url =
            $(link).attr("data-url") ||
            $(link).attr("href");

        if (!url || url === "#") {
            return false;
        }


        loadAgentDashboardPage(
            url
        );

        return false;

    }
);


// =====================================================
// 6. OLD .ajax-link SUPPORT
// =====================================================
//
// Profile ya kisi purane AJAX link ke liye.
//
// =====================================================

document.addEventListener(
    "click",
    function (e) {

        const link =
            e.target.closest(
                ".ajax-link"
            );

        if (!link) {
            return;
        }


        // Agar same element already
        // ajax-sidebar-link hai to common
        // handler ko kaam karne do.

        if (
            link.classList.contains(
                "ajax-sidebar-link"
            )
        ) {

            return;

        }


        e.preventDefault();
        e.stopPropagation();


        const href =
            link.getAttribute(
                "href"
            );

        if (!href || href === "#") {
            return;
        }


        const absoluteUrl =
            href.startsWith("http")
                ? href
                : window.location.origin +
                  (
                      href.startsWith("/")
                          ? href
                          : "/" + href
                  );


        loadAgentDashboardPage(
            absoluteUrl
        );

    }
);


// =====================================================
// 7. SITE VISIT FORM AJAX SUBMISSION
// =====================================================

$(document).on(
    "submit",
    "#siteVisitForm",
    function (e) {

        e.preventDefault();

        const form =
            this;

        const formData =
            new FormData(form);

        const $container =
            $("#dashboard-dynamic-content");

        const formActionUrl =
            $(form).attr("action") ||
            window.location.href;


        if ($container.length === 0) {
            return false;
        }


        $.ajax({

            url: formActionUrl,

            type: "POST",

            data: formData,

            processData: false,

            contentType: false,

            headers: {
                "X-Requested-With":
                    "XMLHttpRequest"
            },


            success: function (response) {

                const html =
                    extractDashboardContent(
                        response
                    );

                $container.html(
                    html
                );


                setTimeout(
                    function () {

                        reinitializeDashboardScripts(
                            $container[0]
                        );

                    },
                    50
                );


                console.log(
                    "Site visit submitted and history updated successfully!"
                );

            },


            error: function (xhr) {

                console.error(
                    "Error in site visit submission:",
                    xhr.responseText
                );

            }

        });


        return false;

    }
);


// =====================================================
// 8. EDIT SITE VISIT - AJAX GET
// =====================================================

$(document).on(
    "click",
    ".edit-visit-btn",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        const rawUrl =
            $(this).attr("href");


        if (!rawUrl || rawUrl === "#") {
            return false;
        }


        const url =
            rawUrl.includes("?")
                ? rawUrl + "&ajax=true"
                : rawUrl + "?ajax=true";


        const $container =
            $("#dashboard-dynamic-content");


        if ($container.length === 0) {
            return false;
        }


        $container.html(`

            <div class="flex items-center justify-center h-64">

                <div class="text-center">

                    <i class="fa-solid fa-spinner fa-spin text-blue-600 text-2xl mb-2"></i>

                    <p class="text-xs text-slate-500">
                        Loading edit form...
                    </p>

                </div>

            </div>

        `);


        $.ajax({

            url: url,

            type: "GET",


            success: function (response) {

                $container.html(
                    response
                );

            },


            error: function (xhr) {

                console.error(
                    "Error loading edit form:",
                    xhr.responseText
                );


                $container.html(`

                    <div class="p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs">

                        <p class="font-bold">
                            Failed to load edit form.
                        </p>

                    </div>

                `);

            }

        });


        return false;

    }
);


// =====================================================
// 9. EDIT SITE VISIT FORM SUBMISSION
// =====================================================

$(document).on(
    "submit",
    "#editSiteVisitForm",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        const form =
            this;

        const formData =
            new FormData(form);

        const $container =
            $("#dashboard-dynamic-content");

        const formActionUrl =
            $(form).attr("action") ||
            window.location.href;


        if ($container.length === 0) {
            return false;
        }


        $.ajax({

            url: formActionUrl,

            type: "POST",

            data: formData,

            processData: false,

            contentType: false,

            headers: {
                "X-Requested-With":
                    "XMLHttpRequest"
            },


            success: function (response) {

                const html =
                    extractDashboardContent(
                        response
                    );

                $container.html(
                    html
                );


                setTimeout(
                    function () {

                        reinitializeDashboardScripts(
                            $container[0]
                        );

                    },
                    50
                );


                console.log(
                    "Site visit updated successfully!"
                );

            },


            error: function (xhr) {

                console.error(
                    "Error updating site visit:",
                    xhr.responseText
                );


                alert(
                    "Failed to update site visit. Please check the form data."
                );

            }

        });


        return false;

    }
);


// =====================================================
// 10. CANCEL EDIT SITE VISIT
// =====================================================

$(document).on(
    "click",
    "#cancelEditBtn",
    function (e) {

        e.preventDefault();


        if (
            typeof siteVisitsUrl !==
            "undefined"
        ) {

            $("#nav-site-visits")
                .trigger("click");

        } else {

            location.reload();

        }

    }
);


// =====================================================
// 11. DELETE SITE VISIT
// =====================================================

$(document).on(
    "click",
    ".delete-visit-btn",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        if (
            !confirm(
                "Are you sure you want to delete this site visit?"
            )
        ) {

            return false;

        }


        const rawUrl =
            $(this).attr("href");


        if (!rawUrl || rawUrl === "#") {
            return false;
        }


        const url =
            rawUrl.includes("?")
                ? rawUrl + "&ajax=true"
                : rawUrl + "?ajax=true";


        const $container =
            $("#dashboard-dynamic-content");


        if ($container.length === 0) {
            return false;
        }


        const csrfToken =
            $('input[name="csrfmiddlewaretoken"]')
                .first()
                .val();


        $.ajax({

            url: url,

            type: "POST",

            data: {
                csrfmiddlewaretoken:
                    csrfToken
            },

            headers: {
                "X-Requested-With":
                    "XMLHttpRequest"
            },


            success: function (response) {

                const html =
                    extractDashboardContent(
                        response
                    );

                $container.html(
                    html
                );


                setTimeout(
                    function () {

                        reinitializeDashboardScripts(
                            $container[0]
                        );

                    },
                    50
                );


                console.log(
                    "Site visit deleted successfully!"
                );

            },


            error: function (xhr) {

                console.error(
                    "Error deleting site visit:",
                    xhr.responseText
                );


                alert(
                    "Failed to delete site visit."
                );

            }

        });


        return false;

    }
);


// =====================================================
// 12. EDIT PROFILE FORM AJAX
// =====================================================

document.addEventListener(
    "submit",
    function (e) {

        const form =
            e.target.closest("form");


        if (
            !form ||
            !form.getAttribute("action") ||
            !form
                .getAttribute("action")
                .includes("profile")
        ) {

            return;

        }


        e.preventDefault();


        const formData =
            new FormData(form);


        const url =
            form.getAttribute("action");


        const absoluteUrl =
            url.startsWith("http")
                ? url
                : window.location.origin +
                  (
                      url.startsWith("/")
                          ? url
                          : "/" + url
                  );


        const csrfInput =
            form.querySelector(
                '[name="csrfmiddlewaretoken"]'
            );


        fetch(
            absoluteUrl,
            {

                method: "POST",

                body: formData,

                headers: {

                    "X-Requested-With":
                        "XMLHttpRequest",

                    "X-CSRFToken":
                        csrfInput
                            ? csrfInput.value
                            : ""

                }

            }
        )

        .then(
            function () {

                location.reload();

            }
        )

        .catch(
            function (error) {

                console.error(
                    "Error submitting profile form:",
                    error
                );

            }
        );

    }
);


// =====================================================
// 13. LOGOUT MODAL
// =====================================================

$(document).on(
    "click",
    "#logoutTrigger, #profileLogoutTrigger",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        $("#logoutModal")
            .removeClass("hidden");

    }
);


$(document).on(
    "click",
    "#cancelLogout",
    function (e) {

        e.preventDefault();


        $("#logoutModal")
            .addClass("hidden");

    }
);


$(document).on(
    "click",
    "#logoutModal",
    function (e) {

        if (
            $(e.target).is(
                "#logoutModal"
            )
        ) {

            $(this)
                .addClass("hidden");

        }

    }
);


// =====================================================
// 14. SETTINGS SUBMENU
// =====================================================

$(document).on(
    "click",
    "#settingsToggle",
    function (e) {

        e.preventDefault();


        const $submenu =
            $("#settingsSubmenu");

        const $chevron =
            $("#settingsChevron");


        $submenu.toggleClass(
            "hidden"
        );

        $chevron.toggleClass(
            "rotate-180"
        );

    }
);


// =====================================================
// 15. CHANGE PASSWORD
// =====================================================

$(document).on(
    "submit",
    "#changePasswordForm",
    function (e) {

        e.preventDefault();


        const $form =
            $(this);

        const formData =
            new FormData(this);

        const $container =
            $("#dashboard-dynamic-content");


        $.ajax({

            url:
                $form.attr("action"),

            type:
                "POST",

            data:
                formData,

            processData:
                false,

            contentType:
                false,

            headers: {

                "X-Requested-With":
                    "XMLHttpRequest",

                "X-CSRFToken":
                    $form
                        .find(
                            'input[name="csrfmiddlewaretoken"]'
                        )
                        .val()

            },


            success: function (response) {

                const html =
                    extractDashboardContent(
                        response
                    );


                if (html) {

                    $container.html(
                        html
                    );

                }


                setTimeout(
                    function () {

                        reinitializeDashboardScripts(
                            $container[0]
                        );

                    },
                    50
                );

            },


            error: function (xhr) {

                const html =
                    extractDashboardContent(
                        xhr.responseText
                    );


                if (html) {

                    $container.html(
                        html
                    );

                } else {

                    $container.html(
                        xhr.responseText
                    );

                }

            }

        });

    }
);


// =====================================================
// 16. NOTIFICATION DROPDOWN
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const wrapper =
            document.querySelector(
                ".notif-wrapper"
            );


        if (!wrapper) {
            return;
        }


        const btn =
            wrapper.querySelector(
                ".notif-btn"
            );

        const dropdown =
            wrapper.querySelector(
                ".notif-dropdown"
            );


        if (!btn || !dropdown) {
            return;
        }


        btn.addEventListener(
            "click",
            function (e) {

                e.stopPropagation();

                dropdown.classList.toggle(
                    "hidden"
                );

            }
        );


        document.addEventListener(
            "click",
            function (e) {

                if (
                    !wrapper.contains(
                        e.target
                    )
                ) {

                    dropdown.classList.add(
                        "hidden"
                    );

                }

            }
        );


        const markAllBtn =
            document.getElementById(
                "mark-all-read-btn"
            );


        if (markAllBtn) {

            markAllBtn.addEventListener(
                "click",
                function (e) {

                    e.preventDefault();


                    const markReadUrl =
                        wrapper.dataset.markUrl ||
                        "/mark-ajax-read/";


                    fetch(
                        markReadUrl,
                        {

                            method:
                                "POST",

                            headers: {

                                "X-CSRFToken":
                                    getCookie(
                                        "csrftoken"
                                    ),

                                "Content-Type":
                                    "application/json"

                            }

                        }
                    )

                    .then(
                        response =>
                            response.json()
                    )

                    .then(
                        data => {

                            if (
                                data.success
                            ) {

                                location.reload();

                            }

                        }
                    )

                    .catch(
                        error => {

                            console.error(
                                "Notification error:",
                                error
                            );

                        }
                    );

                }
            );

        }

    }
);


// =====================================================
// 17. CSRF COOKIE
// =====================================================

function getCookie(name) {

    let cookieValue =
        null;


    if (
        document.cookie &&
        document.cookie !== ""
    ) {

        const cookies =
            document.cookie.split(";");


        for (
            let i = 0;
            i < cookies.length;
            i++
        ) {

            const cookie =
                cookies[i].trim();


            if (
                cookie.substring(
                    0,
                    name.length + 1
                ) ===
                name + "="
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;

            }

        }

    }


    return cookieValue;

}


// =====================================================
// 18. NEXT SITE VISIT - OPEN MODAL
// =====================================================

console.log(
    "NEXT VISIT JS LOADED"
);


$(document).on(
    "click",
    ".next-visit-btn",
    function (e) {

        console.log(
            "NEXT VISIT BUTTON CLICKED"
        );


        e.preventDefault();

        e.stopImmediatePropagation();


        const $button =
            $(this);


        const visitId =
            $button.data(
                "visit-id"
            );


        const customerName =
            $button.data(
                "customer-name"
            ) || "";


        const propertyName =
            $button.data(
                "property-name"
            ) || "";


        const currentPropertyId =
            $button.data(
                "property-id"
            ) || "";


        const nextVisitUrl =
            $button.data(
                "url"
            );


        const $modal =
            $("#nextVisitModal");


        const $form =
            $("#nextVisitForm");


        if (
            $modal.length === 0 ||
            $form.length === 0
        ) {

            console.error(
                "Next Visit modal or form not found."
            );

            return false;

        }


        if (!nextVisitUrl) {

            alert(
                "Unable to open Next Visit. Please refresh the page and try again."
            );

            return false;

        }


        $form[0].reset();


        // -----------------------------------------
        // Minimum date/time
        // -----------------------------------------

        const $dateInput =
            $("#nextVisitDate");


        if ($dateInput.length) {

            const now =
                new Date();


            const year =
                now.getFullYear();


            const month =
                String(
                    now.getMonth() + 1
                ).padStart(
                    2,
                    "0"
                );


            const day =
                String(
                    now.getDate()
                ).padStart(
                    2,
                    "0"
                );


            const hours =
                String(
                    now.getHours()
                ).padStart(
                    2,
                    "0"
                );


            const minutes =
                String(
                    now.getMinutes()
                ).padStart(
                    2,
                    "0"
                );


            const currentDateTime =
                year +
                "-" +
                month +
                "-" +
                day +
                "T" +
                hours +
                ":" +
                minutes;


            $dateInput.attr(
                "min",
                currentDateTime
            );

        }


        $("#nextVisitId")
            .val(visitId);


        $("#nextVisitCustomerName")
            .text(customerName);


        if (propertyName) {

            $("#nextVisitPropertyName")
                .text(
                    "Property: " +
                    propertyName
                );

        } else {

            $("#nextVisitPropertyName")
                .text("");

        }


        // -----------------------------------------
        // Property dropdown
        // -----------------------------------------

        const $propertySelect =
            $("#nextVisitProperty");


        const $propertySource =
            $("#visitProperties-" + visitId);


        if ($propertySelect.length) {

            $propertySelect.empty();


            $propertySelect.append(
                '<option value="">-- Select Property --</option>'
            );


            if ($propertySource.length) {

                $propertySource
                    .find("option")
                    .each(function () {

                        $propertySelect.append(
                            $(this).clone()
                        );

                    });

            }


            if (currentPropertyId) {

                $propertySelect.val(
                    String(
                        currentPropertyId
                    )
                );

            }

        }


        $form.attr(
            "action",
            nextVisitUrl
        );


        $modal.removeClass(
            "hidden"
        );


        return false;

    }
);


// =====================================================
// 19. CLOSE NEXT VISIT MODAL
// =====================================================

$(document).on(
    "click",
    "#closeNextVisitModal, #cancelNextVisitBtn",
    function (e) {

        e.preventDefault();


        const $modal =
            $("#nextVisitModal");


        const $form =
            $("#nextVisitForm");


        if ($form.length) {

            $form[0].reset();

        }


        $("#nextVisitId")
            .val("");


        $("#nextVisitCustomerName")
            .text("");


        $("#nextVisitPropertyName")
            .text("");


        $modal.addClass(
            "hidden"
        );

    }
);


// =====================================================
// 20. NEXT VISIT MODAL BACKDROP
// =====================================================

$(document).on(
    "click",
    "#nextVisitModal",
    function (e) {

        if (
            e.target === this
        ) {

            const $modal =
                $("#nextVisitModal");


            const $form =
                $("#nextVisitForm");


            if ($form.length) {

                $form[0].reset();

            }


            $("#nextVisitId")
                .val("");


            $("#nextVisitCustomerName")
                .text("");


            $("#nextVisitPropertyName")
                .text("");


            $modal.addClass(
                "hidden"
            );

        }

    }
);


// =====================================================
// 21. SUBMIT NEXT VISIT
// =====================================================

$(document).on(
    "submit",
    "#nextVisitForm",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        const form =
            this;


        const $form =
            $(form);


        const $submitButton =
            $("#submitNextVisitBtn");


        const $modal =
            $("#nextVisitModal");


        const formActionUrl =
            $form.attr(
                "action"
            );


        if (!formActionUrl) {

            alert(
                "Next Visit URL not found. Please refresh the page and try again."
            );

            return false;

        }


        const formData =
            new FormData(form);


        const originalButtonText =
            $submitButton.text();


        $submitButton
            .prop(
                "disabled",
                true
            )
            .html(`
                <i class="fa-solid fa-spinner fa-spin mr-2"></i>
                Scheduling...
            `);


        $.ajax({

            url:
                formActionUrl,

            type:
                "POST",

            data:
                formData,

            processData:
                false,

            contentType:
                false,

            headers: {

                "X-Requested-With":
                    "XMLHttpRequest"

            },


            success: function (response) {

                if (!response.success) {

                    alert(
                        response.message ||
                        "Failed to schedule next visit."
                    );

                    return;

                }


                console.log(
                    "Next visit scheduled successfully!"
                );


                $modal.addClass(
                    "hidden"
                );


                form.reset();


                $("#nextVisitId")
                    .val("");


                $("#nextVisitCustomerName")
                    .text("");


                $("#nextVisitPropertyName")
                    .text("");


                // ---------------------------------
                // Site Visits URL
                // ---------------------------------

                let siteVisitsUrl =
                    null;


                const $siteVisitsLink =
                    $("#agentSiteVisitsLink");


                if (
                    $siteVisitsLink.length
                ) {

                    siteVisitsUrl =
                        $siteVisitsLink.data(
                            "url"
                        ) ||
                        $siteVisitsLink.attr(
                            "href"
                        );

                }


                if (
                    !siteVisitsUrl &&
                    typeof window.siteVisitsUrl !==
                    "undefined"
                ) {

                    siteVisitsUrl =
                        window.siteVisitsUrl;

                }


                // ---------------------------------
                // Refresh Site Visits
                // ---------------------------------

                if (siteVisitsUrl) {

                    loadAgentDashboardPage(
                        siteVisitsUrl
                    );

                } else {

                    location.reload();

                }

            },


            error: function (xhr) {

                console.error(
                    "Error submitting next visit:",
                    xhr.responseText
                );


                let message =
                    "Failed to submit next visit. Please try again.";


                try {

                    const errorResponse =
                        JSON.parse(
                            xhr.responseText
                        );


                    if (
                        errorResponse.message
                    ) {

                        message =
                            errorResponse.message;

                    }

                } catch (error) {

                    console.error(
                        "Could not parse error response."
                    );

                }


                alert(
                    message
                );

            },


            complete: function () {

                $submitButton
                    .prop(
                        "disabled",
                        false
                    )
                    .text(
                        originalButtonText
                    );

            }

        });


        return false;

    }
);


// =====================================================
// 22. VIEW SITE VISIT MODAL
// =====================================================

$(document).on(
    "click",
    ".view-visit-btn",
    function (e) {

        e.preventDefault();

        e.stopImmediatePropagation();


        const $button =
            $(this);


        const customerName =
            $button.attr(
                "data-customer-name"
            ) ||
            "Unknown Customer";


        const propertyName =
            $button.attr(
                "data-property-name"
            ) ||
            "Property Not Specified";


        const location =
            $button.attr(
                "data-location"
            ) ||
            "Not specified";


        const notes =
            $button.attr(
                "data-notes"
            ) ||
            "No notes available.";


        const status =
            $button.attr(
                "data-status"
            ) ||
            "Pending";


        const visitType =
            $button.attr(
                "data-visit-type"
            ) ||
            "Site Visit";


        const visitDate =
            $button.attr(
                "data-visit-date"
            ) ||
            "Date not available";


        const image =
            $button.attr(
                "data-image"
            ) ||
            "";


        $("#viewVisitCustomer")
            .text(customerName);


        $("#viewVisitProperty")
            .text(propertyName);


        $("#viewVisitType")
            .text(visitType);


        $("#viewVisitDate")
            .text(visitDate);


        $("#viewVisitLocation")
            .text(location);


        $("#viewVisitNotes")
            .text(notes);


        const $status =
            $("#viewVisitStatus");


        $status.removeClass(
            "text-emerald-400 bg-emerald-950/50 border-emerald-800 " +
            "text-rose-400 bg-rose-950/50 border-rose-800 " +
            "text-amber-400 bg-amber-950/50 border-amber-800"
        );


        $status.text(
            status
        );


        if (
            status === "Approved"
        ) {

            $status.addClass(
                "text-emerald-400 bg-emerald-950/50 border border-emerald-800"
            );

        } else if (
            status === "Rejected"
        ) {

            $status.addClass(
                "text-rose-400 bg-rose-950/50 border border-rose-800"
            );

        } else {

            $status.addClass(
                "text-amber-400 bg-amber-950/50 border border-amber-800"
            );

        }


        if (image) {

            $("#viewVisitImage")
                .attr(
                    "src",
                    image
                );


            $("#viewVisitImageContainer")
                .removeClass(
                    "hidden"
                );

        } else {

            $("#viewVisitImage")
                .attr(
                    "src",
                    ""
                );


            $("#viewVisitImageContainer")
                .addClass(
                    "hidden"
                );

        }


        $("#viewVisitModal")
            .removeClass(
                "hidden"
            );


        return false;

    }
);


// =====================================================
// 23. CLOSE VIEW SITE VISIT MODAL
// =====================================================

$(document).on(
    "click",
    "#closeViewVisitModal, #closeViewVisitBtn",
    function (e) {

        e.preventDefault();


        $("#viewVisitModal")
            .addClass(
                "hidden"
            );

    }
);


// =====================================================
// 24. CLOSE VIEW MODAL - BACKDROP
// =====================================================

$(document).on(
    "click",
    "#viewVisitModal",
    function (e) {

        if (
            e.target === this
        ) {

            $("#viewVisitModal")
                .addClass(
                    "hidden"
                );

        }

    }
);


// =====================================================
// 25. AGENT PROFILE DROPDOWN
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const profileBtn =
            document.getElementById(
                "agentProfileBtn"
            );


        const profileDropdown =
            document.getElementById(
                "agentProfileDropdown"
            );


        if (
            !profileBtn ||
            !profileDropdown
        ) {

            return;

        }


        // -----------------------------------------
        // Open / Close
        // -----------------------------------------

        profileBtn.addEventListener(
            "click",
            function (e) {

                e.preventDefault();

                e.stopPropagation();


                profileDropdown.classList.toggle(
                    "hidden"
                );

            }
        );


        // -----------------------------------------
        // Outside click
        // -----------------------------------------

        document.addEventListener(
            "click",
            function (e) {

                if (
                    !profileBtn.contains(
                        e.target
                    ) &&
                    !profileDropdown.contains(
                        e.target
                    )
                ) {

                    profileDropdown.classList.add(
                        "hidden"
                    );

                }

            }
        );

    }
);
