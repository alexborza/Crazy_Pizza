const imageContainer = document.querySelector('.image-container');
const images = document.querySelectorAll('.image-container img');

//Buttons
const prevBtn = document.querySelector('#prevBtn');
const nextBtn = document.querySelector('#nextBtn');

//Counter
let counter = 1;
const size = images[0].clientWidth;

imageContainer.style.transform = 'translateX(' + (-size * counter) + 'px)';

//Button Listeners

nextBtn.addEventListener('click', ()=>{
    if (counter >= images.length - 1) return;
    imageContainer.style.transition = "transform 0.4s ease-in-out";
    counter++;
    imageContainer.style.transform = 'translateX(' + (-size * counter) + 'px)';
})

prevBtn.addEventListener('click', ()=>{
    if (counter <= 0) return;
    imageContainer.style.transition = "transform 0.4s ease-in-out";
    counter--;
    imageContainer.style.transform = 'translateX(' + (-size * counter) + 'px)';
})

imageContainer.addEventListener('transitionend', ()=>{
    if (images[counter].id === 'lastClone'){
        imageContainer.style.transition = "none";
        counter = images.length - 2;
        imageContainer.style.transform = 'translateX(' + (-size * counter) + 'px)';
    }
})

imageContainer.addEventListener('transitionend', ()=>{
    if (images[counter].id === 'firstClone'){
        imageContainer.style.transition = "none";
        counter = images.length - counter;
        imageContainer.style.transform = 'translateX(' + (-size * counter) + 'px)';
    }
})
