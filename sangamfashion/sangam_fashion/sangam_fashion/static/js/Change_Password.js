const wrapper = document.querySelector('.wrapper');
const loginlink = document.querySelector('.login-link');

loginlink.addEventListener('click',()=>{
    wrapper.classList.remove('active');
})

document.addEventListener('DOMContentLoaded', function () {
    const loginWrapper = document.querySelector('.wrapper');
    const closeIcon = document.querySelector('.icon-close');

    closeIcon.addEventListener('click', function () {
        wrapper.style.display = 'none'; 
    });
});


