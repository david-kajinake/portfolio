const projects = document.querySelectorAll(".project-card");

//Route to project.html on click
projects.forEach(project=>{
    project.addEventListener("click",()=>{
        const redirect_url = `${window.origin}/projects/${project.id}/`;
        window.location.href = redirect_url
    });
});