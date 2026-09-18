
document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // API & ELEMENTS
    // ==========================================

    const API_URL = "/api/resumes/profile/";

    const saveButton =
        document.getElementById("saveProfileButton");

    const saveButtonText =
        document.getElementById("saveButtonText");

    const messageBox =
        document.getElementById("messageBox");

    const completionPercentage =
        document.getElementById("completionPercentage");

    const addEducationBtn =
        document.getElementById("addEducationBtn");

    const educationContainer =
        document.getElementById("educationContainer");


    // ==========================================
    // PERSONAL INFORMATION FIELDS
    // ==========================================

    const profileFields = [
        "full_name",
        "email",
        "phone",
        "location",
        "linkedin",
        "github",
        "portfolio",
        "summary"
    ];


    // ==========================================
    // GET JWT ACCESS TOKEN
    // ==========================================

    function getAccessToken() {

        return localStorage.getItem("access_token");

    }


    // ==========================================
    // DISPLAY MESSAGE
    // ==========================================

    function showMessage(message, type) {

        if (!messageBox) {
            return;
        }

        messageBox.innerText = message;

        messageBox.className =
            `alert alert-${type}`;

        messageBox.classList.remove("d-none");

        messageBox.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    }


    // ==========================================
    // CALCULATE PROFILE COMPLETION
    // ==========================================

    function calculateCompletion() {

        if (!completionPercentage) {
            return;
        }

        let completed = 0;

        profileFields.forEach(function (fieldId) {

            const element =
                document.getElementById(fieldId);

            if (
                element &&
                element.value.trim() !== ""
            ) {
                completed++;
            }

        });

        const percentage =
            Math.round(
                (completed / profileFields.length) * 100
            );

        completionPercentage.innerText =
            `${percentage}%`;

    }


    // ==========================================
    // ADD EDUCATION CARD
    // ==========================================

    function addEducationCard(education = {}) {

        if (!educationContainer) {
            return;
        }

        const card =
            document.createElement("div");

        card.className =
            "education-card";

        card.innerHTML = `
            <div class="education-card-header">

                <h3>Education</h3>

                <button
                    type="button"
                    class="remove-education-btn"
                >
                    Remove
                </button>

            </div>

            <div class="education-grid">

                <div class="education-field">

                    <label>Degree</label>

                    <input
                        type="text"
                        class="education-degree"
                        placeholder="e.g. BMM"
                        value="${education.degree || ""}"
                    >

                </div>


                <div class="education-field">

                    <label>Institution</label>

                    <input
                        type="text"
                        class="education-institution"
                        placeholder="e.g. Vidyalankar School of Information Technology"
                        value="${education.institution || ""}"
                    >

                </div>


                <div class="education-field">

                    <label>Start Year</label>

                    <input
                        type="number"
                        class="education-start-year"
                        placeholder="e.g. 2024"
                        value="${education.start_year || ""}"
                    >

                </div>


                <div class="education-field">

                    <label>End Year</label>

                    <input
                        type="number"
                        class="education-end-year"
                        placeholder="e.g. 2027"
                        value="${education.end_year || ""}"
                    >

                </div>


                <div class="education-field">

                    <label>Percentage / CGPA</label>

                    <input
                        type="text"
                        class="education-percentage"
                        placeholder="e.g. 8.5 CGPA"
                        value="${education.percentage || ""}"
                    >

                </div>

            </div>
        `;


        // ==========================================
        // REMOVE EDUCATION
        // ==========================================

        const removeButton =
            card.querySelector(
                ".remove-education-btn"
            );

        if (removeButton) {

            removeButton.addEventListener(
                "click",
                function () {

                    card.remove();

                    updateEducationEmptyState();

                }
            );

        }


        // Add card to container

        educationContainer.appendChild(card);

        updateEducationEmptyState();

    }


    // ==========================================
    // ADD EDUCATION BUTTON
    // ==========================================

    if (addEducationBtn) {

        addEducationBtn.addEventListener(
            "click",
            function () {

                addEducationCard();

            }
        );

    }


    // ==========================================
    // GET EDUCATION DATA
    // ==========================================

    function getEducationData() {

        if (!educationContainer) {
            return [];
        }

        const cards =
            educationContainer.querySelectorAll(
                ".education-card"
            );

        const education = [];


        cards.forEach(function (card) {

            const degree =
                card.querySelector(
                    ".education-degree"
                ).value.trim();


            const institution =
                card.querySelector(
                    ".education-institution"
                ).value.trim();


            const startYear =
                card.querySelector(
                    ".education-start-year"
                ).value;


            const endYear =
                card.querySelector(
                    ".education-end-year"
                ).value;


            const percentage =
                card.querySelector(
                    ".education-percentage"
                ).value.trim();


            // Ignore completely empty cards

            if (
                !degree &&
                !institution &&
                !startYear &&
                !endYear &&
                !percentage
            ) {
                return;
            }


            education.push({

                degree: degree,

                institution: institution,

                start_year:
                    startYear
                        ? parseInt(startYear)
                        : null,

                end_year:
                    endYear
                        ? parseInt(endYear)
                        : null,

                percentage: percentage

            });

        });


        return education;

    }


    // ==========================================
    // LOAD EDUCATION
    // ==========================================

    function loadEducation(education) {

        if (!educationContainer) {
            return;
        }

        educationContainer.innerHTML = "";


        if (
            !education ||
            education.length === 0
        ) {

            updateEducationEmptyState();

            return;

        }


        education.forEach(function (item) {

            addEducationCard(item);

        });

    }


    // ==========================================
    // EDUCATION EMPTY STATE
    // ==========================================

    function updateEducationEmptyState() {

        if (!educationContainer) {
            return;
        }

        const cards =
            educationContainer.querySelectorAll(
                ".education-card"
            );


        const existingMessage =
            educationContainer.querySelector(
                ".education-empty"
            );


        if (cards.length === 0) {

            if (!existingMessage) {

                const message =
                    document.createElement("div");

                message.className =
                    "education-empty";

                message.innerText =
                    "No education details added yet.";

                educationContainer.appendChild(
                    message
                );

            }

        } else {

            if (existingMessage) {

                existingMessage.remove();

            }

        }

    }


    // ==========================================
    // LOAD EXISTING PROFILE
    // ==========================================

    async function loadProfile() {

        const token =
            getAccessToken();


        if (!token) {

            window.location.href =
                "/login/";

            return;

        }


        try {

            const response =
                await fetch(
                    API_URL,
                    {
                        method: "GET",

                        headers: {
                            "Authorization":
                                `Bearer ${token}`
                        }
                    }
                );


            // ==========================================
            // PROFILE DOES NOT EXIST
            // ==========================================

            if (response.status === 404) {

                try {

                    const storedUser =
                        localStorage.getItem("user");


                    if (storedUser) {

                        const user =
                            JSON.parse(
                                storedUser
                            );


                        if (user.username) {

                            const nameElement =
                                document.getElementById(
                                    "full_name"
                                );

                            if (
                                nameElement &&
                                !nameElement.value
                            ) {

                                nameElement.value =
                                    user.username;

                            }

                        }


                        if (user.email) {

                            const emailElement =
                                document.getElementById(
                                    "email"
                                );

                            if (
                                emailElement &&
                                !emailElement.value
                            ) {

                                emailElement.value =
                                    user.email;

                            }

                        }

                    }

                } catch (error) {

                    console.warn(
                        "Could not prefill user:",
                        error
                    );

                }


                updateEducationEmptyState();

                calculateCompletion();

                return;

            }


            const data =
                await response.json();


            if (!response.ok) {

                showMessage(
                    data.error ||
                    data.message ||
                    "Unable to load profile.",
                    "danger"
                );

                return;

            }


            // ==========================================
            // POPULATE PERSONAL INFORMATION
            // ==========================================

            profileFields.forEach(
                function (fieldId) {

                    const element =
                        document.getElementById(
                            fieldId
                        );


                    if (
                        element &&
                        data[fieldId] !== undefined &&
                        data[fieldId] !== null
                    ) {

                        element.value =
                            data[fieldId];

                    }

                }
            );


            // ==========================================
            // LOAD EDUCATION
            // ==========================================

            loadEducation(
                data.education || []
            );


            calculateCompletion();

        } catch (error) {

            console.error(
                "Profile Load Error:",
                error
            );

            showMessage(
                "Unable to connect to the server.",
                "danger"
            );

        }

    }


    // ==========================================
    // SAVE / UPDATE PROFILE
    // ==========================================

    async function saveProfile() {

        const token =
            getAccessToken();


        if (!token) {

            window.location.href =
                "/login/";

            return;

        }


        // ==========================================
        // PERSONAL INFORMATION
        // ==========================================

        const profileData = {};


        profileFields.forEach(
            function (fieldId) {

                const element =
                    document.getElementById(
                        fieldId
                    );

                profileData[fieldId] =
                    element
                        ? element.value.trim()
                        : "";

            }
        );


        // ==========================================
        // EDUCATION
        // ==========================================

        profileData.education =
            getEducationData();


        // ==========================================
        // OTHER SECTIONS
        // ==========================================

        profileData.experience = [];

        profileData.projects = [];

        profileData.skills = [];

        profileData.certifications = [];

        profileData.achievements = [];

        profileData.languages = [];


        // ==========================================
        // BASIC VALIDATION
        // ==========================================

        if (!profileData.full_name) {

            showMessage(
                "Full Name is required.",
                "danger"
            );

            return;

        }


        if (!profileData.email) {

            showMessage(
                "Email is required.",
                "danger"
            );

            return;

        }


        // ==========================================
        // DISABLE SAVE BUTTON
        // ==========================================

        if (saveButton) {

            saveButton.disabled = true;

        }


        if (saveButtonText) {

            saveButtonText.innerText =
                "Saving...";

        }


        try {

            // ==========================================
            // CHECK EXISTING PROFILE
            // ==========================================

            const checkResponse =
                await fetch(
                    API_URL,
                    {
                        method: "GET",

                        headers: {
                            "Authorization":
                                `Bearer ${token}`
                        }
                    }
                );


            const method =
                checkResponse.status === 404
                    ? "POST"
                    : "PUT";


            // ==========================================
            // SAVE PROFILE
            // ==========================================

            const response =
                await fetch(
                    API_URL,
                    {
                        method: method,

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Authorization":
                                `Bearer ${token}`
                        },

                        body:
                            JSON.stringify(
                                profileData
                            )
                    }
                );


            const data =
                await response.json();


            if (response.ok) {

                showMessage(
                    "Profile saved successfully!",
                    "success"
                );


                // Reload education from server

                if (data.education) {

                    loadEducation(
                        data.education
                    );

                }


                calculateCompletion();

            } else {

                console.error(
                    "Save Profile Error:",
                    data
                );


                let errorMessage =
                    "Unable to save profile.";


                if (data.error) {

                    errorMessage =
                        data.error;

                } else if (
                    typeof data === "object"
                ) {

                    errorMessage =
                        Object.values(data)
                            .flat()
                            .join(" ");

                }


                showMessage(
                    errorMessage,
                    "danger"
                );

            }

        } catch (error) {

            console.error(
                "Save Profile Connection Error:",
                error
            );


            showMessage(
                "Unable to connect to the server.",
                "danger"
            );

        } finally {

            if (saveButton) {

                saveButton.disabled = false;

            }


            if (saveButtonText) {

                saveButtonText.innerText =
                    "Save Profile";

            }

        }

    }


    // ==========================================
    // SAVE BUTTON EVENT
    // ==========================================

    if (saveButton) {

        saveButton.addEventListener(
            "click",
            saveProfile
        );

    }


    // ==========================================
    // PROFILE INPUT EVENTS
    // ==========================================

    document
        .querySelectorAll(".profile-input")
        .forEach(
            function (input) {

                input.addEventListener(
                    "input",
                    calculateCompletion
                );

            }
        );


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    loadProfile();

    calculateCompletion();

    updateEducationEmptyState();

});

