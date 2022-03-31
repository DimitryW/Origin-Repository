const bookingSrc = "http://3.230.236.135:3000/api/booking";
// const bookingSrc = "http://127.0.0.1:3000/api/booking";
const bookingHeaders = { "Content-type": "application/json" };

// 開始預訂行程
async function createBooking() {
    if (!document.cookie.includes("wehelp_user")) {
        signinWindow();
        return
    }
    let date = document.getElementById("date").value;
    if (!date) {
        document.getElementById("error-message").innerHTML = "請選擇日期";
        // return
    }
    let attractionId = window.location.pathname.split("/")[2];
    let time = document.querySelector("input[name='time']:checked").value;
    let price = document.querySelector("input[name='time']:checked").value === "morning" ? 2000 : 2500;
    let requestBody = {
        "attractionId": attractionId,
        "date": date,
        "time": time,
        "price": price
    };
    try {
        let response = await fetch(bookingSrc, {
            method: "POST",
            headers: bookingHeaders,
            body: JSON.stringify(requestBody)
        });
        let result = await response.json();
        if (result["ok"]) {
            location.href = "http://3.230.236.135:3000/booking";
            // location.href = "http://127.0.0.1:3000/booking";
        }
    } catch (error) {
        console.log(error);
    }

}

// 取得預定行程資訊
async function checkBooking() {
    if (!document.cookie.includes("wehelp_user")) {
        location.href = "http://3.230.236.135:3000";
        // location.href = "http://127.0.0.1:3000";
        return
    }
    try {
        let memberResponse = await fetch(memberSrc, {
            method: "GET",
            headers: headers
        });
        let memberResult = await memberResponse.json();
        membername = memberResult["data"]["name"];
    } catch (error) {
        console.log(error);
    }
    if (!document.cookie.includes("wehelp_booking")) {
        document.getElementById("booking-content").style.display = "none";
        document.getElementById("booking-greeting").innerHTML = "您好，" + membername + "，待預訂的行程如下："
        document.getElementById("nobooking").style.display = "block";
        document.getElementById("booking-footer").style.height = "680px";
        document.getElementById("page-wrapper").style.paddingBottom = 0;
        document.getElementById("booking-footer").style.position = "relative";
        return
    }
    try {
        let response = await fetch(bookingSrc, {
            method: "GET",
            headers: bookingHeaders
        });
        console.log(111)
        let result = await response.json();
        console.log(112)
        if (!result["error"]) {
            document.getElementById("booking-content").style.display = "block"; // display is not an attribute - it's a CSS property. You need to access the style object
            document.getElementById("booking-greeting").innerHTML = "您好，" + membername + "，待預訂的行程如下："
            document.getElementById("booking-info-img").src = result["data"]["attraction"]["image"];
            let name = result["data"]["attraction"]["name"];
            let bookingDate = result["data"]["date"];
            let bookingTime = result["data"]["time"] === "morning" ? "早上9點到中午12點" : "下午1點到下午5點";
            let bookingPrice = result["data"]["price"];
            let bookingAddress = result["data"]["attraction"]["address"];
            document.getElementById("attractName").innerHTML = name;
            document.getElementById("book-date").innerHTML = bookingDate
            document.getElementById("book-time").innerHTML = bookingTime
            document.getElementById("book-charge").innerHTML = "新台幣 " + bookingPrice + " 元";
            document.getElementById("book-address").innerHTML = bookingAddress
            return
        }
        if (result["error"]) {
            document.getElementById("booking-greeting").innerHTML = "您好，" + membername + "，待預訂的行程如下："
            document.getElementById("nobooking").style.display = "block";
            document.getElementById("booking-footer").style.height = "680px";
            document.getElementById("page-wrapper").style.paddingBottom = 0;
            document.getElementById("booking-footer").style.position = "relative";
        }

    } catch (error) {
        console.log(error);
    }
}

// 刪除行程
async function deleteBooking() {
    try {
        let response = await fetch(bookingSrc, {
            method: "DELETE",
            headers: bookingHeaders
        });
        let result = await response.json();
        if (result["ok"]) {
            document.getElementById("booking-content").style.display = "none";
            document.getElementById("booking-greeting").innerHTML = "您好，" + membername + "，待預訂的行程如下："
            document.getElementById("nobooking").style.display = "block";
            document.getElementById("booking-footer").style.height = "680px";
            document.getElementById("page-wrapper").style.paddingBottom = 0;
            document.getElementById("booking-footer").style.position = "relative";
        }
    } catch (error) {
        console.log(error);
    }
}