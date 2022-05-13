const signinBtn = document.querySelector("#signin-btn");
const signupBtn = document.querySelector("#signup-btn");
const container=document.querySelector(".container");

signupBtn.addEventListener('click',()=>{
	container.classList.add("signup-mode");
});

signinBtn.addEventListener('click',()=>{
	container.classList.remove("signup-mode");
});