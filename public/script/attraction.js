import { authenticateLogin, switchPopupDisplay } from "./auth.js";
let imageIndex = 0
const id = window.location.pathname.split("/")[2]

function setTourPrice(){
    const firstHalfDay = document.getElementById("radio_first_half_of_day");
    const tourPrice = document.getElementById("tour_price");
    if (firstHalfDay.checked){
        tourPrice.innerText = "新台幣 2000 元";
    }else{
        tourPrice.innerText = "新台幣 2500 元";
    }
}

async function getAttractionDataById(id){
    let url = `/api/attraction/${id}`
    try{
        const response = await fetch(url);
        const attractionData = await response.json();
        return attractionData["data"]
    }
    catch(e){
        console.log(e)
    }
}

async function bookTour(){
    let authenticated = await authenticateLogin();
    if (authenticated){
        const attractionId = id;
        const tourName = document.getElementById("attraction_name").innerText
        const date = document.getElementById("tour_date").value;
        const timeRadios = document.getElementsByName('time');
        const timeRadiosArray = [...timeRadios];
        const time = timeRadiosArray.filter(radio=>radio.checked)[0].value;
        const priceText = document.getElementById("tour_price").innerText;
        const price = priceText.split(" ")[1];
        if (date && time){
            //request create booking
            const startTime = time.split(",")[0]
            const endTime = time.split(",")[1]
            const confirmMessage = `${tourName}\n日期：${date}\n時間：${startTime}:00 - ${endTime}:00\n價錢：新台幣${price}元\n確認預約以上行程嗎?`
            if(confirm(confirmMessage)){
                let result = await requestCreateBooking(attractionId, date, time, price)
                if (result["ok"]){
                    window.location.href = '/booking'
                }
            }
        }else{
            alert("Please select tour date!")
            return 
        }
    }else{
        switchPopupDisplay(false)
    }
}

async function requestCreateBooking(attractionId, date, time, price){
    try{
        let url = "/api/booking"
        let token = localStorage.getItem("token")
        const body = {
            "attractionId": attractionId,
            "date": date,
            "time": time,
            "price": price
        };
        const head = {
            "Authorization":`Bearer ${token}`,
            "Content-Type":"application/json"
        };
        let result = await fetch(url,{method: "POST", body: JSON.stringify(body), headers: head})
        let data = result.json()
        return data
    }catch(e){
        console.error(e)
        return false
    }
}

async function addAttractionData(id){
    const data = await getAttractionDataById(id);
    const imagesWrapper = document.getElementById("attraction_images_wrapper");
    const dotsContainer = document.getElementById("dots_container");

    const name = document.getElementById("attraction_name");
    const location = document.getElementById("attraction_location");
    const description = document.getElementById("attraction_description");
    const address = document.getElementById("attraction_address");
    const direction = document.getElementById("attraction_direction");

    data["images"].forEach((imgUrl,index)=>{
        const imageContainer = document.createElement("div");
        imageContainer.className = "attraction-intro__image-container";
        const img = document.createElement("img");
        img.setAttribute("src",imgUrl);
        img.setAttribute("alt",`Image#${index}`);
        img.id = `img#${index+1}`
        imageContainer.appendChild(img);
        imagesWrapper.appendChild(imageContainer);
        const dot = document.createElement("a");
        dot.className="attraction-intro__dot";
        dot.onclick = function(){showSlide(index)};
        dotsContainer.appendChild(dot);
    });
    name.innerText = data["name"];
    location.innerText = `${data["category"]} at ${data["mrt"] || ""}`;
    description.innerText = data["description"] || "";
    address.innerText = data["address"] || "";
    direction.innerText = data["transport"] || "";

}
function showSlide(imageIndex){
    let images = Array.from(document.getElementsByClassName("attraction-intro__image-container"));
    let dots = Array.from(document.getElementsByClassName("attraction-intro__dot"))
    images.forEach(img=>{
        images.indexOf(img)==imageIndex?img.style.display="block":img.style.display="none"
    });
    dots.forEach((dot)=>{
        dots.indexOf(dot)==imageIndex?dot.classList.add("dot--active"):dot.className="attraction-intro__dot"
    })
} 

function plusSlide(n){
    let images = Array.from(document.getElementsByClassName("attraction-intro__image-container"));
    let length = images.length;
    if (imageIndex + n >= length){
        imageIndex = 0
    }else if(imageIndex + n < 0){
        imageIndex = length-1
    }else{
        imageIndex+=n;
    }
    showSlide(imageIndex);
}

window.plusSlide = plusSlide;
window.setTourPrice = setTourPrice;
window.bookTour = bookTour;

window.onload = function(){
    //hide the preloader
    document.querySelector(".preload").style.display = "none";
}

addAttractionData(id)
.then(()=>{
    showSlide(imageIndex);
})
.catch((e)=>{console.log(e)})