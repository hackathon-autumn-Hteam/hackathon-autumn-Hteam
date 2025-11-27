// チャンネルを編集するモーダルの制御
const updateChannelModal = document.getElementById("update-channel-modal");
const updateButton = document.getElementById("update-channel-button");
const updatePageButtonClose = document.getElementById(
  "update-channel-modal-close-button"
);
const updateChannelInfo = document.getElementById("update-channel-form");

// モーダルが存在するページのみ（uidとチャンネルidが同じ時のみ）
if (updateChannelModal) {
  updateButton.addEventListener("click", () => {
    updateChannelModal.style.display = "flex";
  });

  // チャンネル編集モーダル内の「閉じる」アイコンが押された時にモーダルを非表示にする
  updatePageButtonClose.addEventListener("click", () => {
    updateChannelModal.style.display = "none";
    if (updateChannelInfo) {
      updateChannelInfo.reset();
    }
  });

  addEventListener("click", (e) => {
    if (e.target == updateChannelModal) {
      updateChannelModal.style.display = "none";
      if (updateChannelInfo) {
        updateChannelInfo.reset();
      }
    }
  });
}
