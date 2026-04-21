// Authentication JavaScript - Login and Signup

// Show error messages
function showError(container, errors) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    
    if (Array.isArray(errors)) {
        const ul = document.createElement('ul');
        ul.className = 'error-list';
        errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            ul.appendChild(li);
        });
        errorDiv.appendChild(ul);
    } else {
        errorDiv.textContent = errors;
    }
    
    container.innerHTML = '';
    container.appendChild(errorDiv);
}

// Show success message
function showSuccess(container, message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    container.innerHTML = '';
    container.appendChild(successDiv);
}

// Clear messages
function clearMessages(container) {
    container.innerHTML = '';
}

// Login Form Handler
if (document.getElementById('loginForm')) {
    const loginForm = document.getElementById('loginForm');
    const errorContainer = document.getElementById('errorContainer');
    const loginBtn = document.getElementById('loginBtn');
    const loginBtnText = document.getElementById('loginBtnText');
    const loginBtnLoading = document.getElementById('loginBtnLoading');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearMessages(errorContainer);

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        // Show loading
        loginBtnText.classList.add('hidden');
        loginBtnLoading.classList.remove('hidden');
        loginBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to dashboard
                window.location.href = 'dashboard.html';
            } else {
                showError(errorContainer, data.error || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError(errorContainer, 'Network error. Please try again.');
        } finally {
            // Hide loading
            loginBtnText.classList.remove('hidden');
            loginBtnLoading.classList.add('hidden');
            loginBtn.disabled = false;
        }
    });
}

// Signup Form Handler
if (document.getElementById('signupForm')) {
    const signupForm = document.getElementById('signupForm');
    const errorContainer = document.getElementById('errorContainer');
    const successContainer = document.getElementById('successContainer');
    const signupBtn = document.getElementById('signupBtn');
    const signupBtnText = document.getElementById('signupBtnText');
    const signupBtnLoading = document.getElementById('signupBtnLoading');

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearMessages(errorContainer);
        clearMessages(successContainer);

        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // Show loading
        signupBtnText.classList.add('hidden');
        signupBtnLoading.classList.remove('hidden');
        signupBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    full_name: fullName,
                    email,
                    password,
                    confirm_password: confirmPassword
                })
            });

            const data = await response.json();

            if (data.success) {
                showSuccess(successContainer, 'Account created successfully! Redirecting to login...');
                signupForm.reset();
                
                // Redirect to login after 2 seconds
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            } else {
                showError(errorContainer, data.errors || ['Registration failed']);
            }
        } catch (error) {
            console.error('Signup error:', error);
            showError(errorContainer, ['Network error. Please try again.']);
        } finally {
            // Hide loading
            signupBtnText.classList.remove('hidden');
            signupBtnLoading.classList.add('hidden');
            signupBtn.disabled = false;
        }
    });
}
