frappe.ready(function() {
    // Wait for login form to be available
    const interval = setInterval(() => {
        const loginForm = document.querySelector(".login-content .page-card-actions");
        if (loginForm && !document.querySelector("#whatsapp-login-btn")) {
            clearInterval(interval);

            // Create the button
            let btn = document.createElement("a");
            btn.id = "whatsapp-login-btn";
            btn.className = "btn btn-sm btn-primary btn-block mt-3";
            btn.href = "/whatsapp_login.html";
            btn.innerText = "Login with WhatsApp";
            btn.className = "btn btn-lg btn-block btn-primary mt-3";
            btn.style.backgroundColor = "#25D366";  // WhatsApp green
            btn.style.border = "none";
            btn.style.color = "#fff";
            btn.innerHTML = `
                <img src="/assets/frappe_whatspp_login/img/whatsapp-logo.png" 
                     alt="WhatsApp" 
                     style="height:24px; margin-right:8px;">
                Login with WhatsApp
            `;

            // Append after the existing login buttons
            loginForm.appendChild(btn);
        }
    }, 300);
});
