
document.addEventListener('DOMContentLoaded', function(){
  var body = document.body;
  var hellobar = document.querySelector('.hellobar');

  if (hellobar && getComputedStyle(hellobar).display !== 'none') {
    body.classList.add('hellobar-visible');
  }

  document.querySelectorAll('.close-hellobar').forEach(function(button){
    button.addEventListener('click', function(){
      if (hellobar) {
        hellobar.style.display = 'none';
        body.classList.remove('hellobar-visible');
      }
    });
  });
});
