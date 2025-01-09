document.addEventListener("DOMContentLoaded", () => {
    let burgermenu=document.querySelector(".burger-menu");
    let popupmenu=document.querySelector(".popup-menu");
    burgermenu.addEventListener('click',()=>{
        popupmenu.classList.toggle('active');
    });

    let closeicon=document.querySelector(".close-icon")
    closeicon.addEventListener('click',()=>{
        popupmenu.classList.remove('active');
    });
});