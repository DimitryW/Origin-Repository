const thankySrc = "http://54.86.13.161:3000";
// const thankySrc = "http://127.0.0.1:3000";

async function thankyou() {
    let urlParam = new URLSearchParams(window.location.search)
    let order_no = urlParam.get("number")

    if (order_no) {
        let res = await fetch("/api/order/" + order_no);
        let data = await res.json();
        let number = data["data"]["number"];
        // let date = data["data"]["trip"]["date"];
        // let time = data["data"]["trip"]["time"] === "morning" ? "早上9點到中午12點" : "下午1點到下午5點";
        // let price = data["data"]["price"];
        // let address = data["data"]["trip"]["attraction"]["address"];
        // let name = data["data"]["contact"]["name"];
        // let email = data["data"]["contact"]["email"];
        // let phone = data["data"]["contact"]["phone"];
        document.getElementById("order-no").innerHTML = number;
        // document.getElementById("book-date").innerHTML = date;
        // document.getElementById("book-time").innerHTML = time;
        // document.getElementById("book-charge").innerHTML = price;
        // document.getElementById("book-address").innerHTML = address;
        // document.getElementById("book-name").innerHTML = name;
        // document.getElementById("book-email").innerHTML = email;
        // document.getElementById("book-phone").innerHTML = phone;
    } else {
        location.href = "/";
    }

}