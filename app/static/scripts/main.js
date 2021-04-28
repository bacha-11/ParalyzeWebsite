let currentLocation = location.href
let addActive = document.querySelectorAll('.addActive');
for(let i=0; i<addActive.length; i++ ){

    if (addActive[i].href === currentLocation){
        addActive[i].classList.add('active')
    }
}
