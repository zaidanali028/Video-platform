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

 const data2 = getQueryParam('activated');

// Display SweetAlert if 'success' query parameter is true
if (data2 === 'true') {
    Swal.fire({
        title: 'Activated!',
        text: 'Enjoy An Awesome Immersive Streaming Experience!',
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        // Remove the 'success' query parameter from the URL
        removeQueryParam('activated');
    });
}else if(data2 === 'false'){
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