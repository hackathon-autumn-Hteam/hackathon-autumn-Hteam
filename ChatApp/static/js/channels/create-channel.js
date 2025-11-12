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
  createChannelModal.style.display == "none";
});

// 画面のどこかが押された時にモーダルを閉じる
addEventListener("click", (e) => {
  if (e.target == createChannelModal) {
    createChannelModal.style.display == "none";
  }
});

// 必須ではないので余裕があったら検討する（一旦残しておく）
// create-channel-modalが表示されている時に Ctrl/Command + Enterで送信
// Enterでの自動送信を防ぐ
document.addEventListener("keydown", keydownEvent);

function keydownEvent(e) {
  // -(ハイフン)は演算子になってしまうのをどうするか？
  const newChannelName = document.create - channel.channel_name.value;

  const createChannelModal = document.getElementById("create-channel-modal");
  const createChannelModalStyle = getComputedStyle(
    createChannelModal,
    null
  ).getPropertyValue("display");

  if (e.code === "Enter") {
    e.preventDefault();
  }
  // Ctrl（またはcommand）＋Enter が押されていて、かつモーダルが開いていて、チャンネル名が空でないときに送信する
  //「keycode」は昔からある数字でキーを表す記述方法（現在は非推奨だが、古いブラウザなどに対応するため両方の記述方法で書いておく
  if (
    ((e.ctrlKey && !e.metaKey) || (!e.ctrlKey && e.metaKey)) &&
    e.keyCode == 13
  ) {
    if (e.code === "Enter") {
      if (createChannelModalStyle !== "none") {
        if (newChannelName !== "") {
          document.createChannelForm.submit();
        }
      }
    }
  }
}
