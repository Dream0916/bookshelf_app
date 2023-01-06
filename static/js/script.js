const viewButtons = document.querySelectorAll('.view-button');
viewButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    button.classList.toggle('focus');
  });
});