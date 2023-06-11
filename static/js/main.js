const slides = document.querySelectorAll('.slide');
const next = document.querySelector('#next');
const prev = document.querySelector('#prev');
const auto = false; //автоматическое переключение слайдов
const intervalTime = 3000;
let slideInterval;

const nextSlide = () => {
    const current = document.querySelector('.current');
    current.classList.remove('current')

    //Проверяем есть ли след слайд
    if(current.nextElementSibling) {
        //добавляем класс current к нему
        current.nextElementSibling.classList.add('current');
    }
        else {
            slides[0].classList.add('current');
        }
        setTimeout(() => current.classList.remove('current'));
    }

const prevSlide = () => {
    const current = document.querySelector('.current');
    current.classList.remove('current')
    
    //Проверяем есть ли предыдущий слайд
    if(current.previousElementSibling) {
         //добавляем класс current к нему
        current.previousElementSibling.classList.add('current');
    }
        else {
            slides[slides.length - 1].classList.add('current');
        }
        setTimeout(() => {
            current.classList.remove('current');
        });
    }


    next.addEventListener('click', e => {
        nextSlide();
        if (auto) {
            clearInterval(slideInterval);
            slideInterval = setInterval(nextSlide, intervalTime);
         }
    })

    prev.addEventListener('click', e => {
        prevSlide();
        if (auto) {
            clearInterval(slideInterval);
            slideInterval = setInterval(nextSlide, intervalTime);
        }
    })
    
    if (auto) {
        slideInterval = setInterval(nextSlide, intervalTime);
    }