// チャンネル一覧ページでレスポンスが返ってきたあと
// チャンネル一覧の配列データを元にページネーションを作成・制御する

const pagination = () => {
  try {
    let page = 1; // 今何ページ目にいるか
    const STEP = 5; // 1ページに表示する項目数

    // 全ページ数を計算
    //「 チャンネルの総数/ステップ数　の余りの有無で場合分
    // 余りがある場合は1ページ余分に追加する
    const TOTAL =
      channels.length % STEP == 0
        ? channels.length / STEP
        : Math.floor(channels.length / STEP) + 1;

    // ページネーションで表示されるページ数部分の要素を作成（＜　PREV 1 2 3 NEXT >)
    //querySelector() ＝＞指定されたセレクターまたはセレクター群に一致する、文書内の最初の要素を返す
    const paginationUl = document.querySelector(".pagination");
    let pageCount = 0;
    while (pageCount < TOTAL) {
      let pageNumber = document.createElement("li");
      pageNumber.dataset.pageNum = pageCount + 1;
      pageNumber.innerText = pageCount + 1;
      // appendChild　＝＞　特定の親ノードの子ノードリストの”末尾”に追加
      paginationUl.appendChild(pageNumber);
      //　ページネーションの数字部分が押された時にもページ数が変わるようにする処理
      pageNumber.addEventListener("click", (e) => {
        const targetPageNum = e.target.dataset.pageNum;
        page = Number(targetPageNum);
        init(page, STEP);
      });
      pageCount++;
    }

    // 各チャンネル名と削除ボタンの要素を作成
    const createChannelsList = (page, STEP) => {
      const ul = document.querySelector(".channels-box");
      // 一度チャンネルリストを空にする
      ul.innerHTML = "";

      const firstChannelInPage = (page - 1) * STEP + 1;
      const lasChannelInPage = page * STEP;

      //各チャンネル要素の作成
      channels.forEach((channel, i) => {
        // 表示範囲外のものを無視する
        if (i < firstChannelInPage - 1 || i > lasChannelInPage - 1) return;
        // 取得したデータに応じて自動でリストを作成する（HTMLで固定で書くと動的な更新が不可）
        const a = document.createElement("a");
        const li = document.createElement("li");
        const channelURL = `/channels/${channel.channel_id}/messages`;
        a.innerText = channel.channel_name;
      });
    };
    // ページネーション内で現在選択されているページの番号に色を付ける
    const colorPaginationNum = () => {
      // ページネーションの数字部分の全要素から"colored"クラスを一旦取り除く
      const paginationArr = [...document.querySelectorAll(".pagination li")];
      paginationArr.forEach((page) => {
        page.classList.remove("colored");
      });
      // 選択されているページに"class=colored"を追加（文字色が変わる）
      paginationArr[page - 1].classList.add("colored");
    };

    // 初期動作時に1ページ目を表示
    init(page, STEP);

    //前ページへ遷移
    document.getElementById("prev").addEventListener("click", () => {
      if (page <= 1) return;
      page = page - 1;
      init(page, STEP);
    });

    // 次ページへ遷移
    document.getElementById("next").addEventListener("click", () => {
      if (page >= channels.length / STEP) return;
      page = page + 1;
      init(page, STEP);
    });

    return true;
  } catch (error) {
    console.log(`エラー：${error}`);
    return false;
  }
};

//DOMツリーが構築されたらpagination関数を発火（ページネーションを作成）
document.addEventListener("DOMContentLoaded", function () {
  try {
    pagination();
  } catch (error) {
    console.log(`エラー：${error}`);
  }
});
