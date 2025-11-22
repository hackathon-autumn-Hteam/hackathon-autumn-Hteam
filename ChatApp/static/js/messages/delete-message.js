// メッセージを削除するモーダルの制御
// 担当ではないためローカルで所持

const deleteMessageModal = document.getElementById("delete-message-modal");
const deleteMessageButtonClose = document.getElementById(
  "delete-message-modal-close-button"
);

const deleteMessageForm = document.getElementById("delete-message-form");
const deleteMessageButtons = document.querySelectorAll(
  ".delete-message-button"
);

if (deleteMessageModal && deleteMessageButtons.length > 0) {
  deleteMessageButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const messageId = btn.dataset.messageId; //　メッセージID
      const channelId = btn.dataset.channelId; // チャンネルID

      // console.log("delete target:", { channelId, messageId }); // 検証用

      // モーダルを表示する
      deleteMessageModal.style.display = "flex";

      // form.actionをセット
      deleteMessageForm.action = `/channels/${channelId}/messages/${messageId}`;
    });
  });

  // モーダルを閉じるボタンが押されたときモーダルを非表示にする
  deleteMessageButtonClose.addEventListener("click", () => {
    deleteMessageModal.style.display = "none";
  });

  // 画面のどこかを押されたときに、モーダルを非表示にする
  document.addEventListener("click", (e) => {
    if (e.target == deleteMessageModal) {
      deleteMessageModal.style.display = "none";
    }
  });
}
