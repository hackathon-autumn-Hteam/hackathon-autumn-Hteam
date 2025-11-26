/*
ページネーションを作成・制御する関数。
チャンネル名、削除ボタンを作成・制御。
*/
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
    const paginationUl = document.querySelector(".pagination");
    let pageCount = 0;
    while (pageCount < TOTAL) {
      let pageNumber = document.createElement("li");
      pageNumber.dataset.pageNum = pageCount + 1;
      pageNumber.innerText = pageCount + 1;
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
      const lastChannelInPage = page * STEP;

      // 各チャンネル要素の作成
      channels.forEach((channel, i) => {
        if (i < firstChannelInPage - 1 || i > lastChannelInPage - 1) return;
        const a = document.createElement("a");
        const li = document.createElement("li");
        const channelURL = `/channels/${channel.channel_id}/messages`;
        a.innerText = channel.channel_name;
        a.setAttribute("href", channelURL);
        li.appendChild(a);
        ul.appendChild(li);
      });
    };

    // ページネーション内で現在選択されているページの番号に色を付ける
    const colorPaginationNum = () => {
      // ページネーションの数字部分の全要素から"colored"クラスを一旦取り除く
      const paginationArr = [...document.querySelectorAll(".pagination li")];
      paginationArr.forEach((page) => {
        page.classList.remove("colored");
      });
      // 選択されているページにclass="colored"を追加（文字色が変わる）
      paginationArr[page - 1].classList.add("colored");
    };

    const init = (page, STEP) => {
      createChannelsList(page, STEP);
      colorPaginationNum();
    };

    // 初期動作時に1ページ目を表示
    init(page, STEP);

    //前ページへ遷移
    document.getElementById("prev").addEventListener("click", () => {
      if (page <= 1) return;
      page = page - 1;
      init(page, STEP);
    });

    // 次ページ遷移
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

// DOMツリーが構築されたらpagination関数を発火（ページネーションを作成し、その後チャンネル追加ボタンを作成・表示）
document.addEventListener("DOMContentLoaded", function () {
  try {
    pagination();
  } catch (error) {
    console.log(`エラー：${error}`);
  }
});
