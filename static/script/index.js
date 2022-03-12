let page = 0;
let keyword = "";


// 取得景點資料，並新增照片資料到網頁
const fetchData = () => {
    let src = "http://127.0.0.1:3000/api/attractions?page=" + page + "&keyword=" + keyword;
    let listName = [];
    let listMrt = [];
    let listCat = [];
    let listImg = [];
    fetch(src)
        .then(function(response) {
            return response.json();
        })
        .then(function(result) {
            page = result.nextPage;
            console.log(result);
            console.log([page]);
            if (result.data) {
                for (let i in result.data) {
                    let name = result.data[i].name;
                    let mrt = result.data[i].mrt;
                    let cat = result.data[i].category;
                    let img = result.data[i].images[0]
                    listName.push(name);
                    listMrt.push(mrt);
                    listCat.push(cat);
                    listImg.push(img);
                }
            }
            showData(listName, listMrt, listCat, listImg);
        })
}


// 新增照片資料到網頁
let i = 0;
const showData = (listN, listM, listC, listI) => {
    for (let count = 0; count < listN.length; count++) {
        let divBox = document.createElement("div");
        let divName = document.createElement("div");
        let divMrt = document.createElement("div");
        let divCat = document.createElement("div");
        let img = document.createElement("img");
        let nameText = document.createTextNode(listN[count]);
        let mrtText = document.createTextNode(listM[count]);
        let catText = document.createTextNode(listC[count]);
        divBox.id = "box" + i;
        divName.id = "name" + i;
        divMrt.id = "mrt" + i;
        divCat.id = "category" + i;
        img.src = listI[count];
        divName.appendChild(nameText);
        divMrt.appendChild(mrtText);
        divCat.appendChild(catText);
        document.getElementsByClassName("content")[0].appendChild(divBox);
        document.getElementById("box" + i).appendChild(img);
        document.getElementById("box" + i).appendChild(divName);
        document.getElementById("box" + i).appendChild(divMrt);
        document.getElementById("box" + i).appendChild(divCat);
        i++;
    }
}


// 自動載入後續頁面的功能
let options = { rootMargin: '20px', threshold: 0, }; // 觸發條件

// 觸發條件後的回呼函式
let callback = (entry) => {
    if (entry[0].isIntersecting) {
        console.log("CALLBACK OK")
        keyword = document.getElementById("keyword").value;
        if (keyword) {
            if (page != null) {
                fetchData();
                console.log("Page: " + page);
            } else {
                observer.unobserve(target);
            }
        } else {
            if (page != null) {
                fetchData();
                console.log("Page: " + page);
            } else {
                observer.unobserve(target);
            }
        }
    }
};

// 建立 IntersectionObserver物件
let observer = new IntersectionObserver(callback, options);
const target = document.querySelector("#end"); // observer的target
observer.observe(target); // 開啟觀察目標


// 關鍵字搜尋功能
const searchKeyword = () => {
    document.getElementById("content").innerHTML = "";
    console.log("KW" + page);
    page = 0;
    keyword = document.getElementById("keyword").value;
    src = "http://127.0.0.1:3000/api/attractions?page=" + page + "&keyword=" + keyword;
    fetch(src)
        .then(function(response) {
            return response.json();
        })
        .then(function(result) {
            if (result.error) { // 先確認有無此資料
                console.log("查無此景點")
                observer.unobserve(target); // 沒有資料的話記得要關閉observer，不然之後很難再打開
                div = document.createElement('div');
                div.id = "errMsg";
                txt = document.createTextNode("查無此景點");
                div.appendChild(txt);
                document.getElementById("content").appendChild(div);
            } else {
                observer.observe(target); // 找得到資料就開啟觀察目標
            }
        })
}