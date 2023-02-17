window.onload = function() {

    if (localStorage.getItem('token') != undefined) {
        window.location = "projects-list.html";
    }
    let form = document.getElementById('login-form');

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        console.log('Form was submitted');
        let formData = {
            'username': form.username.value,
            'password': form.password.value,
        }
        console.log(formData);

        fetch('http://127.0.0.1:8000/api/users/token/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if(data.access) {
                localStorage.setItem('token', data['access']);
                window.location = 'projects-list.html';
            }
            else {
                alert('Invalid username or password');
            }
            
        })
    })

}