// メッセージ編集モーダル
const updateMessageModal = document.getElementById("update-message-modal");
const closeButton = document.getElementById(
  "update-message-modal-close-button"
);

const updateMessageForm = document.getElementById("update-message-form");
const modalMessageText = document.getElementById("modal-message-text");
const updateButtons = document.querySelectorAll(".update-message-button");

if (updateMessageModal && updateButtons.length > 0) {
  updateButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const messageId = btn.dataset.messageId; // メッセージID
      const messageText = btn.dataset.messageText; // メッセージ本文
      const channelId = btn.dataset.channelId; // チャンネルID（テンプレで渡す）

      // モーダルを表示
      updateMessageModal.style.display = "flex";

      // textarea に本文をセット
      modalMessageText.value = messageText;

      // form.action をセット
      updateMessageForm.action = `/channels/${channelId}/messages/${messageId}`;
    });
  });

  // 閉じるボタン
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
