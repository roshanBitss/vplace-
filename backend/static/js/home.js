document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       USER AUTH & PERSONALIZATION
    ========================= */
    try {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            const user = JSON.parse(storedUser);
            const heroGreeting = document.getElementById("heroGreeting");
            if (heroGreeting && (user.username || user.name)) {
                const displayName = user.name || user.username;
                heroGreeting.innerHTML = `Hello, <span>${escapeHtml(displayName)}</span>`;
            }
        }
    } catch (e) {
        console.warn("Could not load user profile from localStorage:", e);
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    /* =========================
       LOGOUT CONFIRMATION & CLEANUP
    ========================= */
    const logoutLink = document.getElementById("logoutLink");
    if (logoutLink) {
        logoutLink.addEventListener("click", function (event) {
            const confirmed = confirm("Are you sure you want to logout?");
            if (!confirmed) {
                event.preventDefault();
            } else {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                localStorage.removeItem("user");
            }
        });
    }

    /* =========================
       SCROLL REVEAL ANIMATION
    ========================= */
    const revealElements = document.querySelectorAll(".reveal-section");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px"
            }
        );

        revealElements.forEach(function (element) {
            observer.observe(element);
        });
    } else {
        revealElements.forEach(function (element) {
            element.classList.add("visible");
        });
    }

    /* =========================
       STAT & HIGHLIGHT NUMBER COUNTER
    ========================= */
    const counters = document.querySelectorAll(".count-up[data-target]");

    if ("IntersectionObserver" in window) {
        const counterObserver = new IntersectionObserver(
            function (entries, obs) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.2 }
        );

        counters.forEach(function (counter) {
            counterObserver.observe(counter);
        });
    } else {
        counters.forEach(function (counter) {
            animateCounter(counter);
        });
    }

    function animateCounter(counter) {
        const target = parseFloat(counter.getAttribute("data-target"));
        const prefix = counter.getAttribute("data-prefix") || "";
        const suffix = counter.getAttribute("data-suffix") || "";
        const decimals = parseInt(counter.getAttribute("data-decimals") || "0", 10);

        if (isNaN(target)) return;

        let current = 0;
        const duration = 1600;
        const steps = 50;
        const stepTime = duration / steps;
        const increment = target / steps;

        const timer = setInterval(function () {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            const displayVal = decimals > 0 ? current.toFixed(decimals) : Math.floor(current);
            counter.innerText = prefix + displayVal + suffix;
        }, stepTime);
    }

    /* =========================
       NAVBAR SCROLL EFFECT
    ========================= */
    const navbar = document.querySelector(".vplace-navbar");
    if (navbar) {
        function checkScroll() {
            if (window.scrollY > 30) {
                navbar.classList.add("navbar-scrolled");
            } else {
                navbar.classList.remove("navbar-scrolled");
            }
        }
        window.addEventListener("scroll", checkScroll, { passive: true });
        checkScroll();
    }

    /* =========================
       PLACEMENT CHARTS (CANVASJS)
    ========================= */
    function initCharts() {
        if (typeof CanvasJS === "undefined") {
            console.warn("CanvasJS library not loaded. Retrying in 500ms...");
            setTimeout(initCharts, 500);
            return;
        }

        // Package per Year Chart
        const chartFruitsContainer = document.getElementById("chartContainerFruits");
        if (chartFruitsContainer) {
            const defaultPackageData = [
                { label: "2020", y: 4.8, color: "#e57373" },
                { label: "2021", y: 5.5, color: "#ef5350" },
                { label: "2022", y: 6.8, color: "#e53935" },
                { label: "2023", y: 8.2, color: "#d32f2f" },
                { label: "2024", y: 9.6, color: "#dc1f26" }
            ];

            const packageData = (window.fruitsData && window.fruitsData.length > 0)
                ? window.fruitsData
                : defaultPackageData;

            const chartPackage = new CanvasJS.Chart("chartContainerFruits", {
                animationEnabled: true,
                theme: "light2",
                axisY: {
                    title: "Package (in LPA)",
                    suffix: " L",
                    includeZero: true,
                    gridColor: "#f0f0f0"
                },
                axisX: {
                    title: "Year",
                    gridColor: "transparent"
                },
                toolTip: {
                    shared: false,
                    content: "<strong>{label}</strong>: ₹{y} Lakhs/annum"
                },
                data: [
                    {
                        type: "column",
                        yValueFormatString: "₹#,##0.00'L'",
                        dataPoints: packageData
                    }
                ]
            });
            chartPackage.render();
        }

        // Department Placement Chart
        const chartSalesContainer = document.getElementById("chartContainerSales");
        if (chartSalesContainer) {
            const defaultDeptData = [
                { label: "B.Sc IT", y: 35, color: "#dc1f26" },
                { label: "B.Sc CS", y: 28, color: "#b51219" },
                { label: "BMS", y: 18, color: "#f87171" },
                { label: "BAF", y: 14, color: "#fb7185" },
                { label: "BBI", y: 10, color: "#fda4af" },
                { label: "BFM", y: 8, color: "#fecdd3" }
            ];

            const deptData = (window.salesData && window.salesData.length > 0)
                ? window.salesData
                : defaultDeptData;

            const chartDept = new CanvasJS.Chart("chartContainerSales", {
                animationEnabled: true,
                theme: "light2",
                toolTip: {
                    content: "<strong>{label}</strong>: {y} Placements (#percent%)"
                },
                data: [
                    {
                        type: "doughnut",
                        showInLegend: true,
                        legendText: "{label}",
                        indexLabel: "{label}: {y}",
                        indexLabelFontSize: 11,
                        dataPoints: deptData
                    }
                ]
            });
            chartDept.render();
        }
    }

    // Initialize charts once DOM is ready or after brief delay
    if (document.getElementById("chartContainerFruits") || document.getElementById("chartContainerSales")) {
        initCharts();
    }
});