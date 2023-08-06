// Добавляем обработчики событий для изменения изображения при наведении курсора
window.addEventListener('DOMContentLoaded', function() {
  var cards = document.querySelectorAll('.card');
  cards.forEach(function(card) {
    var image = card.querySelector('img');
    var description = card.querySelector('.card-description');
    
    card.addEventListener('mouseover', function() {
      image.style.filter = 'brightness(35%)'; // прозрачность затемнения
      description.style.display = 'block';
    });
    
    card.addEventListener('mouseout', function() {
      image.style.filter = 'none';
      description.style.display = 'none';
    });
  });
});

document.querySelectorAll('.scroll-btn').forEach((button) => {
  button.addEventListener('click', (event) => {
    const container = button.parentElement.querySelector('.card-container');
    const scrollAmount = 800; // измените это значение, чтобы контролировать скорость прокрутки

    if (button.classList.contains('right-scroll')) {
      container.scrollLeft += scrollAmount;
    } else {
      container.scrollLeft -= scrollAmount;
    }
  });
});


const open_popup = document.getElementById('logo');
open_popup.addEventListener('click', openPopup);


function openPopup() {
  document.getElementById('blackout').style.display = 'block';
}

function closePopup() {
  document.getElementById('blackout').style.display = 'none';
}
