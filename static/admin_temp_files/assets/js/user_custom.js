
document.addEventListener("htmx:beforeRequest", function(event) {
    // event from htmx which is invoked before form requests

    // Get the form element that is triggering the request
    let form = event.target.closest('form');
    
    // If a form was found, proceed to disable the submit button and input fields
    if (form) {
        // Disable all input fields within the form
        let inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.setAttribute('disabled', 'disabled');
        });
        
        // Disable all submit buttons within the form
        let submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
        submitButtons.forEach(function(button) {
            button.setAttribute('disabled', 'disabled');
            button.innerText = "Submitting...";
        });
    }
});



document.addEventListener("htmx:afterRequest", function(evt) {
    // event from htmx which is invoked after form requests
  
      // Get the form element that is triggering the request
      let form = event.target.closest('form');
    
      // If a form was found, proceed to enable the submit button and input fields
      if (form) {
          // Enable all input fields within the form
          let inputs = form.querySelectorAll('input, textarea, select');
          inputs.forEach(function(input) {
              input.removeAttribute('disabled');
          });
          
          // Enable all submit buttons within the form
          let submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
          submitButtons.forEach(function(button) {
              button.removeAttribute('disabled');
              button.innerText = "Submit"; // Reset button text if needed
          });
      }
});


function openShowModal(){
    $('#darkModal').modal('show');
}




function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);

}

// Function to remove query parameters from the URL
function removeQueryParam(param) {
    const url = new URL(window.location);
    url.searchParams.delete(param);
    window.history.replaceState({}, document.title, url.toString());
}

// Get the 'success' query parameter
const data = getQueryParam('created');

// Display SweetAlert if 'success' query parameter is true
if (data === 'true') {
    Swal.fire({
        title: 'Created!',
        text: 'Created Your Account Successfully! Kindly Check Your Email!',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('created');
    });
}

 const activated_data = getQueryParam('activated');

// Display SweetAlert if 'success' query parameter is true
if (activated_data === 'true') {
    Swal.fire({
        title: 'Activated!',
        text: 'Enjoy An Awesome Immersive Streaming Experience!',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('activated');
    });
}else if(activated_data === 'false'){
    Swal.fire({
        title: 'Error!',
        text: 'Activation Link is Invalid or expired!',
        icon: 'error',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('activated');
    });    
}

const auth_data = getQueryParam('authenticated');
if (auth_data === 'true') {
    Swal.fire({
        title: 'Log in success!',
        text: 'Enjoy An Awesome Immersive Streaming Experience!',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('authenticated');
    });
}else if(auth_data === 'false'){
    Swal.fire({
        title: 'Logged Out!',
        text: 'Session revoked!',
        icon: 'warning',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('authenticated');
    });    
}

const reset_data = getQueryParam('reset');

if (reset_data === 'true') {
    Swal.fire({
        title: 'Reset Initiation Success!',
        text: 'Please check your email for further instructions',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('reset');
    });
}


const updated_data = getQueryParam('updated');

if (updated_data === 'true') {
    Swal.fire({
        title: 'Password Reset Success!',
        text: 'Your Password Was successfully Updated,You Are Logged In!',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('updated');
    });
}

