import { authenticateLogin } from "./auth.js";

async function showBookingList(){
    let authenticatedUser = await authenticateLogin()
    if (authenticatedUser){
        let data = await requestBookingList()
        let result = data["data"]
        const userName = document.getElementById("user_name")
        userName.innerText = authenticatedUser["name"]
        const bookInfo = document.getElementById("booking_info")
        let totalCost = 0
        if (result.length > 0){
            bookInfo.style.display = "flex";
            const bookList = document.getElementById("booking_list")
            result.forEach((book)=>{
                totalCost+= parseInt(book["price"])
                const listItem = document.createElement("div");
                listItem.className = "list-item"
                //img
                const itemImg = document.createElement("div");
                itemImg.className = "item__img";
                const img = document.createElement("img");
                img.src = book["attraction"]["image"];
                img.alt = book["attraction"]["name"];
                itemImg.appendChild(img)
                //info
                const infoContainer = document.createElement("div")
                infoContainer.className = "item__info-container"
                const deleteBtn = document.createElement("img")
                deleteBtn.className = "item__delete"
                deleteBtn.src = "/icon/icon-delete.png"
                deleteBtn.setAttribute("onclick",`deleteBookingTour(${book["id"]})`)
                const itemTitle = document.createElement("p")
                itemTitle.className = "item__title"
                itemTitle.innerText = `台北一日遊：${book["attraction"]["name"]}`
                const itemDate = document.createElement("p")
                const itemTime = document.createElement("p")
                const itemPrice = document.createElement("p")
                const itemLocation = document.createElement("p")
                itemDate.className = "item__info"
                itemTime.className = "item__info"
                itemPrice.className = "item__info"
                itemLocation.className = "item__info"
                const timeStart = book["time"].split(",")[0]
                const timeEnd = book["time"].split(",")[1]
                itemDate.innerText = `日期： ${book["date"]}`
                itemTime.innerText = `時間： ${timeStart}:00 - ${timeEnd}:00`
                itemPrice.innerText = `費用： 新台幣${book["price"]}元`
                itemLocation.innerText = `地點： ${book["attraction"]["address"]}`
                infoContainer.appendChild(deleteBtn)
                infoContainer.appendChild(itemTitle)
                infoContainer.appendChild(itemDate)
                infoContainer.appendChild(itemTime)
                infoContainer.appendChild(itemPrice)
                infoContainer.appendChild(itemLocation)
                //combine together
                listItem.appendChild(itemImg)
                listItem.appendChild(infoContainer)
                bookList.appendChild(listItem)
            })
        const totalFee = document.getElementById("total_fee")    
        totalFee.innerText = `${totalCost}`
        }else{
            const noBookMessage = document.getElementById("no_book_message")
            noBookMessage.style.display = "block"
            bookInfo.style.display = "none"
        }
    }else{
        window.location.href = "/"
    }
}

async function requestBookingList(){
    try{
        let url = "/api/booking"
        let token = localStorage.getItem("token")
        const head = {
            "Authorization":`Bearer ${token}`,
        }
        let result = await fetch(url, {method:"GET", headers:head})
        let data = result.json()
        return data
    }catch(e){
        console.error(e)
        return false
    }
}

async function requestBookingDelete(bookingId){
    try{
        let url = "/api/booking"
        let token = localStorage.getItem("token")
        const head = {
            "Authorization":`Bearer ${token}`,
            "Content-Type":"application/json"
        }
        const body = {
            "bookingId":bookingId,
        }
        let result = await fetch(url, {method:"DELETE", headers:head, body: JSON.stringify(body)})
        let data = result.json()
        return data
    }catch(e){
        console.error(e)
        return false
    }
    
}

async function deleteBookingTour(bookingId){
    if (confirm("確定刪除嗎?")){
        let result = await requestBookingDelete(bookingId)
        if (result["ok"]){
            location.reload();
        }else{
            alert("刪除失敗，再試一次");
        }
    }
}

