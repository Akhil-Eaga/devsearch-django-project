let projectsUrl = "http://127.0.0.1:8000/api/projects/"

let getProjects = () => {
    fetch(projectsUrl)
    .then(response => response.json())
    .then(data => {
        buildProjects(data);
    })
}

let buildProjects = (projects) => {
    var root = document.getElementById('projects-wrapper');
    root.innerHTML = "";

    var all_projects = ""

    for(let i =0; i < projects.length; i++){
        project = projects[i];
        projectString  = `
            <div class="project--card">
                <div class="image--container">
                    <img src="http://127.0.0.1:8000${project.featured_image}">
                </div>
                <div class="card--content">
                    <h1 class="project--header">${project.title}</h1>
                    <p><i>${project.vote_ratio}% positive feedback</i></p>
                    <p>${project.description.substring(0,150)}</p>
                    <button class="vote--option" data-vote="up" data-project="${project.id}">Upvote</button> &nbsp;
                    <button class="vote--option" data-vote="down" data-project="${project.id}">Downvote</button>
                </div>
            </div>
        `
        root.innerHTML += projectString;
    }

    // call the addVoteEvents to add event listeners
    addVoteEvents();
}

let addVoteEvents = () => {
    let voteButtons = document.querySelectorAll('.vote--option');
    
    for(let i = 0; i < voteButtons.length; i++) {
        voteButtons[i].addEventListener('click', (event) => {

            // GET THE PROJECT AND THE TYPE OF VOTE THE USER HAS CLICKED ON
            // custom html element attributes that are 
            // of the form data-something can be accessed as element.dataset.something
            let vote = event.target.dataset.vote;
            let projectId = event.target.dataset.project;

            let token = localStorage.getItem('token');


            fetch(`http://127.0.0.1:8000/api/projects/${projectId}/vote/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({'value': vote}),
            })
            .then(response => response.json())
            .then(data => {
                getProjects();
            })
        })
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location = "login.html";
}

// window loads here
window.onload = function() {
    if (localStorage.getItem('token') == undefined) {
        window.location = "login.html";
    }
    else {
        getProjects()
    }
    
}