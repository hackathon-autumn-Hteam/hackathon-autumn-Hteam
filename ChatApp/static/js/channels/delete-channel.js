// チャンネルを削除するモーダルの制御

// console.log("delete-channel.js loaded");　検証用

const deleteChannelModal = document.getElementById("delete-channel-modal");
const deleteChannelButtonClose = document.getElementById(
  "delete-channel-modal-close-button"
);

const deleteChannelForm = document.getElementById("delete-channel-form");
const deleteChannelButton = document.getElementById("delete-channel-button");

if (deleteChannelModal && deleteChannelButton) {
  deleteChannelButton.addEventListener("click", () => {
    const channelId = deleteChannelButton.dataset.channelId;

    // console.log("delete channel target", channelId);　検証用

    // モーダルを表示する
    deleteChannelModal.style.display = "flex";

    deleteChannelForm.action = `/channels/${channelId}`;
  });

  // モーダルを閉じるボタンが押されたときモーダルを非表示にする
  deleteChannelButtonClose.addEventListener("click", () => {
    deleteChannelModal.style.display = "none";
  });

  // 画面のどこかを押されたときモーダルを非表示にする
  document.addEventListener("click", (e) => {
    if (e.target == deleteChannelModal) {
      deleteChannelModal.style.display = "none";
    }
  });
}
