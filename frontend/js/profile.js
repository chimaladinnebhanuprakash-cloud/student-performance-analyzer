// Profile Page JavaScript

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProfile);
} else {
    initProfile();
}

function initProfile() {
    // Check if elements exist (page might not be loaded yet)
    const profileForm = document.getElementById('profileForm');
    if (!profileForm) {
        // Retry after a short delay
        setTimeout(initProfile, 100);
        return;
    }

    const profileMessage = document.getElementById('profileMessage');
    const saveProfileBtn = document.getElementById('saveProfileBtn');
    const saveProfileText = document.getElementById('saveProfileText');
    const saveProfileLoading = document.getElementById('saveProfileLoading');

    // Load profile data
    loadProfileData();

    // Save profile form handler
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        profileMessage.innerHTML = '';

        const age = document.getElementById('age').value;
        const gender = document.getElementById('gender').value;
        const course = document.getElementById('course').value;
        const semester = document.getElementById('semester').value;
        const college = document.getElementById('college').value;

        // Show loading
        saveProfileText.classList.add('hidden');
        saveProfileLoading.classList.remove('hidden');
        saveProfileBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    age: age ? parseInt(age) : null,
                    gender,
                    course,
                    semester,
                    college
                })
            });

            const data = await response.json();

            if (data.success) {
                profileMessage.innerHTML = '<div class="success-message">Profile updated successfully!</div>';
            } else {
                profileMessage.innerHTML = `<div class="error-message">${data.error || 'Failed to update profile'}</div>`;
            }
        } catch (error) {
            console.error('Error saving profile:', error);
            profileMessage.innerHTML = '<div class="error-message">Network error. Please try again.</div>';
        } finally {
            // Hide loading
            saveProfileText.classList.remove('hidden');
            saveProfileLoading.classList.add('hidden');
            saveProfileBtn.disabled = false;
        }
    });
}

// Load profile data
async function loadProfileData() {
    try {
        const response = await fetch(`${API_BASE}/profile`, {
            credentials: 'include'
        });
        const data = await response.json();

        if (data.success) {
            // Set user data (read-only)
            const profileName = document.getElementById('profileName');
            const profileEmail = document.getElementById('profileEmail');

            if (profileName) profileName.value = data.user.full_name;
            if (profileEmail) profileEmail.value = data.user.email;

            // Set profile data if exists
            if (data.profile) {
                const ageInput = document.getElementById('age');
                const genderInput = document.getElementById('gender');
                const courseInput = document.getElementById('course');
                const semesterInput = document.getElementById('semester');
                const collegeInput = document.getElementById('college');

                if (data.profile.age && ageInput) {
                    ageInput.value = data.profile.age;
                }
                if (data.profile.gender && genderInput) {
                    genderInput.value = data.profile.gender;
                }
                if (data.profile.course && courseInput) {
                    courseInput.value = data.profile.course;
                }
                if (data.profile.semester && semesterInput) {
                    semesterInput.value = data.profile.semester;
                }
                if (data.profile.college && collegeInput) {
                    collegeInput.value = data.profile.college;
                }
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}
