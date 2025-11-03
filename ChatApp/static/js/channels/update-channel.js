/*
チャンネルを更新するモーダルの制御
*/

// チャンネルを編集するモーダルの制御

// モーダルウィンドウを「開く」ボタン
const updateButton = document.getElementById("update-channel-button");

// モーダルウィンドウを「閉じる」ボタン。
const updatePageButtonClose = document.getElementById("close-modal-button");

// 「編集する」ボタン

// モーダル。IDは後で確認@update-channel.html。
const updateChannelModal = document.getElementById("update-channel-modal");
// マスク(モーダルの背景をマスクする)

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

  // TODO(rootさん): 画面のどこかが押された時に、モーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == updateChannelModal) {
      updateChannelModal.style.display = "none";
    }
  });

  // TODO(root):チャンネル編集モーダル内の「編集する」ボタンが押された時にモーダルを非表示にする
} else {
  console.log("モーダルが見つかりません");
}

// update-channel-modalが表示されている時に Ctrl/Command + Enter で送信
function sendUpdateForm() {
  const newChannelTitle = document.updateChannelForm.channelTitle.value;

  if (newChannelTitle !== "") {
    document.updateChannelForm.submit();
  }
}
