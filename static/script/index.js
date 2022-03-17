let page = 0;
let keyword = "";
// let src = "http://127.0.0.1:3000/api/attractions?page=" + page + "&keyword=" + keyword;
let src = "http://3.230.236.135:3000/api/attractions?page=" + page + "&keyword=" + keyword;


// 建立照片資料元素到網頁
// 新增id建立連結
let i = 0;
const showData = (listN, listM, listC, listI, ListD) => {
    for (let count = 0; count < listN.length; count++) {
        let aBox = document.createElement("a");
        let divName = document.createElement("div");
        let divMrt = document.createElement("div");
        let divCat = document.createElement("div");
        let img = document.createElement("img");
        let nameText = document.createTextNode(listN[count]);
        let mrtText = document.createTextNode(listM[count]);
        let catText = document.createTextNode(listC[count]);
        aBox.id = "box" + i;
        divName.id = "name" + i;
        divMrt.id = "mrt" + i;
        divCat.id = "category" + i;
        img.src = listI[count];
        aBox.href = "http://127.0.0.1:3000/attraction/" + ListD[count];
        divName.appendChild(nameText);
        divMrt.appendChild(mrtText);
        divCat.appendChild(catText);
        document.getElementsByClassName("content")[0].appendChild(aBox);
        document.getElementById("box" + i).appendChild(img);
        document.getElementById("box" + i).appendChild(divName);
        document.getElementById("box" + i).appendChild(divMrt);
        document.getElementById("box" + i).appendChild(divCat);
        i++;
    }
}


// 自動載入後續頁面的功能

// 觸發條件
let options = { rootMargin: '20px', threshold: 0, };

// 觸發條件後的回呼函式
let callback = (entry) => {
    if (entry[0].isIntersecting) {
        keyword = document.getElementById("keyword").value;
        console.log("SCROLL CALLBACK OK")

        if (page != null) {
            // src = "http://3.230.236.135:3000/api/attractions?page=" + page + "&keyword=" + keyword;
            src = "http://127.0.0.1:3000/api/attractions?page=" + page + "&keyword=" + keyword;
            let listName = [];
            let listMrt = [];
            let listCat = [];
            let listImg = [];
            let listId = [];
            // 新增id作為連結網址id

            fetch(src)
                .then((response) => {
                    return response.json();
                })
                .then((result) => {
                    page = result.nextPage;
                    if (result.error) { // 先確認有無此資料
                        console.log("查無此景點")
                        observer.unobserve(target); // 沒有資料的話記得要關閉observer，不然之後很難再打開
                        div = document.createElement('div');
                        div.id = "errMsg";
                        txt = document.createTextNode("查無此景點");
                        div.appendChild(txt);
                        document.getElementById("content").appendChild(div);
                    } else {

                        for (let i in result.data) {
                            let name = result.data[i].name;
                            let mrt = result.data[i].mrt;
                            let cat = result.data[i].category;
                            let img = result.data[i].images[0]
                            let id = result.data[i].id;
                            listName.push(name);
                            listMrt.push(mrt);
                            listCat.push(cat);
                            listImg.push(img);
                            listId.push(id);
                        }
                        showData(listName, listMrt, listCat, listImg, listId);
                        console.log("nextPage: " + page);
                        console.log("keyword: " + keyword);
                    }
                })

        } else { observer.unobserve(target); }
    }
}

// 建立 IntersectionObserver物件
let observer = new IntersectionObserver(callback, options);
const target = document.querySelector("#end"); // observer的target
observer.observe(target); // 開啟觀察目標


// 關鍵字搜尋功能
const searchKeyword = () => {
    document.getElementById("content").innerHTML = "";
    page = 0;
    keyword = document.getElementById("keyword").value;
    observer.observe(target);
}