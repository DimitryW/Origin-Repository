// 切換費用金額
const inputFunc = () => {
    let value = document.querySelector('input[name="time"]:checked').value;
    switch (value) {
        case "morning":
            document.getElementById("fee").innerHTML = "新台幣 2000 元"
            break;
        case "afternoon":
            document.getElementById("fee").innerHTML = "新台幣 2500 元"
            break;
    }
}
inputFunc();


// 取得景點ID並渲染頁面
let path = window.location.pathname;
let id = path.split("/")[2];
// let src = "http://127.0.0.1:3000/api/attraction/" + id;
let src = "http://3.230.236.135:3000/api/attraction/" + id;

const inputAttributes = {
    name: "switch-button",
    type: "radio",
    class: "data-switch-input-btn"
}

function addAttributes(element, attributes) {
    Object.keys(attributes).forEach(attr => {
        element.setAttribute(attr, attributes[attr]);
    });
}

const loadAttraction = () => {
    fetch(src)
        .then((response) => {
            return response.json();
        })
        .then((result) => {
            document.getElementById("name").innerHTML = result.data.name;
            document.getElementById("cat").innerHTML = result.data.category;
            document.getElementById("mrt").innerHTML = result.data.mrt;
            // document.getElementById("img").src = result.data.images[0];
            document.getElementById("desc").innerHTML = result.data.description;
            document.getElementById("add").innerHTML = result.data.address;
            document.getElementById("trans").innerHTML = result.data.transport;
            let imgList = result.data.images;
            for (let i = 0; i < imgList.length; i++) {
                let input = document.createElement("input");
                let li = document.createElement("li");
                let img = document.createElement("img");
                addAttributes(input, inputAttributes);
                li.setAttribute("class", "slide");
                img.src = imgList[i];
                document.getElementsByClassName("data-switch-input")[0].appendChild(input);
                li.appendChild(img);
                document.getElementById("slide-list").appendChild(li);
            }
            document.getElementsByClassName("data-switch-input-btn")[0].checked = true;
            document.getElementsByClassName("slide")[0].dataset.active = true;
            inputBtn = document.querySelectorAll(".data-switch-input-btn")
                // console.log(inputBtn = document.querySelectorAll(".data-switch-input-btn"))

        });
}


// 左右按鈕輪播功能
const buttons = document.querySelectorAll("[data-carousel-button]")
console.log(document.querySelectorAll("[data-carousel-button]"))
buttons.forEach(button => {
    button.addEventListener("click", () => {
        let offset = button.dataset.carouselButton === "next" ? 1 : -1
            // 條件 (三元) 運算子  // dataset.carouselButton等於data-carousel-button
        let slides = document.querySelector("[data-slides]")
            // const slides = button.closest("[data-carousel]").querySelector("[data-slides]")
        let activeSlide = document.querySelector("[data-active]")
        let newIndex = [...slides.children].indexOf(activeSlide) + offset
        if (newIndex < 0) newIndex = slides.children.length - 1
        if (newIndex >= slides.children.length) newIndex = 0
        delete activeSlide.dataset.active
        slides.children[newIndex].dataset.active = true

        let inputBtn = document.querySelectorAll("input")
        let checkedInput = document.querySelector("[checked=checked]")
        inputBtn[newIndex].checked = true
            // checkedInput.checked = false

    })
})

// 下方園點輪播功能
window.onclick = e => {
    console.log(e.target); // to get the element
    let index = [...inputBtn].indexOf(document.querySelector([".data-switch-input-btn:checked"]))
    let activeSlide = document.querySelector("[data-active]")
    let slides = document.querySelector("[data-slides]")
    delete activeSlide.dataset.active
    slides.children[index].dataset.active = true
}