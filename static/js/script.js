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



  // Получаем элемент flip-box-inner
  var flipBoxInner = document.querySelector('.flip-box-inner');

  // Функция для переворачивания flip-box-inner
  function flip() {
    flipBoxInner.style.transform = 'rotateX(180deg)';
    setTimeout(function() {
      flipBoxInner.style.transform = 'rotateX(0deg)';
    }, 2000);
  }

  // Вызываем функцию flip каждую секунду
  setInterval(flip, 4000); // 2000 миллисекунд = 2 секунды