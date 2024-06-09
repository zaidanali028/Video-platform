document.addEventListener('DOMContentLoaded', function () {

    
    const closeModalButton = document.getElementById('closeModal');
    const modal = document.getElementById('modal');
    


if (closeModalButton) {
    closeModalButton.addEventListener('click', function () {
        // Close the modal
        modal.classList.remove('opacity-100', 'pointer-events-auto');
        modal.classList.add('opacity-0', 'pointer-events-none');
    });
}

// Close the modal when clicking outside of the modal content
window.addEventListener('click', function (event) {
    if (event.target === modal) {
        modal.classList.remove('opacity-100', 'pointer-events-auto');
        modal.classList.add('opacity-0', 'pointer-events-none');
    }
});


document.addEventListener("htmx:beforeSwap", function(event) {
    // before swapping uponn success of post request,
    if(((event.detail.target.id=='showForm') ||(event.detail.target.id=='videoForm') ||(event.detail.target.id=='genreForm') || (event.detail.target.id=='categoryForm')) &&  (!event.detail.xhr.response)){
        // if any of the forms above made the request and it returned an empty response,then all went well for adding to its model  so close modal
        // !event.detail.xhr.response will be true because each post request done upon success will have an epty response 
        // with a 204 status code
        modal.classList.add('opacity-0', 'pointer-events-none');
        modal.classList.remove('opacity-100', 'pointer-events-auto');
        Swal.fire({
            title: 'Success!',
            text: 'Transaction Was Successful!',
            icon: 'success',
            confirmButtonText: 'OK'
        }).then(() => {});
    }
});

});

document.addEventListener("htmx:beforeRequest", function(event) {
    //this event is invoked before a request is sent to the server using HTMX


    inputs=['nameInput','emailInput','phoneNumInput','brandInput','passwordConfirmInput','passwordInput']

    // Access the endpoint URL from the event detail
    const url_origin = event.detail.pathInfo.requestPath || event.detail.pathInfo.finalRequestPath;
   if (url_origin=="/admin-app/post-config/"){
    // console.log(url_origin=="/admin-app/post-config/")
    // if user clicks on a button to send config FormData,
     // disable input fields
     inputs.forEach(function(id) {
        let input = document.querySelector('#' + id);
        if (input) {
            
                input.setAttribute('disabled', 'disabled');
    
        }
    });

   }

    
   
  
    
});


document.addEventListener("htmx:afterRequest", function(evt) {
  
    inputs=['nameInput','emailInput','phoneNumInput','brandInput','passwordConfirmInput','passwordInput']
        // Loop through each input ID and disable the corresponding input
        inputs.forEach(function(id) {
            let input = document.querySelector('#' + id);
            if (input) {
                input.removeAttribute('disabled');

            }
        });
});


document.addEventListener("htmx:response", function(event) {
    var response = event.detail.xhr.response;
    var redirectUrl = response.headers.get('HX-Redirect');
    if (redirectUrl) {
        // Redirect to the specified URL
        window.location.href = redirectUrl;
    }
});



// user acc creation sweet alert start
 // Function to get query parameters from the URL
    // using it to find ?success=true
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
    const success = getQueryParam('success');

    // Display SweetAlert if 'success' query parameter is true
    if (success === 'true') {
        Swal.fire({
            title: 'Success!',
            text: 'Successful Transaction!',
            icon: 'success',
            confirmButtonText: 'OK'
        }).then(() => {
            // Remove the 'success' query parameter from the URL
            removeQueryParam('success');
        });
    }
// user acc creation sweet alert end






function openModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('opacity-0', 'pointer-events-none');
    modal.classList.add('opacity-100', 'pointer-events-auto');
}

// getting csrf-token for making requests
function getCsrfToken() {
    const hxHeaders = document.body.getAttribute('hx-headers');
    const headers = JSON.parse(hxHeaders);
    return headers['X-CSRFToken'];
}

function showConfirmationDialog() {
    return Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    });
}

// Generic function to handle deletion
function deleteItem(itemType, itemId) {
    // alert(`${itemType}-${itemId}`)
    const csrfToken = getCsrfToken();
    const url = `/admin-app/${itemType}/delete/${itemId}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`${itemType}-${itemId}`).remove();
            Swal.fire(
                'Deleted!',
                `${capitalize(itemType)} has been deleted.`,
                'success'
            );
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire(
            'Error!',
            `There was an error deleting the ${itemType}.`,
            'error'
        );
    });
}

// Function to confirm deletion and call the generic delete function
function confirmDelete(modelId) {
    showConfirmationDialog().then((result) => {
        if (result.isConfirmed) {
            const url_origin = window.location.pathname;
            if (url_origin == "/admin-app/genres/") {
                deleteItem('genres', modelId);
            } else if (url_origin == "/admin-app/categories/") {
                deleteItem('categories', modelId);
            } else if (url_origin == "/admin-app/videos/") {
                deleteItem('videos', modelId);
            }
            else if (url_origin == "/admin-app/shows/") {
                deleteItem('shows', modelId);
            }
        }
    });
}
// Utility function to capitalize the first letter of a string
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}



