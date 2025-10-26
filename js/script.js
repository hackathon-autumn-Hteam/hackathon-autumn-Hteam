
//hamburger Menu

$('#show').on('click', function(){
  $(this).toggleClass('active');
  $('#nav').toggleClass('active');
  $('body').toggleClass('active');
});

$('.nav-menu li a').on('click', function () {
    $('#show').removeClass('active');
    $('#nav').removeClass('active');
    $('body').removeClass('active');
});

//

<nav id="nav">
  <ul class="nav-menu">
    <li class="nav-title">Menu</li>
    <li><a href="#">link</a></li>
    <li><a href="#">linklinklink</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
    <li><a href="#">link</a></li>
  </ul>  
</nav>





