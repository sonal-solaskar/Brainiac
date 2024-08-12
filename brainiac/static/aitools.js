const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');
const tools = document.querySelector('.tools');

let currentIndex = 0;
const cardWidth = 320; 
const visibleCards = 3;

leftArrow.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        tools.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
    }
});

rightArrow.addEventListener('click', () => {
    if (currentIndex < tools.children.length - visibleCards) {
        currentIndex++;
        tools.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
    }
});
