// チャンネルを編集するモーダルの制御

// モーダルウィンドウを「開く」ボタン @messages.html
const updateButton = document.getElementById("update-channel-button");

// モーダルウィンドウを「閉じる」ボタン @update-channel.html
const updatePageButtonClose = document.getElementById(
  "update-channel-modal-close-button"
);

// モーダル @update-channel.html
const updateChannelModal = document.getElementById("update-channel-modal");

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateChannelModal) {
  // メッセージページ内の「チャンネル編集」アイコンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateChannelModal.style.display = "flex";
  });

  // チャンネル編集モーダル内の「閉じる」アイコンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
  });

  addEventListener("click", (e) => {
    if (e.target == updateChannelModal) {
      updateChannelModal.style.display = "none";
    }
  });
}
