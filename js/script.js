
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



function showOrHide() 
    let showpass = document.getElementById("pass");
    let check = document.getElementById("showpassword");
    if (check.checked) {
      showpass.type = "text";
    } else {
      showpass.type = "password";
    }
  }

function login() {
    let loginuser = ""
    let username = document.getElementById("emailaddress").value;
    let password = document.getElementById("password").value;
  
    let found = false;
    let i = 0;
  
    while (!found && i < userdata.length)
      loginuser = userdata[i];
      if (loginuser.hasOwnProperty("name") && loginuser.hasOwnProperty("password"))
        if (loginuser.name === username && loginuser.password === password) {
          found = true;
        }
      }
      i++;
    }
  
var login = function() {
    var email = $("#email").val();
    var password = $("#password").val();
    var userInfo = { "email": email, "password": password };
    Nebula.User.login(userInfo)
        .then(function(user) {
            window.location.href = "app.html";
        })
        .catch(function(e) {
            alert(e.statusText);
        });
};

var signup = function() {
    var email = $("#email").val();
    var password = $("#password").val();
    var password_confirmation = $("#password_confirm").val();

    if (password !== password_confirmation) {
        alert("Passwords does not match.");
        return;
    }

    var user = new Nebula.User();
    user.set("email", email);
    user.set("password", password);
    user.register()
        .then(function(u) {
            alert("User registered.");
            window.location.href = "index.html";
        })
        .catch(function(e) {
            alert(e.statusText);
            clear();
        })
};

init: function () {
    var self = this;

   Nebula.User.current()
        .then(function(user) {
            if (user === null) {
                window.location.href = "index.html"; // 未ログイン
                return;
            }
            self.user = user; // ユーザ情報保存
            self.initApp();
        })
        .catch(function () {
            window.location.href = "index.html"; // 未ログイン
        });
},

logout: function() {
    Nebula.User.logout()
        .then(function() {
            window.location.href = "index.html";
        })
        .catch(function(e) {
            window.location.href = "index.html";
        })
},


  // ログイン処理
        function nextPage() {
            id = document.login_form.id.value
            pwd = document.login_form.pass.value;
            location.href = id + pwd + ".html";
        }
        

 
