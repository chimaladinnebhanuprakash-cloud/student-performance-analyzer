// Dashboard JavaScript - Navigation and Session Management

let currentUser = null;

// Check session on load
async function checkSession() {
    try {
        const response = await fetch(`${API_BASE}/check-session`, {
            credentials: 'include'
        });
        const data = await response.json();

        if (!data.logged_in) {
            // Redirect to login
            window.location.href = 'index.html';
            return false;
        }

        currentUser = data.user;
        updateProfileButton();
        return true;
    } catch (error) {
        console.error('Session check error:', error);
        window.location.href = 'index.html';
        return false;
    }
}

// Update profile button with user initial
function updateProfileButton() {
    if (currentUser && currentUser.full_name) {
        const initial = currentUser.full_name.charAt(0).toUpperCase();
        document.getElementById('profileInitial').textContent = initial;
    }
}

// Load page content
async function loadPage(pageName) {
    try {
        const response = await fetch(`${pageName}.html`);
        const html = await response.text();
        document.getElementById('pageContent').innerHTML = html;

        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.page === pageName) {
                tab.classList.add('active');
            }
        });

        // Load the corresponding JavaScript file
        loadPageScript(pageName);
    } catch (error) {
        console.error('Error loading page:', error);
        document.getElementById('pageContent').innerHTML = '<p>Error loading page</p>';
    }
}

// Load page-specific JavaScript
function loadPageScript(pageName) {
    // Remove any existing page script
    const existingScript = document.getElementById('pageScript');
    if (existingScript) {
        existingScript.remove();
    }

    // Create and load new script
    const script = document.createElement('script');
    script.id = 'pageScript';
    script.src = `js/${pageName}.js?t=${Date.now()}`; // Add timestamp to prevent caching
    script.onload = function () {
        console.log(`Loaded ${pageName}.js successfully`);
    };
    script.onerror = function () {
        console.error(`Failed to load ${pageName}.js`);
    };
    document.body.appendChild(script);
}

// Navigate to page (can be called from loaded pages)
function navigateToPage(pageName) {
    loadPage(pageName);
}

// Tab click handlers
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const pageName = tab.dataset.page;
        loadPage(pageName);
    });
});

// Profile dropdown toggle
const profileBtn = document.getElementById('profileBtn');
const profileDropdown = document.getElementById('profileDropdown');

profileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    profileDropdown.classList.toggle('show');
});

// Close dropdown when clicking outside
document.addEventListener('click', () => {
    profileDropdown.classList.remove('show');
});

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', async () => {
    try {
        await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = 'index.html';
    }
});

// Initialize dashboard
async function initDashboard() {
    const sessionValid = await checkSession();
    if (sessionValid) {
        // Load home page by default
        loadPage('home');
    }
}

// Run on page load
initDashboard();
