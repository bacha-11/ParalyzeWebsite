
// provide color to the active link
let currentLocation = location.href
let addActive = document.querySelectorAll('.addActive');
for(let i=0; i<addActive.length; i++ ) {

    if (addActive[i].href === currentLocation) {
        addActive[i].classList.add('active');
    }
}


// Change navbar icon
let checkBtn = document.querySelector('.checkBtn');

function changeLoge(){
    if (checkBtn.innerHTML == '<i class="fas fa-bars"></i>'){
        checkBtn.innerHTML = '<i class="far fa-window-close"></i>'
    }
    else{
        checkBtn.innerHTML = '<i class="fas fa-bars"></i>'
    }
    
}

checkBtn.addEventListener('click', changeLoge)
