//About Us why choose us
document.addEventListener("DOMContentLoaded", function () {
    const grid = document.querySelector(".choose-grid");

    if (!grid) return;

    function slideAndRotate() {
        const cards = grid.querySelectorAll(".choose-card");
        if (cards.length === 0) return;

        const firstCard = cards[0];
        const cardWidth = firstCard.offsetWidth + 20; // Card size + 20px gap

        // 1. Smoothly slide left
        grid.style.transition = "transform 0.5s ease-in-out";
        grid.style.transform = `translateX(-${cardWidth}px)`;

        // 2. Transition khatam hone par pehle card ko right side shifted me append karein
        setTimeout(() => {
            grid.style.transition = "none";
            grid.style.transform = "translateX(0)";
            grid.appendChild(firstCard); // Pehla card left se nikalke right me chala jayega
        }, 500);
    }

    // Har 2.5 second me autorotate hoga
    let interval = setInterval(slideAndRotate, 2500);

    // Hover par pause / leave par play
    grid.addEventListener("mouseenter", () => clearInterval(interval));
    grid.addEventListener("mouseleave", () => interval = setInterval(slideAndRotate, 2500));
});

document.addEventListener("DOMContentLoaded", function () {
    // const propertyCards = document.querySelectorAll(".property-card");
    const propertyCards = document.querySelectorAll(
    ".property-card:not(.properties-page-card)"
);
    const projectCards = document.querySelectorAll(".project-card");
    
    const modal = document.getElementById("propertyPopupModal");
    const closeBtn = document.getElementById("closePopupBtn");
    
    const modalTrack = document.getElementById("modalSliderTrack");
    const modalTitle = document.getElementById("modalTitle");
    const modalLocation = document.getElementById("modalLocation");
    const modalPrice = document.getElementById("modalPrice");
    const modalBeds = document.getElementById("modalBeds");
    const modalBaths = document.getElementById("modalBaths");
    const modalArea = document.getElementById("modalArea");
    const modalDesc = document.getElementById("modalDesc");
    
    const nextBtn = document.getElementById("modalNextBtn");
    const prevBtn = document.getElementById("modalPrevBtn");

    const requestCallBtn = document.getElementById("projectRequestCallBtn");

    let currentSlide = 0;

    // 1. Featured Properties Click (Slider ke sath)
    propertyCards.forEach(card => {
        card.style.cursor = "pointer";
        card.addEventListener("click", function () {
            if (!modal || !modalTrack) return;

            const location = card.getAttribute("data-location") || "";
            const locationText = modalLocation && modalLocation.querySelector("span");
            if (modalTitle) modalTitle.textContent = card.getAttribute("data-title") || "Property Details";
            if (locationText) {
                locationText.textContent = location;
            } else if (modalLocation) {
                modalLocation.textContent = location;
            }
            if (modalPrice) modalPrice.textContent = "₹ " + (card.getAttribute("data-price") || "On Request");
            if (modalBeds) modalBeds.textContent = (card.getAttribute("data-beds") || "0") + " Beds";
            if (modalBaths) modalBaths.textContent = (card.getAttribute("data-baths") || "0") + " Baths";
            if (modalArea) modalArea.textContent = (card.getAttribute("data-area") || "0") + " Sq.Ft.";
            if (modalDesc) {
                modalDesc.textContent = card.getAttribute("data-description")
                    || "Spacious property located at " + location + " featuring modern amenities.";
            }

            // Properties ke liye arrows show karein
            if (nextBtn) nextBtn.style.display = "flex";
            if (prevBtn) prevBtn.style.display = "flex";

            if (requestCallBtn) requestCallBtn.style.display = "inline-flex";

            let imageList = [];
            const mainImg = card.getAttribute("data-main");
            if (mainImg) imageList.push(mainImg);

            try {
                const galleryStr = card.getAttribute("data-gallery");
                if (galleryStr) {
                    const gallery = JSON.parse(galleryStr);
                    if (Array.isArray(gallery)) {
                        gallery.forEach(imgUrl => {
                            if (!imageList.includes(imgUrl)) imageList.push(imgUrl);
                        });
                    }
                }
            } catch (e) {
                console.error("Unable to load property image gallery.", e);
            }

            modalTrack.innerHTML = "";
            imageList.forEach(url => {
                const slide = document.createElement("div");
                slide.classList.add("popup-modal-slide");
                const image = document.createElement("img");
                image.src = url;
                image.alt = "Property Image";
                slide.appendChild(image);
                modalTrack.appendChild(slide);
            });

            currentSlide = 0;
            updateModalSlider();
            if (modal) modal.style.display = "flex";
        });
    });

    // 2. Featured Projects Click (Keval Single Image, No Slider)
    projectCards.forEach(card => {
        card.style.cursor = "pointer";
        card.addEventListener("click", function () {
            if (!modal || !modalTrack) return;

            const title = card.querySelector("h3");
            const location = card.querySelector(".location");
            const overview = card.querySelector("ul li");
            const projectImage = card.querySelector(".project-image img");
            if (modalTitle) modalTitle.textContent = title ? title.textContent.trim() : "Project Details";
            if (modalLocation) modalLocation.textContent = location ? location.textContent.trim() : "";
            if (modalPrice) modalPrice.textContent = "₹ On Request";
            if (modalBeds) modalBeds.textContent = "Project Overview";
            if (modalBaths) modalBaths.textContent = "";
            if (modalArea) modalArea.textContent = card.getAttribute("data-amenities")
                || (overview ? overview.textContent.trim() : "");
            if (modalDesc) modalDesc.textContent = card.getAttribute("data-description")
                || "Explore exclusive features, modern architecture, and high-class construction standards for this project.";

            // Projects ke liye arrows hide kar dein taaki slider na chale
            if (nextBtn) nextBtn.style.display = "none";
            if (prevBtn) prevBtn.style.display = "none";

            if (requestCallBtn) requestCallBtn.style.display = "inline-flex";

            modalTrack.innerHTML = "";
            if (projectImage) {
                const slide = document.createElement("div");
                slide.classList.add("popup-modal-slide");
                const image = document.createElement("img");
                image.src = projectImage.currentSrc || projectImage.src;
                image.alt = title ? title.textContent.trim() : "Project Image";
                slide.appendChild(image);
                modalTrack.appendChild(slide);
            }

            currentSlide = 0;
            updateModalSlider();
            if (modal) modal.style.display = "flex";
        });
    });

    function updateModalSlider() {
        const slides = modalTrack.querySelectorAll(".popup-modal-slide");
        if (slides.length > 0) {
            modalTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        }
    }

    if (nextBtn) {
        nextBtn.onclick = function () {
            const slides = modalTrack.querySelectorAll(".popup-modal-slide");
            if (slides.length > 1) {
                currentSlide = (currentSlide + 1) % slides.length;
                updateModalSlider();
            }
        };
    }

    if (prevBtn) {
        prevBtn.onclick = function () {
            const slides = modalTrack.querySelectorAll(".popup-modal-slide");
            if (slides.length > 1) {
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                updateModalSlider();
            }
        };
    }

    if (closeBtn) {
        closeBtn.onclick = () => { if (modal) modal.style.display = "none"; };
    }
    if (modal) {
        modal.addEventListener("click", function (event) {
            if (event.target === modal) modal.style.display = "none";
        });
    }
});

// Latest Blog

