document.addEventListener("DOMContentLoaded", () => {
    const mainSlider = document.querySelector(".main-slider");
    const mainSlides = document.querySelectorAll(".main-slide");
    let mainIndex = 0;

    function showNextMainSlide() {
        mainIndex = (mainIndex + 1) % mainSlides.length; // 인덱스를 순환하도록 설정
        mainSlider.style.transform = `translateX(${-mainIndex * 100}%)`;
    }

    // 3초마다 다음 슬라이드로 전환
    setInterval(showNextMainSlide, 3000);
});