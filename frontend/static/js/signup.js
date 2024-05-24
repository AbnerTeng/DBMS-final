document.getElementById('signup-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Sign up failed');
        }
    }).then(data => {
        alert(data.message);
    }).catch(error => {
        alert(error.message);
    })
});