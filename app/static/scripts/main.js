
// provide color to the active link
let currentLocation = location.href
let addActive = document.querySelectorAll('.addActive');
for(let i=0; i<addActive.length; i++ ) {

    if (addActive[i].href === currentLocation) {
        addActive[i].classList.add('active');
    }
}


// Change navbar logo
// let checkBtn = document.querySelector('.checkBtn');

// function changeLoge(){
//     checkBtn.innerHTML = '<i class="fas fa-remove"></i>'
// }

// checkBtn.addEventListener('click', changeLoge)
