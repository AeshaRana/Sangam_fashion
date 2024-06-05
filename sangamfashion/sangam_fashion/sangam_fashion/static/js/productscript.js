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

