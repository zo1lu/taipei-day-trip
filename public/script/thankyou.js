import { authenticateLogin } from "./auth.js";

async function requestOrderDetail(orderNumber){
    let token = localStorage.getItem("token")
    let url = `/api/order/${orderNumber}`;
    const head = {
        "Authorization":`Bearer ${token}`
    }
    let result = await fetch(url, {headers:head})
    return result
}

async function getOrderDetail(){
    const queryParams = new URLSearchParams(window.location.search);
    let orderNumber = queryParams.get('number');
    let response = await requestOrderDetail(orderNumber);
    let returnData = response.json();
    return returnData
}

async function renderOrderDetail(){
    let authenticatedUser = await authenticateLogin()
    if (authenticatedUser){
        let returnData = await getOrderDetail();
        let data = returnData["data"]
        if(data){
            const tripsContainer = document.getElementById("trips_container");
            const tripsData = data["trip"];
            document.getElementById("order_number").innerText = data["order_number"];
            document.getElementById("order_date").innerText = data["created_time"];
            document.getElementById("order_price").innerText = `$${data["price"]} NTD`;
            document.getElementById("order_status").innerText = data["status"]?"已付款":"未付款";
            const contact = JSON.parse(data["contact"])
            document.getElementById("contact_name").innerText = contact["name"];
            document.getElementById("contact_email").innerText = contact["email"];
            document.getElementById("contact_phone").innerText = contact["phone"];
            tripsData.forEach(site => {
                const tripContainer = document.createElement('div')
                tripContainer.className = "trip-container"
                const tripImg = document.createElement('img')
                tripImg.className = "trip__image"
                tripImg.src = site["image"]
                const tripInfoContainer = document.createElement("div")
                tripInfoContainer.className = "trip__info-container"
                const tripSiteInfo = document.createElement("div")
                tripSiteInfo.className = "trip__site-info"
                const tripName = document.createElement("p")
                const tripAddress = document.createElement("p")
                tripName.className = "trip__name"
                tripAddress.className = "trip__address" 
                tripName.innerText = site["name"]
                tripAddress.innerText = site["address"]
                tripSiteInfo.appendChild(tripName)
                tripSiteInfo.appendChild(tripAddress)
                const tripDate = document.createElement("p")
                const tripTime = document.createElement("p")
                const tripPrice = document.createElement("p")
                tripDate.className = "trip__content"
                tripTime.className = "trip__content"
                tripPrice.className = "trip__content"
                tripDate.innerText = site["date"]
                let startTime = site["time"].split(",")[0]
                let endTime = site["time"].split(",")[1]
                tripTime.innerText = `${startTime}:00-${endTime}:00`
                tripPrice.innerText =  `$${site["price"]} NTD`
                tripInfoContainer.appendChild(tripSiteInfo)
                tripInfoContainer.appendChild(tripDate)
                tripInfoContainer.appendChild(tripTime)
                tripInfoContainer.appendChild(tripPrice)
                tripContainer.appendChild(tripImg)
                tripContainer.appendChild(tripInfoContainer)
                tripsContainer.appendChild(tripContainer)

            });
        }else{
            window.location.href = "/"
        }    
    }else{
        window.location.href = "/"
    }
    
}

renderOrderDetail();