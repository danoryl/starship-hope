/* FORM HANDLING */

function handleFormSubmission(formId, messageId, url) {
    const form = document.getElementById(formId);
    event.preventDefault(); // Prevent default form submission
    
    const formData = new FormData(form);
    
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.redirect) {
            window.location.href = data.redirect;
        } else {
        const flashMessage = document.getElementById(messageId);  
        flashMessage.innerHTML = "";
        // Loop through the error messages and display them
        if (Array.isArray(data.message)) {
            const errorList = document.createElement("ul");
            data.message.forEach(errorMessage => {
                const listItem = document.createElement("li");
                listItem.textContent = errorMessage;
                errorList.appendChild(listItem);
            });
            flashMessage.appendChild(errorList);
        } else {
            flashMessage.textContent = data.message;
        }  
        
        // Add a class based on data.success
        flashMessage.classList.remove('alert-success', 'alert-error');
        if (data.success) {
             flashMessage.classList.add('alert-success');
        } else {
             flashMessage.classList.add('alert-error');
         }
        }
          
    })
    .catch(error => {
        console.error('Error:', error);
    });
   
}

/* NAVBAR */

document.addEventListener("DOMContentLoaded", function () {
    

    // Smooth scrolling on the navbar links
    var navbarLinks = document.querySelectorAll(".navbar-nav a");
    navbarLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            if (this.hash !== "") {
                event.preventDefault();
                var targetElement = document.querySelector(this.hash);
                var targetOffset = targetElement.getBoundingClientRect().top + window.scrollY;
                var scrollOptions = {
                    top: targetOffset - 110,
                    behavior: 'smooth',
                };
                window.scrollTo(scrollOptions);

                
            }
        });
    });
});