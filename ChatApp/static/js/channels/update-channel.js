// チャンネルを編集するモーダルの制御

// モーダルウィンドウを「開く」ボタン @messages.html
const updateButton = document.getElementById("update-channel-button");

// モーダルウィンドウを「閉じる」ボタン @update-channel.html
const updatePageButtonClose = document.getElementById("close-modal-button");

// モーダル @update-channel.html
const updateChannelModal = document.getElementById("update-channel-modal");

// 「編集する」ボタン @update-channel.html
const editChannelDescription = document.getElementById(
  "edit-channel-description-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateChannelModal) {
  // TODO(rootさん): id="update-channel-button"のボタンがクリックされた時に、モーダルを表示する
  // メッセージページ内の「チャンネル編集」アイコンが押された時にモーダルを表示する
  updateButton.addEventListener("click", () => {
    updateChannelModal.style.display = "flex";
  });

  // TODO(rootさん): id="close-modal-button"のボタンがクリックされた時に、モーダルを非表示にする
  // チャンネル編集モーダル内の「閉じる」アイコンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
  });

  // チャンネル編集モーダル内の「編集する」ボタンが押された時に情報を送信する
  editChannelDescription.addEventListener("click", () => {
    const newChannelDescription =
      document.updateChannelForm.channelDescription.value;
    if (newChannelDescription !== "") {
      document.updateChannelForm.submit();
    }
    updateChannelModal.style.display = "flex";
  });

  // TODO(rootさん): 画面のどこかが押された時に、モーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateChannelModal) {
      updateChannelModal.style.display = "none";
    }
  });
} else {
  // デバッグ用
  console.log("モーダルが見つかりません");
}
