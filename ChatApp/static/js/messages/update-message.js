// メッセージを編集するモーダルの制御

const updateButton = document.getElementById("update-message-button");
const updateMessageModal = document.getElementById("update-message-modal");
const closeButton = document.getElementById(
  "update-message-modal-close-button"
);

if (updateMessageModal) {
  // モーダルを開く
  updateButton.addEventListener("click", () => {
    updateMessageModal.style.display = "flex";
  });

  // モーダルを閉じる（×ボタン）
  closeButton.addEventListener("click", () => {
    updateMessageModal.style.display = "none";
  });

  // 背景クリックで閉じる
  document.addEventListener("click", (e) => {
    if (e.target === updateMessageModal) {
      updateMessageModal.style.display = "none";
    }
  });
}
