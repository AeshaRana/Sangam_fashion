let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () => {
    searchForm.classList.toggle('active');
    // navbar.classList.remove('active');
}

document.querySelector('#search-btn1').onclick = () => {
    searchForm.classList.toggle('active');
    // navbar.classList.remove('active');
}

window.onscroll = () => {
    searchForm.classList.remove('active');
    // navbar.classList.remove('active');
}

var swiper = new Swiper(".home-slider", {
    centeredSlides: true,
    loop: true,
    autoplay: {
        delay: 9500,
        disableOnInteraction: false,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});



//filter buttons

let filterBtn = document.querySelectorAll('.filter-buttons .buttons');
let filterItem = document.querySelectorAll('.container .box-container .box');

filterBtn.forEach(button => {
    button.onclick = () => {
        filterBtn.forEach(btn => btn.classList.remove('active'))
        button.classList.add('active');

        let dataFilter = button.getAttribute('data-filter');
        filterItem.forEach(item => {

            item.classList.remove('active');
            item.classList.add('hide');

            if (item.getAttribute('data-item') == dataFilter || dataFilter == 'all') {
                item.classList.remove('hide');
                item.classList.add('active');
            }

        });
    };
});

// Featured product slider

var swiper = new Swiper(".featured-slider", {
    // centeredSlides:true,
    loop: true,
    spaceBetween: 20,
    autoplay:{
        delay:2000,
        disableOnInteraction:false,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        450: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 4,
        },
        1600: {
            slidesPerView: 4,
        },
    },
});

var swiper = new Swiper(".product-details-slider",{
    loop:true,
    spaceBetween:20,
    autoplay:{
        delay:9500,
        disableOnInteraction:false,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0:{
            slidesPerView: 1,
        },
        768:{
            slidesPerView: 1,
        },
        // 1600:{
        //     slidesPerView: 5,
        // },
    },
});


// increment and decrement
const quantityInput=document.getElementById('quantityInput');

function increment(){
    quantityInput.value=parseInt(quantityInput.value)+1;
}

function decrement(){
    if(quantityInput.value>1){
    quantityInput.value=parseInt(quantityInput.value)-1;
    }
}

// login registration 
const wrapper = document.querySelector('.wrapper');
const loginlink = document.querySelector('.login-link');
const registerlink = document.querySelector('.register-link');
// const iconClose=document.querySelector('.icon-close');

registerlink.addEventListener('click',()=>{
    wrapper.classList.add('active');
})


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

//productpage css
// script.js

document.addEventListener("DOMContentLoaded", function () {
    const priceFilter = document.getElementById('price_filter');
    const fltPrice = document.getElementById('flt_price');
    const priceFirstInput = document.getElementById('price_first');
    const priceSecondInput = document.getElementById('price_second');
  
    const slider = new Slider(priceFilter, {
      range: true,
      tooltip: 'hide',
      min: 0,
      max: 6000,
      value: [400, 4000],
     // handleColor: 'white', // Set handle color to white
     // selectionBarColor: 'red', // Set selection bar color to red
      clickToMove: true, // Enable moving the handle on click
    });
  
    slider.on('slide', function (values) {
      fltPrice.innerHTML = 'Rs:' + values[0] + ' to ' + values[1];
      priceFirstInput.value = values[0];
      priceSecondInput.value = values[1];
    });
  
    // Initial setup
    fltPrice.innerHTML = 'Rs:' + slider.getValue()[0] + ' to ' + slider.getValue()[1];
});


// auto scroll javascript

