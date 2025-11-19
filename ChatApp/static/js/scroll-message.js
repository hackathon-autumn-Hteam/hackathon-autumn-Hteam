// ページ読み込み時にメッセージエリアの最下部までスクロール
document.addEventListener("DOMContentLoaded", function () {
  const messageArea = document.querySelector(".message-area");

  if (!messageArea) return;

  // すぐ実行すると若干残るため、遅延させる
  setTimeout(function () {
    messageArea.scrollTop = messageArea.scrollHeight;
  }, 100);
});
