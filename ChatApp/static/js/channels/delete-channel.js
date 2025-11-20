// チャンネルを削除するモーダルの制御

const deleteChannelModal = document.getElementById("delete-channel-modal");
const deleteChannelButton = document.getElementById("delete-channel-button");
const deleteChannelButtonClose = document.getElementById(
  "delete-channel-modal-close-button"
);

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (deleteChannelModal) {
  // 「ゴミ箱」アイコンが押されたときモーダルを表示する
  deleteChannelButton.addEventListener("click", () => {
    deleteChannelModal.style.display = "flex";
  });

  // モーダルを閉じるボタンが押されたときモーダルを非表示にする
  deleteChannelButtonClose.addEventListener("click", () => {
    deleteChannelModal.style.display = "none";
  });

  // 画面のどこかを押されたときに、モーダルを非表示にする
  addEventListener("click", (e) => {
    if (e.target == deleteChannelModal) {
      deleteChannelModal.style.display = "none";
    }
  });
}
