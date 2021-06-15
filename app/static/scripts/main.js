
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
checkBtn.addEventListener('click', changeIcon)

function changeIcon(){
    if (checkBtn.innerHTML == '<i class="fas fa-bars"></i>'){
        checkBtn.innerHTML = '<i class="far fa-window-close"></i>';
    }
    else{
        checkBtn.innerHTML = '<i class="fas fa-bars"></i>';
    }
    
}





// // Display popup box

function add_CssClass(){
    document.getElementsByClassName('pop')[0].classList.add('active')
    document.getElementsByClassName('pop_box')[0].classList.add('popactive')
}


function remove_cssClass(){
     document.getElementsByClassName('pop')[0].classList.remove('active')
    document.getElementsByClassName('pop_box')[0].classList.remove('popactive')
}


// close flash message alert

function alertClose(){
    document.getElementsByClassName('alert')[0].classList.add('remove_alert')
}