//payment 
TPDirect.card.onUpdate(function(update){
    const submitButton = document.getElementById("submit_btn");
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitButton.removeAttribute('disabled')
        submitButton.classList.remove("disabled")
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
        submitButton.classList.add("disabled")
    }

    // number 欄位是錯誤的
    const cardNumber = document.getElementById("card-number");
    const cardExpiration = document.getElementById("card-expiration-date");
    const cardCcv = document.getElementById("card-ccv");
    if (update.status.number === 2) {
        cardNumber.style.borderColor = "red"
    } else if (update.status.number === 0) {
        cardNumber.style.borderColor = "green"
    } else {
        cardNumber.style.borderColor = "gray"
    }
    
    if (update.status.expiry === 2) {
        cardExpiration.style.borderColor = "red"
    } else if (update.status.expiry === 0) {
        cardExpiration.style.borderColor = "green"
    } else {
        cardExpiration.style.borderColor = "gray"
    }
    
    if (update.status.ccv === 2) {
        cardCcv.style.borderColor = "red"
    } else if (update.status.ccv === 0) {
        cardCcv.style.borderColor = "green"
    } else {
        cardCcv.style.borderColor = "gray"
    }
})

function setUpCardField(){
    let fields = {
        number: {
            // css selector
            element: document.getElementById('card-number'),
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            // DOM object
            element: document.getElementById('card-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: document.getElementById('card-ccv'),
            placeholder: '後三碼'
        }
    }
    TPDirect.card.setup({
        fields: fields,
        styles: {
            // Style all elements
            'input': {
                'color': 'black'
            },
            // Styling ccv field
            'input.ccv': {
                'font-size': '16px'
            },
            // Styling expiration-date field
            'input.expiration-date': {
                'font-size': '16px'
            },
            // Styling card-number field
            'input.card-number': {
                'font-size': '16px'
            },
            // style focus state
            ':focus': {
                'color': 'black'
            },
            // style valid state
            '.valid': {
                'color': 'green'
            },
            // style invalid state
            '.invalid': {
                'color': 'red'
            },
        },
        // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
        isMaskCreditCardNumber: true,
        maskCreditCardNumberRange: {
            beginIndex: 6, 
            endIndex: 11
        }
    })
}

function submitPayment(event) {
    event.preventDefault()
    if(isContactInfoNull()){
        alert("請填寫完整聯絡人姓名、電子信箱、連絡電話")
        return 
    }
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('付款資料錯誤，請重新填寫')
        return
    }
    // Get prime
    TPDirect.card.getPrime(async (result) => {
        if (result.status !== 0) {
            alert('發生錯誤' + result.msg)
            return
        }
        transactionAnimationToggle(true);
        let prime = result.card.prime;
        let responseData = await requestOrdering(prime);
        let resultData = responseData.json();
        resultData
        .then((data)=>dealOrderingResponse(data))
        .catch(e=>console.error(e))
    })
}

function transactionAnimationToggle(show){
    const transactionAnimation = document.getElementById("transaction_animation");
    transactionAnimation.style.display = show?"flex":"none";
}

async function requestOrdering(prime){
    let token = localStorage.getItem("token")
    let url = "/api/orders"
    let totalPrice = document.getElementById("total_fee").innerText
    let name = document.getElementById("contact_name").value
    let email = document.getElementById("contact_email").value
    let phone = document.getElementById("contact_phone").value
    const head = {
        "Authorization":`Bearer ${token}`,
        "Content-Type":"application/json"
    }
    const body = {
        "prime":prime,
        "total_price":totalPrice,
        "contact":{
            "name":name,
            "email":email,
            "phone":phone
        }
    }
    let response = await fetch(url, {method:"POST", headers:head, body:JSON.stringify(body)})
    return response
}

function dealOrderingResponse(result){
    if (result["data"]){
        setTimeout(()=>{
            window.location.href =`/thankyou?number=${result["data"]["number"]}`
        },3000)
    }else{
        transactionAnimationToggle(false);
        alert("發生錯誤，請再次嘗試")
    }
}

function isContactInfoNull(){
    const contactName = document.getElementById("contact_name").value
    const contactEmail = document.getElementById("contact_email").value
    const contactPhone = document.getElementById("contact_phone").value
    if (contactName==""||contactEmail==""||contactPhone==""){
        return true
    }
    return false
}

window.deleteBookingTour = deleteBookingTour;
window.submitPayment = submitPayment;

showBookingList();
setUpCardField();

////////////////////////////////////////////////////////////////////////////////////////////////
// Develope Queue
// function isEmailValid(){}
// function isPhoneValid(){}


////////////////////////////////////////////////////////////////////////////////////////////////
// For testing
// function setTestingData(){
//     document.getElementById("contact_name").value ="tester"
//     document.getElementById("contact_email").value = "test@gmail.com"
//     document.getElementById("contact_phone").value = "0912345678"
// }
// setTestingData();