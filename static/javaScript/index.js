const signUpBtn = document.getElementById('signUp');
const signInBtn = document.getElementById('signIn');
const logincontainer = document.getElementById('login-container');

signUpBtn.addEventListener('click', () => {
    logincontainer.classList.remove('right-panel-active');
});

signInBtn.addEventListener('click', () => {
    logincontainer.classList.add('right-panel-active');
});
