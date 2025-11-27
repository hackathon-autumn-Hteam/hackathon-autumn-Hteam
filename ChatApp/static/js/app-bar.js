const menu = document.getElementById("header-menu");
const btn = document.getElementById("hamburger");

// スライドメニューボタンを押した時の処理
btn.addEventListener("click", (event) => {
  event.stopPropagation();
  toggleMenu();
});

// ボタン以外を押した時の処理
document.addEventListener("click", (event) => {
  // スライドメニューボタンやスライドメニュー以外を押し、さらにメニューが開いている時にメニューを閉じる
  if (
    !menu.contains(event.target) &&
    !btn.contains(event.target) &&
    menu.classList.contains("open")
  ) {
    toggleMenu();
  }
});

// メニューの開閉処理
function toggleMenu() {
  btn.classList.toggle("open");
  menu.classList.toggle("open");

  if (menu.classList.contains("open")) {
    // メニューを開く
    menu.style.height = menu.scrollHeight + "px";
  } else {
    // メニューを閉じる
    menu.style.height = "0";
  }
}
