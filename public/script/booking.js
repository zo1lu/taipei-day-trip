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

window.deleteBookingTour = deleteBookingTour;

showBookingList();