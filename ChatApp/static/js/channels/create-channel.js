// チャンネルを新規作成するモーダルの制御

const createChannelModal = document.getElementById("create-channel-modal");
const createChannelButton = document.getElementById("create-channel-button");
const closeButton = document.getElementById(
  "create-channel-modal-close-button"
);

// チャンネル作成ボタンが押された時にモーダルを表示する
createChannelButton.addEventListener("click", () => {
  createChannelModal.style.display = "flex";
});

// モーダル内のXボタンが押されたときにモーダルを閉じる
closeButton.addEventListener("click", () => {
  createChannelModal.style.display = "none";
});

// 画面のどこかが押された時にモーダルを閉じる
addEventListener("click", (e) => {
  if (e.target == createChannelModal) {
    createChannelModal.style.display = "none";
  }
});