document.addEventListener("DOMContentLoaded", function () {
    // Agar page par '.blogs-grid-box' ya blogs page ki koi class hai, toh ye script yahin ruk jayegi
    if (document.querySelector(".blogs-page-container")) {
        return; 
    }

    // 1. Popup Modal CSS ko Dynamically Inject karna
    const style = document.createElement('style');
    style.innerHTML = `
        .js-blog-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.65);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            backdrop-filter: blur(4px);
        }
        .js-blog-content {
            background: #fff;
            width: 650px;
            max-width: 90%;
            max-height: 85vh;
            border-radius: 12px;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            animation: jsPopupAnim 0.3s ease;
        }
        @keyframes jsPopupAnim {
            from { transform: scale(0.9); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .js-blog-close {
            position: absolute;
            top: 12px; right: 18px;
            font-size: 28px; font-weight: bold;
            color: #ffffff; cursor: pointer; z-index: 10;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.75);
        }
        .js-blog-close:hover { color: #ffffff; }
        .js-blog-img { width: 100%; height: 260px; object-fit: cover; }
        .js-blog-body { padding: 20px; }
        .js-blog-date { font-size: 13px; color: #ea580c; font-weight: 600; display: block; margin-bottom: 6px; }
        .js-blog-title { font-size: 20px; color: #111827; margin: 0 0 12px 0; font-weight: bold; }
        .js-blog-desc { font-size: 14px; color: #4b5563; line-height: 1.6; border-top: 1px solid #eee; padding-top: 12px; }
    `;
    document.head.appendChild(style);

    // 2. Popup Modal HTML ko Dynamically Append karna
    const modalHTML = `
        <div id="jsBlogModal" class="js-blog-overlay">
            <div class="js-blog-content">
                <span id="jsBlogClose" class="js-blog-close">&times;</span>
                <img id="jsBlogImg" class="js-blog-img" src="" alt="Blog Image">
                <div class="js-blog-body">
                    <span id="jsBlogDate" class="js-blog-date"></span>
                    <h2 id="jsBlogTitle" class="js-blog-title"></h2>
                    <p id="jsBlogDesc" class="js-blog-desc"></p>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // 3. Elements Target karna
    const blogModal = document.getElementById("jsBlogModal");
    const closeBtn = document.getElementById("jsBlogClose");
    const modalImg = document.getElementById("jsBlogImg");
    const modalDate = document.getElementById("jsBlogDate");
    const modalTitle = document.getElementById("jsBlogTitle");
    const modalDesc = document.getElementById("jsBlogDesc");

    // 4. Latest Blog Cards Automatic Detect karke Event Attach karna
    const blogCards = document.querySelectorAll(".blog-card, .blog-item, .properties-section + div .grid > div");
    let targetCards = blogCards.length > 0 ? blogCards : Array.from(document.querySelectorAll('div')).filter(el => el.innerText && el.innerText.includes('Read More'));

    targetCards.forEach(card => {
        card.style.cursor = "pointer";
        card.addEventListener("click", function (e) {
            e.preventDefault();

            const titleEl = card.querySelector("h3, h4, .blog-title");
            const dateEl = card.querySelector("span, small, .blog-date, [class*='date']");
            const imgEl = card.querySelector("img");
            
            const title = titleEl ? titleEl.innerText : "Blog Details";
            const date = dateEl ? dateEl.innerText : "Latest Post";
            const imgSrc = imgEl ? imgEl.src : "";
            
            modalTitle.innerText = title;
            modalDate.innerText = "📅 " + date;
            modalImg.src = imgSrc;
            modalImg.style.display = imgSrc ? "block" : "none";
            
            modalDesc.innerText = "This is the full article for '" + title + "'. It contains all the detailed information, market analysis, and insights for real estate trends.";

            blogModal.style.display = "flex";
        });
    });

    // 5. Close Button & Outside Click Event
    if (closeBtn && blogModal) {
        closeBtn.onclick = () => blogModal.style.display = "none";
        window.onclick = (e) => {
            if (e.target === blogModal) blogModal.style.display = "none";
        };
    }
});

// Properties page 
// Properties page

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('propertyPopupModal');
    const closeBtn = document.getElementById('closePopupBtn');

    // Sirf Properties page ke cards
    const cards = document.querySelectorAll('.properties-page-card');

    const modalTrack = document.getElementById('modalSliderTrack');
    const modalTitle = document.getElementById('modalTitle');
    const modalLocation = document.getElementById('modalLocation');
    const modalPrice = document.getElementById('modalPrice');
    const modalBeds = document.getElementById('modalBeds');
    const modalBaths = document.getElementById('modalBaths');
    const modalArea = document.getElementById('modalArea');
    const modalDesc = document.getElementById('modalDesc');

    const nextBtn = document.getElementById('modalNextBtn');
    const prevBtn = document.getElementById('modalPrevBtn');

    const modalEnquiryBtn = document.getElementById('modalEnquiryBtn');
    const modalBookPropertyBtn = document.getElementById('modalBookPropertyBtn');

    
    // -------------------------
// Enquiry Now Button
// -------------------------

if (modalEnquiryBtn) {

    modalEnquiryBtn.addEventListener('click', function (e) {

        e.preventDefault();
        e.stopPropagation();

        const propertyId =
            this.getAttribute('data-property-id');

        const propertyTitle =
            modalTitle ? modalTitle.innerText.trim() : '';

        console.log(
            'Enquiry button clicked:',
            propertyId,
            propertyTitle
        );

        


        // ---------------------------------
        // Open Existing Enquiry Modal
        // ---------------------------------

        const enquiryModal =
            document.getElementById('enquiryModal');

        if (!enquiryModal) {
            console.error(
                'Enquiry modal (#enquiryModal) not found.'
            );
            return;
        }

        // ---------------------------------
        // Property ID store karo
        // ---------------------------------

        enquiryModal.setAttribute(
            'data-property-id',
            propertyId || ''
        );

        // ---------------------------------
        // Optional Subject Field
        // ---------------------------------

        const subjectField =
            enquiryModal.querySelector(
                '[name="subject"]'
            );

        if (subjectField && propertyTitle) {

            subjectField.value =
                'Enquiry for: ' + propertyTitle;

        }

        // ---------------------------------
        // Optional Message Field
        // ---------------------------------

        const messageField =
            enquiryModal.querySelector(
                '[name="message"]'
            );

        if (messageField && propertyTitle) {

            messageField.value =
                'I am interested in the property: ' +
                propertyTitle +
                '. Please provide more details.';

        }

        // ---------------------------------
        // Property ID hidden input
        // Agar already hai to value update
        // ---------------------------------

        const propertyIdField =
            enquiryModal.querySelector(
                '[name="property_id"]'
            );

        if (propertyIdField) {

            propertyIdField.value =
                propertyId || '';

        }

        // ---------------------------------
        // Open Enquiry Modal
        // ---------------------------------

        enquiryModal.classList.add('active');

        console.log(
            'Enquiry modal opened for property:',
            propertyId,
            propertyTitle
        );

    });

}

    // -------------------------
// Book Property Button
// -------------------------

if (modalBookPropertyBtn) {

    modalBookPropertyBtn.addEventListener('click', function (e) {

        e.preventDefault();
        e.stopPropagation();

        const propertyId =
            this.getAttribute('data-property-id');

        if (!propertyId) {
            console.error('Property ID not found for booking.');
            return;
        }

        const propertyCard = document.querySelector(
            '.properties-page-card[data-property-id="' + propertyId + '"]'
        );

        if (!propertyCard) {
            console.error('Property card not found.');
            return;
        }

        // Existing Save Property button se login state read karenge
        const saveBtn =
            propertyCard.querySelector('.btn-save-property');

        const isLoggedIn =
            saveBtn?.dataset.authenticated === 'true';

        const userRole =
            saveBtn?.dataset.role;

        // Selected property preserve karo
        window.selectedPropertyId = propertyId;

        // Booking action remember karo
        window.propertyActionType = 'booking';

        // Logged-in customer
        if (isLoggedIn && userRole === 'customer') {

            if (typeof window.openPropertyBooking === 'function') {

                window.openPropertyBooking(propertyId);

            } else {

                console.error(
                    'Property booking function not available.'
                );

            }

            return;
        }

        // Logged-out / non-customer
        const loginModal =
            document.getElementById('loginPopupModal');

        if (loginModal) {
            loginModal.style.display = 'flex';
        }

    });

}

    let currentSlide = 0;

    if (cards.length && modal) {

        cards.forEach(card => {

            card.style.cursor = 'pointer';

            card.addEventListener('click', function (e) {

                // BOOKED property par detail modal open nahi hoga
                if (card.dataset.booked === 'true') {
                    return;
                }

                // Wishlist button click par modal open na ho
                if (
                    e.target.closest('.btn-save-property') ||
                    e.target.closest('.book-property-btn')
                ) {
                    return;
                }

                const propertyId = card.getAttribute('data-property-id');

                // -------------------------
                // Property Details
                // -------------------------

                modalTitle.innerText =
                    card.getAttribute('data-title') || '';

                modalLocation.innerHTML =
                    '<i class="fa-solid fa-location-dot"></i> ' +
                    (card.getAttribute('data-location') || '');

                modalPrice.innerText =
                    '₹ ' + (card.getAttribute('data-price') || '');

                modalBeds.textContent =
                    (card.getAttribute('data-beds') || '') + ' Beds';

                modalBaths.textContent =
                    (card.getAttribute('data-baths') || '') + ' Baths';

                modalArea.textContent =
                    (card.getAttribute('data-area') || '') + ' Sq.Ft.';

                modalDesc.innerText =
                    card.getAttribute('data-description') || '';

                // -------------------------
                // Gallery Images
                // -------------------------

                let imageList = [];

                const mainImg = card.getAttribute('data-main');

                if (mainImg) {
                    imageList.push(mainImg);
                }

                const galleryElement = document.getElementById(
                    'property-gallery-' + propertyId
                );

                if (galleryElement) {
                    try {
                        const gallery = JSON.parse(
                            galleryElement.textContent
                        );

                        if (Array.isArray(gallery)) {
                            gallery.forEach(function (imgUrl) {
                                if (
                                    imgUrl &&
                                    !imageList.includes(imgUrl)
                                ) {
                                    imageList.push(imgUrl);
                                }
                            });
                        }

                    } catch (error) {
                        console.error(
                            'Property gallery JSON error:',
                            error
                        );
                    }
                }

                // -------------------------
                // Load Images into Slider
                // -------------------------

                modalTrack.innerHTML = '';

                imageList.forEach(function (url) {

                    const slide = document.createElement('div');

                    slide.classList.add(
                        'popup-modal-slide'
                    );

                    const img = document.createElement('img');

                    img.src = url;
                    img.alt = 'Property Image';

                    slide.appendChild(img);
                    modalTrack.appendChild(slide);
                });

                // -------------------------
                // Reset Slider
                // -------------------------

                currentSlide = 0;

                updatePropertiesModalSlider();

                // Arrows
                if (imageList.length > 1) {
                    if (nextBtn) {
                        nextBtn.style.display = 'flex';
                    }

                    if (prevBtn) {
                        prevBtn.style.display = 'flex';
                    }
                } else {
                    if (nextBtn) {
                        nextBtn.style.display = 'none';
                    }

                    if (prevBtn) {
                        prevBtn.style.display = 'none';
                    }
                }

                // -------------------------
                // Modal Buttons
                // -------------------------

                if (modalEnquiryBtn) {
                    modalEnquiryBtn.setAttribute(
                        'data-property-id',
                        propertyId
                    );
                }

                if (modalBookPropertyBtn) {
                    modalBookPropertyBtn.setAttribute(
                        'data-property-id',
                        propertyId
                    );
                }

                // -------------------------
                // Open Modal
                // -------------------------

                modal.style.display = 'flex';
            });
        });
    }

    // -------------------------
    // Properties Modal Slider
    // -------------------------

    function updatePropertiesModalSlider() {

        const slides =
            modalTrack.querySelectorAll(
                '.popup-modal-slide'
            );

        if (slides.length > 0) {

            modalTrack.style.transform =
                'translateX(-' +
                (currentSlide * 100) +
                '%)';
        }
    }

    // Next
    if (nextBtn) {

        nextBtn.addEventListener('click', function (e) {

            e.stopPropagation();

            const slides =
                modalTrack.querySelectorAll(
                    '.popup-modal-slide'
                );

            if (slides.length > 1) {

                currentSlide =
                    (currentSlide + 1) %
                    slides.length;

                updatePropertiesModalSlider();
            }
        });
    }

    // Previous
    if (prevBtn) {

        prevBtn.addEventListener('click', function (e) {

            e.stopPropagation();

            const slides =
                modalTrack.querySelectorAll(
                    '.popup-modal-slide'
                );

            if (slides.length > 1) {

                currentSlide =
                    (currentSlide - 1 + slides.length) %
                    slides.length;

                updatePropertiesModalSlider();
            }
        });
    }

    // -------------------------
    // Close Modal
    // -------------------------

    if (closeBtn) {

        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (e) {

        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // 1. MODAL OPEN / CLOSE LOGIC
    // ==========================================
    const modal = document.getElementById('enquiryModal');
    const openBtnFloating = document.getElementById('openEnquiryModal');
    const closeBtn = document.getElementById('closeEnquiryModal');
    const navEnquiryBtns = document.querySelectorAll('.btn-enquiry');

    function openModal(e) {
        if (e) e.preventDefault();
        if (modal) {
            modal.classList.add('active');
        }
    }

    function closeModal() {
        if (modal) {
            modal.classList.remove('active');
        }
    }

    // Floating tab click
    if (openBtnFloating) {
        openBtnFloating.addEventListener('click', openModal);
    }

    // Navbar enquiry buttons click
    navEnquiryBtns.forEach(function (btn) {
        btn.addEventListener('click', openModal);
    });

    // Close button click
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    //Visit Schedule 
    const visitModal = document.getElementById('visitModal');
    const scheduleVisitBtns = document.querySelectorAll('.btn-schedule-visit');
    const closeVisitBtn = document.getElementById('closeVisitModal');

    function openVisitModalFunc(e) {
        if (e) e.preventDefault();
        if (visitModal) {
            visitModal.style.display = 'flex'; 
        }
    }

    // Yahan e.stopPropagation() add kiya gaya hai taaki event bubble hokar doosre modals ko na khole
  function closeVisitModalFunc(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
    }

    if (visitModal) {
        visitModal.style.display = 'none';
    }
}

    scheduleVisitBtns.forEach(function (btn) {
        btn.addEventListener('click', function(e) {
             e.preventDefault(); 
             e.stopPropagation(); // Button click par event rokne ke liye
            openVisitModalFunc(e);
        });
    });

  if (closeVisitBtn) {
    closeVisitBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        if (visitModal) {
            visitModal.style.display = 'none';
        }
    });
}
    


    // Background overlay click to close
   // ✅ FIX - dono modals ke liye separate listeners
if (modal) {
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
}

if (visitModal) {
    visitModal.addEventListener('click', function(e) {
        if (e.target === visitModal) {
            closeVisitModalFunc(e);
        }
    });
}


    // ==========================================
    // 2. UNIVERSAL FORM SUBMIT & SWEETALERT LOGIC
    // ==========================================
    const allForms = document.querySelectorAll('form');

    allForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            // Bypass GET forms (Search/Filters) and specific Dashboard/Contact forms safely
            if (this.method.toUpperCase() === 'GET' || this.id === 'contactForm' || this.id === 'skip-ajax-form') {
                return; 
            }

            e.preventDefault(); 

            let currentForm = this;
            let formData = new FormData(currentForm);

            fetch(currentForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {

                    // Check karein form kis modal ke andar hai
                    const isVisitForm = currentForm.closest('#visitModal');
                    const isEnquiryForm = currentForm.closest('#enquiryModal');

                    // Schedule Visit modal close
                    if (isVisitForm && visitModal) {
                        visitModal.style.display = 'none';
                    }

                    // Enquiry modal close
                    if (isEnquiryForm) {
                        closeModal();
                    }

                    if (typeof Swal !== 'undefined') {

                        if (isVisitForm) {
                            Swal.fire({
                                title: 'Visit Scheduled!',
                                text: 'Your visit request has been submitted successfully. Our team will contact you shortly.',
                                icon: 'success',
                                confirmButtonColor: '#ff6600',
                                confirmButtonText: 'Great!'
                            });
                        } else {
                            Swal.fire({
                                title: 'Enquiry Submitted!',
                                text: 'Thank you for reaching out. Our team will contact you shortly.',
                                icon: 'success',
                                confirmButtonColor: '#ff6600',
                                confirmButtonText: 'Great!'
                            });
                        }
                    }

                    currentForm.reset();

                } else {
                    throw new Error('Server response error');
                }
            })
            .catch(error => {
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        title: 'Submission Failed',
                        text: 'Something went wrong while sending your request. Please try again.',
                        icon: 'error',
                        confirmButtonColor: '#ff6600',
                        confirmButtonText: 'Try Again'
                    });
                }
            });
        });
    });
});

// Helper function: Browser Cookies se Django CSRF Token nikale ke liye
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



/* Projects Page */

// Project Detail Popup Modal Logic
document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.theme-project-card');
    
    cards.forEach(card => {
        card.addEventListener('click', function () {
            const title = this.getAttribute('data-title');
            const location = this.getAttribute('data-location');
            const description = this.getAttribute('data-description');
            const image = this.getAttribute('data-image');
            const status = this.getAttribute('data-status');
            const possession = this.getAttribute('data-possession');

            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalLocText').innerText = location;
            document.getElementById('modalDesc').innerText = description;
            document.getElementById('modalImg').src = image;
            document.getElementById('modalStatus').innerText = status;
            document.getElementById('modalPossession').innerText = possession;

            document.getElementById('projectModal').style.display = 'flex';
        });
    });
});

function closeProjectModal() {
    document.getElementById('projectModal').style.display = 'none';
}



/* Blog */
document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.querySelector(".blog-search-form");
    const searchInput = document.querySelector("input[name='q']");
    const categoryDropdown = document.querySelector(".category-dropdown");

    // 1. Page load hone par URL check karega: agar category ya search nahi hai, toh dropdown aur input ko default kar dega
    const urlParams = new URLSearchParams(window.location.search);
    
    if (!urlParams.has('category') || urlParams.get('category') === '') {
        if (categoryDropdown) categoryDropdown.value = "";
    }

    // 2. Search form submit hone par input ko clear kar dega
    if (searchForm) {
        searchForm.addEventListener("submit", function() {
            setTimeout(function() {
                if (searchInput) searchInput.value = "";
            }, 100);
        });
    }
});

// 3. Full Blog Content Modal Functions (Read More & Image click ke liye)
function openBlogModal(imgSrc, title, date, content) {
    const modal = document.getElementById('blogModal');
    const modalImg = document.getElementById('modalBlogImg');
    const modalTitle = document.getElementById('modalBlogTitle');
    const modalDate = document.getElementById('modalBlogDate');
    const modalContent = document.getElementById('modalBlogContent');

    if (modal) {
        if (modalImg) modalImg.src = imgSrc;
        if (modalTitle) modalTitle.innerText = title;
        if (modalDate) modalDate.innerText = date;
        if (modalContent) modalContent.innerHTML = content;
        
        modal.style.display = 'flex';
    }
}

function closeBlogModal() {
    const modal = document.getElementById('blogModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Modal ke bahar dark background par click karne se bhi modal close ho jaye
window.onclick = function(event) {
    const modal = document.getElementById('blogModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


// Register Page

// document.addEventListener("DOMContentLoaded", function() {
//     console.log("Wireframe Registration JS Loaded!");

//     const form = document.querySelector('.reg-center-card form');
//     if (form) {
//         form.addEventListener('submit', function(e) {
//             const pass = document.querySelector('input[name="password"]').value;
//             const confirmPass = document.querySelector('input[name="confirm_password"]').value;

//             if (pass !== confirmPass) {
//                 alert("Passwords do not match! Please check.");
//                 e.preventDefault();
//             }
//         });
//     }
// });


// Register Page
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector(".reg-center-card form");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();

        const password = form.querySelector('input[name="password"]').value;
        const confirmPassword = form.querySelector('input[name="confirm_password"]').value;
        const invalidFields = Array.from(form.elements)
            .filter(field => field.willValidate && !field.checkValidity());

        if (invalidFields.length) {
            Swal.fire({
                title: "Check Your Details",
                text: invalidFields.map(field => field.validationMessage).join("\n"),
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        if (password !== confirmPassword) {
            Swal.fire({
                title: "Password Mismatch",
                text: "Passwords do not match. Please check again.",
                icon: "warning",
                confirmButtonText: "OK"
            });
            return;
        }

        
if (password.length < 8) {
    Swal.fire({
        title: "Weak Password",
        text: "Password must be at least 8 characters long.",
        icon: "warning",
        confirmButtonText: "OK"
    });
    return;
}

if (/^\d+$/.test(password)) {
    Swal.fire({
        title: "Weak Password",
        text: "Password cannot contain only numbers.",
        icon: "warning",
        confirmButtonText: "OK"
    });
    return;
}

if (/^[a-zA-Z]+$/.test(password)) {
    Swal.fire({
        title: "Weak Password",
        text: "Password cannot contain only letters.",
        icon: "warning",
        confirmButtonText: "OK"
    });
    return;
}



        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(async response => {
            const result = await response.json();

            if (result.success) {
                Swal.fire({
                    title: "Registration Successful!",
                    text: "Your account has been created successfully.",
                    icon: "success",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "#2563eb"
                }).then(() => {
                    window.location.href = result.redirect_url || form.dataset.loginUrl;
                });
                return;
            }

            Swal.fire({
                title: "Registration Failed",
                text: (result.errors || ["Please check your details and try again."]).join("\n"),
                icon: "error",
                confirmButtonText: "OK",
                confirmButtonColor: "#2563eb"
            });
        })
        .catch(error => {
            console.error("Registration error:", error);
            Swal.fire({
                title: "Unable to Register",
                text: "Something went wrong while submitting your registration. Please try again.",
                icon: "error",
                confirmButtonText: "OK",
                confirmButtonColor: "#2563eb"
            });
        });
    }, true);
});


// Main Login Form

// document.addEventListener("DOMContentLoaded", function () {

//     const loginForm = document.getElementById("authLoginForm");
//     const authModal = document.getElementById("authModalOverlay");

//     if (!loginForm) return;

//     loginForm.addEventListener("submit", function (e) {

//         e.preventDefault();
//         e.stopImmediatePropagation();

//         const formData = new FormData(loginForm);

//         fetch(loginForm.action, {
//             method: "POST",
//             body: formData,
//             headers: {
//                 "X-Requested-With": "XMLHttpRequest",
//                 "X-CSRFToken": getCookie("csrftoken")
//             }
//         })
//         .then(response => response.text().then(html => ({
//             html: html,
//             url: response.url
//         })))
//         .then(data => {

//             // WRONG EMAIL / PASSWORD
//             if (data.html.includes("Invalid email/mobile or password.")) {

//                 // Login modal close
//                 if (authModal) {
//                     authModal.style.display = "none";
//                 }

//                 Swal.fire({
//                     title: "Login Failed",
//                     text: "Invalid email/mobile or password.",
//                     icon: "error",
//                     confirmButtonText: "Try Again",
//                     confirmButtonColor: "#2563eb",
//                     didOpen: () => {
//                         Swal.getContainer().style.zIndex = "100000";
//                     }
//                 });

//                 return;
//             }

//             // ADMIN ACCESS ERROR
//             if (data.html.includes("Access Denied: You are not authorized as an Admin.")) {

//                 if (authModal) {
//                     authModal.style.display = "none";
//                 }

//                 Swal.fire({
//                     title: "Access Denied",
//                     text: "You are not authorized as an Admin.",
//                     icon: "warning",
//                     confirmButtonText: "OK",
//                     didOpen: () => {
//                         Swal.getContainer().style.zIndex = "100000";
//                     }
//                 });

//                 return;
//             }

//             // AGENT ACCESS ERROR
//             if (data.html.includes("Access Denied: This is not an Agent account.")) {

//                 if (authModal) {
//                     authModal.style.display = "none";
//                 }

//                 Swal.fire({
//                     title: "Access Denied",
//                     text: "This is not an Agent account.",
//                     icon: "warning",
//                     confirmButtonText: "OK",
//                     didOpen: () => {
//                         Swal.getContainer().style.zIndex = "100000";
//                     }
//                 });

//                 return;
//             }

//             // CUSTOMER PORTAL ERROR
//             if (data.html.includes("Please use the Admin or Agent portal to login.")) {

//                 if (authModal) {
//                     authModal.style.display = "none";
//                 }

//                 Swal.fire({
//                     title: "Wrong Portal",
//                     text: "Please use the Admin or Agent portal to login.",
//                     icon: "warning",
//                     confirmButtonText: "OK",
//                     didOpen: () => {
//                         Swal.getContainer().style.zIndex = "100000";
//                     }
//                 });

//                 return;
//             }

//             // LOGIN SUCCESS
//             const finalPath = new URL(
//                 data.url,
//                 window.location.origin
//             ).pathname;

//             const loginPath = window.location.pathname;

//             if (finalPath !== loginPath) {

//                 // Login modal close
//                 if (authModal) {
//                     authModal.style.display = "none";
//                 }

//                 Swal.fire({
//                     title: "Login Successfully!",
//                     text: "Welcome back!",
//                     icon: "success",
//                     confirmButtonText: "Continue",
//                     confirmButtonColor: "#2563eb",
//                     allowOutsideClick: false,
//                     didOpen: () => {
//                         Swal.getContainer().style.zIndex = "100000";
//                     }
//                 }).then(() => {

//                     // Django original redirect
//                     window.location.href = data.url;

//                 });

//                 return;
//             }

//             // Unknown login error
//             if (authModal) {
//                 authModal.style.display = "none";
//             }

//             Swal.fire({
//                 title: "Login Failed",
//                 text: "Please check your email/mobile and password.",
//                 icon: "error",
//                 confirmButtonText: "Try Again",
//                 didOpen: () => {
//                     Swal.getContainer().style.zIndex = "100000";
//                 }
//             });

//         })
//         .catch(error => {

//             console.error("Login error:", error);

//             // Modal close on unexpected error
//             if (authModal) {
//                 authModal.style.display = "none";
//             }

//             Swal.fire({
//                 title: "Something Went Wrong",
//                 text: "Please try again.",
//                 icon: "error",
//                 confirmButtonText: "OK",
//                 didOpen: () => {
//                     Swal.getContainer().style.zIndex = "100000";
//                 }
//             });

//         });

//     }, true);

// });



// ==========================================
// MAIN LOGIN FORM - LOGIN ONLY
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("authLoginForm");
    const authModal = document.getElementById("authModalOverlay");

    // Login form/page par hi chale
    if (!loginForm || !authModal) return;


    // ------------------------------------------
    // LOGIN TOAST FUNCTION
    // ------------------------------------------

    function showLoginToast(title, message, type = "success", duration = 2500) {

        let toast = document.getElementById("dreamHomeLoginToast");

        // Agar toast already nahi hai to create karo
        if (!toast) {

            toast = document.createElement("div");
            toast.id = "dreamHomeLoginToast";

            document.body.appendChild(toast);
        }

        let icon = "✓";

        if (type === "error") {
            icon = "✕";
        } else if (type === "warning") {
            icon = "!";
        }

        toast.innerHTML = `
            <div class="login-toast-icon ${type}">
                ${icon}
            </div>

            <div class="login-toast-content">
                <div class="login-toast-title">
                    ${title}
                </div>

                <div class="login-toast-message">
                    ${message}
                </div>
            </div>

            <button type="button" class="login-toast-close">
                ×
            </button>
        `;

        // Show toast
        setTimeout(function () {
            toast.classList.add("show");
        }, 10);


        // Close button
        const closeButton = toast.querySelector(".login-toast-close");

        if (closeButton) {
            closeButton.addEventListener("click", function () {
                toast.classList.remove("show");
            });
        }


        // Auto hide
        if (duration > 0) {

            setTimeout(function () {

                if (toast) {
                    toast.classList.remove("show");
                }

            }, duration);
        }
    }


    // ------------------------------------------
    // LOGIN SUBMIT
    // ------------------------------------------

    loginForm.addEventListener("submit", function (e) {

        e.preventDefault();
        e.stopImmediatePropagation();

        const formData = new FormData(loginForm);


        fetch(loginForm.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            }
        })

        .then(response => {

            return response.text().then(html => ({
                html: html,
                url: response.url
            }));

        })

        .then(data => {

            // ------------------------------------------
            // CHECK FINAL URL
            // ------------------------------------------

            const finalPath = new URL(
                data.url,
                window.location.origin
            ).pathname;

            const loginPath = window.location.pathname;


            // ------------------------------------------
            // INVALID EMAIL / PASSWORD
            // ------------------------------------------

            if (
                data.html.includes(
                    "Invalid email/mobile or password."
                )
            ) {

                authModal.style.display = "none";

                showLoginToast(
                    "Login Failed",
                    "Invalid email/mobile or password.",
                    "error",
                    3000
                );

                return;
            }


            // ------------------------------------------
            // ADMIN ACCESS ERROR
            // ------------------------------------------

            if (
                data.html.includes(
                    "Access Denied: You are not authorized as an Admin."
                )
            ) {

                authModal.style.display = "none";

                showLoginToast(
                    "Access Denied",
                    "You are not authorized as an Admin.",
                    "warning",
                    3000
                );

                return;
            }


            // ------------------------------------------
            // AGENT ACCESS ERROR
            // ------------------------------------------

            if (
                data.html.includes(
                    "Access Denied: This is not an Agent account."
                )
            ) {

                authModal.style.display = "none";

                showLoginToast(
                    "Access Denied",
                    "This is not an Agent account.",
                    "warning",
                    3000
                );

                return;
            }


            // ------------------------------------------
            // CUSTOMER PORTAL ERROR
            // ------------------------------------------

            if (
                data.html.includes(
                    "Please use the Admin or Agent portal to login."
                )
            ) {

                authModal.style.display = "none";

                showLoginToast(
                    "Wrong Portal",
                    "Please use the Admin or Agent portal to login.",
                    "warning",
                    3000
                );

                return;
            }


            // ------------------------------------------
            // LOGIN SUCCESS
            // ------------------------------------------

            if (finalPath !== loginPath) {

                authModal.style.display = "none";

                showLoginToast(
                    "Login Successful!",
                    "Welcome back! Redirecting...",
                    "success",
                    1800
                );


                // Automatic redirect after 1.5 seconds
                setTimeout(function () {

                    window.location.href = data.url;

                }, 1500);

                return;
            }


            // ------------------------------------------
            // UNKNOWN LOGIN ERROR
            // ------------------------------------------

            authModal.style.display = "none";

            showLoginToast(
                "Login Failed",
                "Please check your email/mobile and password.",
                "error",
                3000
            );

        })

        .catch(error => {

            console.error("Login error:", error);

            authModal.style.display = "none";

            showLoginToast(
                "Something Went Wrong",
                "Please try again.",
                "error",
                3000
            );

        });

    }, true);

});




// Property Booking + Saved Property Login Popup
// document.addEventListener("DOMContentLoaded", function () {

//     const bookBtns = document.querySelectorAll(".book-property-btn");
//     const saveBtns = document.querySelectorAll(".btn-save-property");

//     const loginModal = document.getElementById("loginPopupModal");
//     const closeLogin = document.getElementById("closeLoginPopup");
//     const loginForm = document.getElementById("popupLoginForm");
//     const loginError = document.getElementById("loginError");

//     let selectedPropertyId = null;
//     let actionType = null;

//     // Book Property
//     bookBtns.forEach(btn => {
//         btn.addEventListener("click", function (e) {
//             e.preventDefault();
//             e.stopPropagation();

//             selectedPropertyId = this.dataset.propertyId;
//             actionType = "booking";

//             const isLoggedIn = this.dataset.authenticated === "true";
//             const userRole = this.dataset.role;

//             if (isLoggedIn && userRole === "customer") {
//                 window.location.href = 
//                     "/customers/book-property/" + selectedPropertyId + "/";
//                 return;
//             }

//             if (loginModal) {
//                 loginModal.style.display = "flex";
//             }
//         });
//     });

//     // Save Property 
//     saveBtns.forEach(btn => { 
//         btn.addEventListener("click", function (e) { 
//             e.preventDefault(); 
//             e.stopPropagation(); 
    
//             selectedPropertyId = this.dataset.propertyId; 
//             actionType = "save"; 
    
//             const isLoggedIn = this.dataset.authenticated === "true";
//             const userRole = this.dataset.role;
    
//             if (isLoggedIn && userRole === "customer") { 
//                 window.location.href = 
//                     "/customers/save-property/" + selectedPropertyId + "/"; 
//                 return; 
//             } 
    
//             if (loginModal) { 
//                 loginModal.style.display = "flex"; 
//             } 
//         }); 
//     });

//     // Close Login Popup
//     closeLogin?.addEventListener("click", function () {
//         loginModal.style.display = "none";
//     });

//     loginModal?.addEventListener("click", function (e) {
//         if (e.target === loginModal) {
//             loginModal.style.display = "none";
//         }
//     });

//     // Login
//     loginForm?.addEventListener("submit", async function (e) {
//         e.preventDefault();

//         loginError.textContent = "";

//         const formData = new FormData(loginForm);
//         const loginUrl = loginForm.dataset.loginUrl;

//         try {
//             const response = await fetch(loginUrl, {
//                 method: "POST",
//                 body: formData
//             });

//             const data = await response.json();

//             if (data.success) {

//                 if (actionType === "booking") {
//                     window.location.href =
//                         "/customers/book-property/" + selectedPropertyId + "/";
//                 }

//                 if (actionType === "save") {
//                     window.location.href =
//                         "/customers/save-property/" + selectedPropertyId + "/";
//                 }

//             } else {
//                 loginError.textContent = data.message;
//             }

//         } catch (error) {
//             loginError.textContent =
//                 "Something went wrong. Please try again.";
//         }
//     });

// });



// Property Booking + Saved Property Login Popup
document.addEventListener("DOMContentLoaded", function () {

    const bookBtns = document.querySelectorAll(".book-property-btn");
    const saveBtns = document.querySelectorAll(".btn-save-property");

    const loginModal = document.getElementById("loginPopupModal");
    const closeLogin = document.getElementById("closeLoginPopup");
    const loginForm = document.getElementById("popupLoginForm");
    const loginError = document.getElementById("loginError");

    // Booking Popup
    const bookingModal = document.getElementById("bookingPopupModal");
    const closeBooking = document.getElementById("closeBookingPopup");
    const cancelBookingBtn = document.getElementById("cancelBookingBtn");
    const bookingForm = document.getElementById("bookingConfirmationForm");

    const bookingPropertyName =
        document.getElementById("bookingPropertyName");

    const bookingPropertyLocation =
        document.getElementById("bookingPropertyLocation");

    const bookingPropertyPrice =
        document.getElementById("bookingPropertyPrice");

    const bookingCustomerName =
        document.getElementById("bookingCustomerName");

    const bookingCustomerMobile =
        document.getElementById("bookingCustomerMobile");

    const bookingCustomerEmail =
        document.getElementById("bookingCustomerEmail");

    let selectedPropertyId = null;
    let actionType = null;


    // =========================================================
    // OPEN BOOKING POPUP
    // =========================================================

    window.openPropertyBooking = function (propertyId) {

        selectedPropertyId = propertyId;

        // const propertyBtn = document.querySelector(
        //     '.book-property-btn[data-property-id="' + propertyId + '"]'
        // );

        // if (!propertyBtn) {
        //     console.error("Property booking button not found.");
        //     return;
        // }

        // const propertyCard = propertyBtn.closest(".property-card");

        const propertyCard = document.querySelector(
    '.properties-page-card[data-property-id="' + propertyId + '"]'
        );

        

        if (!propertyCard) {
            console.error("Property card not found.");
            return;
        }

        const title =
            propertyCard.dataset.title || "-";

        const location =
            propertyCard.dataset.location || "-";

        const price =
            propertyCard.dataset.price || "-";


        // Property details
        if (bookingPropertyName) {
            bookingPropertyName.textContent = title;
        }

        if (bookingPropertyLocation) {
            bookingPropertyLocation.textContent =
                "📍 " + location;
        }

        if (bookingPropertyPrice) {
            bookingPropertyPrice.textContent = price;
        }


        // =====================================================
        // LOGGED-IN CUSTOMER DETAILS
        // =====================================================

        const customerName =
            bookingForm?.dataset.customerName || "";

        const customerEmail =
            bookingForm?.dataset.customerEmail || "";

        const customerMobile =
            bookingForm?.dataset.customerMobile || "";


        if (bookingCustomerName) {
            bookingCustomerName.value = customerName;
        }

        if (bookingCustomerEmail) {
            bookingCustomerEmail.value = customerEmail;
        }

        if (bookingCustomerMobile) {
            bookingCustomerMobile.value = customerMobile;
        }


        // Reset dealer selection
        const dealerRadios =
            bookingForm?.querySelectorAll(
                'input[name="is_property_dealer"]'
            );

        dealerRadios?.forEach(function (radio) {
            radio.checked = false;
        });


        // Open popup
        if (bookingModal) {
            bookingModal.style.display = "flex";
        }
    }


    // =========================================================
    // BOOK PROPERTY BUTTON
    // =========================================================

    bookBtns.forEach(function (btn) {

    btn.addEventListener("click", function (e) {

        e.preventDefault();
        e.stopPropagation();

        selectedPropertyId =
            this.dataset.propertyId;

        actionType = "booking";

        // Login ke baad isi property ko booking ke liye open karna hai
        window.selectedPropertyId = selectedPropertyId;
        window.propertyActionType = "booking";

            const isLoggedIn =
                this.dataset.authenticated === "true";

            const userRole =
                this.dataset.role;


            // Already logged-in customer
            if (isLoggedIn && userRole === "customer") {

                window.openPropertyBooking(selectedPropertyId);

                return;
            }


            // Not logged in
            if (loginModal) {
                loginModal.style.display = "flex";
            }

        });

    });


    // =========================================================
    // SAVE PROPERTY
    // =========================================================

    saveBtns.forEach(function (btn) {

        btn.addEventListener("click", function (e) {

            e.preventDefault();
            e.stopPropagation();

            selectedPropertyId =
                this.dataset.propertyId;

            actionType = "save";

            const isLoggedIn =
                this.dataset.authenticated === "true";

            const userRole =
                this.dataset.role;


            // Existing save-property flow
            if (isLoggedIn && userRole === "customer") {

                window.location.href =
                    "/customers/save-property/" +
                    selectedPropertyId +
                    "/";

                return;
            }


            // Login required
            if (loginModal) {
                loginModal.style.display = "flex";
            }

        });

    });


    // =========================================================
    // CLOSE LOGIN POPUP
    // =========================================================

    closeLogin?.addEventListener("click", function () {

        if (loginModal) {
            loginModal.style.display = "none";
        }

    });


    loginModal?.addEventListener("click", function (e) {

        if (e.target === loginModal) {

            loginModal.style.display = "none";

        }

    });


    // =========================================================
    // POPUP LOGIN
    // =========================================================

    loginForm?.addEventListener("submit", async function (e) {

        e.preventDefault();

        if (loginError) {
            loginError.textContent = "";
        }

        const formData =
            new FormData(loginForm);

        const loginUrl =
            loginForm.dataset.loginUrl;


        try {

            const response = await fetch(loginUrl, {

                method: "POST",
                body: formData

            });


            const data =
                await response.json();


            if (data.success) {

            if (loginModal) {
                loginModal.style.display = "none";
            }

            // Booking action
            if (window.propertyActionType === "booking") {

                const propertyId =
                    window.selectedPropertyId;

                if (data.customer && bookingForm) {

                    bookingForm.dataset.customerName =
                        data.customer.name || "";

                    bookingForm.dataset.customerEmail =
                        data.customer.email || "";

                    bookingForm.dataset.customerMobile =
                        data.customer.mobile || "";
                }

                window.openPropertyBooking(propertyId);

                return;
            }

            // Save property action
            if (actionType === "save") {

                window.location.href =
                    "/customers/save-property/" +
                    selectedPropertyId +
                    "/";

                return;
            }


                // Existing save property flow
                if (actionType === "save") {

                    window.location.href =
                        "/customers/save-property/" +
                        selectedPropertyId +
                        "/";

                    return;
                }


            } else {

                if (loginError) {

                    loginError.textContent =
                        data.message;

                }

            }


        } catch (error) {

            console.error(
                "Popup login error:",
                error
            );

            if (loginError) {

                loginError.textContent =
                    "Something went wrong. Please try again.";

            }

        }

    });


    // =========================================================
    // CLOSE BOOKING POPUP
    // =========================================================

    function closeBookingPopup() {

        if (bookingModal) {

            bookingModal.style.display =
                "none";

        }

    }


    closeBooking?.addEventListener(
        "click",
        closeBookingPopup
    );


    cancelBookingBtn?.addEventListener(
        "click",
        closeBookingPopup
    );


    bookingModal?.addEventListener(
        "click",
        function (e) {

            if (e.target === bookingModal) {

                closeBookingPopup();

            }

        }
    );


    // =========================================================
    // CONFIRM & BOOK
    // =========================================================

    bookingForm?.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            e.stopPropagation();

            e.stopImmediatePropagation();


            if (!selectedPropertyId) {

                Swal.fire({

                    title: "Property Not Selected",

                    text: "Please select a property first.",

                    icon: "warning",

                    confirmButtonColor: "#2563eb"

                });

                return;
            }


            const formData =
                new FormData(bookingForm);


            const bookingUrl =
                "/customers/book-property/" +
                selectedPropertyId +
                "/";


            const confirmBtn =
                document.getElementById(
                    "confirmBookingBtn"
                );


            if (confirmBtn) {

                confirmBtn.disabled = true;

                confirmBtn.textContent =
                    "Booking...";

            }


            try {

                const response = await fetch(
                    bookingUrl,
                    {
                        method: "POST",

                        body: formData,

                        headers: {

                            "X-Requested-With":
                                "XMLHttpRequest",

                            "X-CSRFToken":
                                getCookie("csrftoken")

                        }

                    }
                );


                const data =
                    await response.json();


                if (data.success) {

                    closeBookingPopup();


                    if (typeof Swal !== "undefined") {

                        Swal.fire({
                            toast: true,
                            position: "top-end",
                            icon: "success",
                            title: "Booking Successful",
                            text:
                                data.message ||
                                "Booking request submitted successfully. Pending admin confirmation.",
                            showConfirmButton: false,
                            timer: 4000,
                            timerProgressBar: true
                        }).then(function () {

                            window.location.reload();

                        });

                    } else {

                        window.location.reload();

                    }


                } else {

                    Swal.fire({

                        title: "Booking Failed",

                        text:
                            data.message ||
                            "Unable to complete your booking.",

                        icon: "error",

                        confirmButtonColor:
                            "#2563eb",

                        confirmButtonText:
                            "Try Again"

                    });

                }


            } catch (error) {

                console.error(
                    "Booking error:",
                    error
                );


                Swal.fire({

                    title: "Something Went Wrong",

                    text:
                        "Unable to complete your booking. Please try again.",

                    icon: "error",

                    confirmButtonColor:
                        "#2563eb",

                    confirmButtonText:
                        "Try Again"

                });


            } finally {

                if (confirmBtn) {

                    confirmBtn.disabled = false;

                    confirmBtn.textContent =
                        "Confirm & Book";

                }

            }

        },

        true
    );

});





// Home Search: Refresh par search filters reset
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/" && window.location.search) {
        window.history.replaceState(
            {},
            document.title,
            window.location.pathname
        );
    }
});


window.addEventListener("click", function (e) {
    const modal = document.getElementById("projectModal");

    if (e.target === modal) {
        modal.style.display = "none";
    }
});


document.addEventListener("click", function (e) {
    const modal = document.getElementById("blogModal");

    if (e.target === modal) {
        modal.style.display = "none";
    }
});




/* ================================================================= */
/* MOBILE INTERACTIONS - Hamburger Menu, Auto-Scroll, Auto-Rotate */
/* ================================================================= */

// ================================================================= //
// 1. HAMBURGER MENU TOGGLE
// ================================================================= //
document.addEventListener('DOMContentLoaded', function() {
    
    // ================================================================= //
    // 2. AUTO-SCROLL TESTIMONIALS
    // ================================================================= //
    const testimonialSlides = document.querySelectorAll('.testimonial-slide');
    const testimonialDots = document.querySelectorAll('.dot');
    let currentSlide = 0;
    let testimonialAutoScrollInterval;

    function showTestimonialSlide(n) {
        if (testimonialSlides.length === 0) return;

        if (n >= testimonialSlides.length) {
            currentSlide = 0;
        } else if (n < 0) {
            currentSlide = testimonialSlides.length - 1;
        } else {
            currentSlide = n;
        }

        // Hide all slides
        testimonialSlides.forEach(slide => {
            slide.classList.remove('active');
        });

        // Remove active class from all dots
        testimonialDots.forEach(dot => {
            dot.classList.remove('active');
        });

        // Show current slide
        if (testimonialSlides[currentSlide]) {
            testimonialSlides[currentSlide].classList.add('active');
        }

        // Highlight current dot
        if (testimonialDots[currentSlide]) {
            testimonialDots[currentSlide].classList.add('active');
        }
    }

    function autoScrollTestimonials() {
        currentSlide++;
        showTestimonialSlide(currentSlide);
    }

    // Add click handlers to testimonial arrows if they exist
    const prevArrow = document.querySelector('.testimonial-arrow:nth-of-type(1)');
    const nextArrow = document.querySelector('.testimonial-arrow:nth-of-type(2)');

    if (prevArrow && testimonialSlides.length > 0) {
        prevArrow.addEventListener('click', function() {
            clearInterval(testimonialAutoScrollInterval);
            showTestimonialSlide(currentSlide - 1);
            startTestimonialAutoScroll();
        });
    }

    if (nextArrow && testimonialSlides.length > 0) {
        nextArrow.addEventListener('click', function() {
            clearInterval(testimonialAutoScrollInterval);
            showTestimonialSlide(currentSlide + 1);
            startTestimonialAutoScroll();
        });
    }

    // Add click handlers to dots
    testimonialDots.forEach((dot, index) => {
        dot.addEventListener('click', function() {
            clearInterval(testimonialAutoScrollInterval);
            showTestimonialSlide(index);
            startTestimonialAutoScroll();
        });
    });

    // Start auto-scroll
    function startTestimonialAutoScroll() {
        if (testimonialSlides.length > 1) {
            testimonialAutoScrollInterval = setInterval(autoScrollTestimonials, 6000);
        }
    }

    // Initialize testimonials
    if (testimonialSlides.length > 0) {
        showTestimonialSlide(0);
        startTestimonialAutoScroll();
    }

    // ================================================================= //
    // 3. AUTO-ROTATE PARTNERS SECTION
    // ================================================================= //
    function setupPartnerAutoScroll() {
        const partnerGrid = document.querySelector('.partner-grid');
        if (!partnerGrid) return;

        const cards = Array.from(partnerGrid.querySelectorAll('.partner-card:not([data-partner-clone])'));
        if (!cards.length || partnerGrid.dataset.loopReady === 'true') return;

        cards.forEach(card => {
            const clone = card.cloneNode(true);
            clone.dataset.partnerClone = 'true';
            clone.setAttribute('aria-hidden', 'true');
            partnerGrid.appendChild(clone);
        });

        partnerGrid.dataset.loopReady = 'true';
    }

    setupPartnerAutoScroll();

    function setupFeaturedProjectAutoRotate() {
        const viewport = document.querySelector('.featured-projects .project-grid');
        const track = viewport?.querySelector('.project-track');
        if (!viewport || !track || track.dataset.autoRotateReady === 'true') return;

        const cards = track.querySelectorAll('.project-card');
        if (cards.length < 2 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        track.dataset.autoRotateReady = 'true';
        let rotationTimer;

        function scheduleRotation() {
            clearTimeout(rotationTimer);
            rotationTimer = setTimeout(() => {
                const firstCard = track.querySelector('.project-card');
                if (!firstCard) return;

                const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
                track.style.transition = 'transform 0.6s ease-in-out';
                track.style.transform = `translateX(-${firstCard.getBoundingClientRect().width + gap}px)`;

                track.addEventListener('transitionend', function handleRotation() {
                    track.removeEventListener('transitionend', handleRotation);
                    track.style.transition = 'none';
                    track.style.transform = 'translateX(0)';
                    track.appendChild(firstCard);
                    track.offsetHeight;
                    track.style.transition = '';
                    if (!viewport.matches(':hover')) scheduleRotation();
                }, { once: true });
            }, 3500);
        }

        viewport.addEventListener('mouseenter', () => clearTimeout(rotationTimer));
        viewport.addEventListener('mouseleave', scheduleRotation);
        scheduleRotation();
    }

    setupFeaturedProjectAutoRotate();

    // ================================================================= //
    // 4. FAQ ACCORDION TOGGLE
    // ================================================================= //
    const faqToggles = document.querySelectorAll('.faq-toggle');
    
    faqToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const faqItem = this.closest('.faq-item');
            const icon = faqItem.querySelector('.faq-icon');
            
            if (this.checked) {
                // Open animation
                icon.style.transform = 'rotate(45deg)';
            } else {
                // Close animation
                icon.style.transform = 'rotate(0deg)';
            }
        });
    });

    document.addEventListener('click', function(event) {
        if (event.target.closest('.faq-item')) return;

        faqToggles.forEach(toggle => {
            if (toggle.checked) {
                toggle.checked = false;
                toggle.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    });

    // ================================================================= //
    // 5. PROPERTY CARD POPUP/MODAL
    // ================================================================= //
    const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
    const modalOverlay = document.querySelector('.modal-overlay');
    const modalClose = document.querySelector('.modal-close');

    viewDetailsButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (modalOverlay) {
                modalOverlay.style.display = 'flex';
            }
        });
    });

    if (modalClose && modalOverlay) {
        modalClose.addEventListener('click', function() {
            modalOverlay.style.display = 'none';
        });

        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                modalOverlay.style.display = 'none';
            }
        });
    }

    // ================================================================= //
    // 6. FLOATING ENQUIRY BUTTON
    // ================================================================= //
    const floatingBtn = document.querySelector('.floating-enquiry-btn');
    const enquiryModal = document.querySelector('.enquiry-modal-overlay');
    const enquiryCloseBtn = document.querySelector('.modal-close-btn');

    if (floatingBtn && enquiryModal) {
        floatingBtn.addEventListener('click', function() {
            enquiryModal.classList.add('active');
        });
    }

    if (enquiryCloseBtn && enquiryModal) {
        enquiryCloseBtn.addEventListener('click', function() {
            enquiryModal.classList.remove('active');
        });

        enquiryModal.addEventListener('click', function(e) {
            if (e.target === enquiryModal) {
                enquiryModal.classList.remove('active');
            }
        });
    }

    // ================================================================= //
    // 7. IMAGE MODAL FOR BLOGS
    // ================================================================= //
    const blogImages = document.querySelectorAll('.clickable-blog-img, .blog-card img');
    const imageModal = document.querySelector('.image-modal');
    const modalBlogImg = document.querySelector('#modalBlogImg');
    const modalBlogTitle = document.querySelector('#modalBlogTitle');
    const modalBlogDate = document.querySelector('#modalBlogDate');
    const modalBlogContent = document.querySelector('#modalBlogContent');
    const closeModalBtn = document.querySelector('.image-modal .modal-close-btn');

    blogImages.forEach(img => {
        img.addEventListener('click', function() {
            if (imageModal && modalBlogImg) {
                const card = this.closest('.blog-card');
                if (card) {
                    const title = card.querySelector('.blog-content-box h3')?.textContent || 'Blog Post';
                    const date = card.querySelector('.blog-date')?.textContent || '';
                    const excerpt = card.querySelector('.blog-excerpt')?.textContent || '';
                    
                    modalBlogImg.src = this.src;
                    if (modalBlogTitle) modalBlogTitle.textContent = title;
                    if (modalBlogDate) modalBlogDate.textContent = date;
                    if (modalBlogContent) modalBlogContent.textContent = excerpt;
                    
                    imageModal.style.display = 'block';
                }
            }
        });
    });

    if (closeModalBtn && imageModal) {
        closeModalBtn.addEventListener('click', function() {
            imageModal.style.display = 'none';
        });

        imageModal.addEventListener('click', function(e) {
            if (e.target === imageModal) {
                imageModal.style.display = 'none';
            }
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (imageModal) imageModal.style.display = 'none';
            if (enquiryModal) enquiryModal.classList.remove('active');
            if (modalOverlay) modalOverlay.style.display = 'none';
        }
    });

    // ================================================================= //
    // 8. FORM SUBMISSION HANDLERS
    // ================================================================= //
     const enquiryForm = document.querySelector('.enquiry-modal-form');
    
     if (enquiryForm) {
         enquiryForm.addEventListener('submit', function(e) {
             e.preventDefault();
            
             // Show success message
            const successToast = document.querySelector('.login-success-toast');
             if (successToast) {
                 successToast.textContent = 'Enquiry submitted successfully!';
                 successToast.style.display = 'block';
                
                 setTimeout(() => {
                     successToast.style.display = 'none';
                 }, 3000);
             }

             // Close modal
             if (enquiryModal) {
                 enquiryModal.classList.remove('active');
             }

             // Reset form
             this.reset();
         });
     }

    // ================================================================= //
    // 9. SMOOTH SCROLL BEHAVIOR
    // ================================================================= //
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ================================================================= //
    // 10. PROPERTY CATEGORY CLICK HANDLER
    // ================================================================= //
    const categoryCards = document.querySelectorAll('.property-category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const categoryName = this.querySelector('h4')?.textContent || 'Properties';
            console.log('Selected category:', categoryName);
            // You can add navigation or filter logic here
        });
    });

    // ================================================================= //
    // 11. LAZY LOADING IMAGES (Performance)
    // ================================================================= //
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

});





/* Responsive header menu and touch dropdowns. */
function initializeResponsiveHeader() {
  var header = document.querySelector('.header');
  var burger = document.querySelector('.hamburger-menu');
  var navLinks = document.querySelector('.nav-links');
  if (!header || !burger || !navLinks) return;

  var mq = window.matchMedia('(max-width: 1230px)');

  function setMenu(open) {
    header.classList.toggle('menu-open', open);
    burger.classList.toggle('active', open);
    navLinks.classList.toggle('active', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    if (!open) closeDropdowns();
  }

  function closeDropdowns(except) {
    document.querySelectorAll('.dropdown.open, .login-dropdown.open').forEach(function (el) {
      if (el !== except) {
        el.classList.remove('open');
        var t = el.querySelector(':scope > .dropdown-toggle, :scope > .login-dropdown-btn');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
  }

  burger.addEventListener('click', function () {
    setMenu(!header.classList.contains('menu-open'));
  });

  document.addEventListener('click', function (e) {
    // Dropdown trigger: Properties (sirf mobile/tablet par) aur Login/User (har jagah)
    var trigger = e.target.closest('.dropdown-toggle, .login-dropdown > .login-dropdown-btn');
    if (trigger) {
      var isLogin = trigger.classList.contains('login-dropdown-btn');
      if (isLogin || mq.matches) {
        e.preventDefault();
        var parent = trigger.parentElement;
        var willOpen = !parent.classList.contains('open');
        closeDropdowns(parent);
        parent.classList.toggle('open', willOpen);
        trigger.setAttribute('aria-expanded', String(willOpen));
        return;
      }
    }

    // Bahar tap -> dropdowns band
    if (!e.target.closest('.dropdown, .login-dropdown')) closeDropdowns();

    // Menu ke andar kisi link/button par tap -> menu band (navigation ya modal ke liye)
    if (mq.matches && header.classList.contains('menu-open')) {
      var outside = !e.target.closest('.header');
      var picked = e.target.closest('.nav-links a, .header-actions > a, .login-dropdown-content a');
      if (outside || picked) setMenu(false);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMenu(false);
      burger.focus();
    }
  });

  // Desktop width par aate hi mobile state reset
  var onChange = function () { if (!mq.matches) setMenu(false); };
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else mq.addListener(onChange);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeResponsiveHeader, { once: true });
} else {
  initializeResponsiveHeader();
}