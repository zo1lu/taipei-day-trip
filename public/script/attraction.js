let imageIndex = 0

function setTourPrice(){
    const firstHalfDay = document.getElementById("radio_first_half_of_day");
    const tourPrice = document.getElementById("text_tour_price");
    if (firstHalfDay.checked){
        tourPrice.innerText = "新台幣 2000 元";
    }else{
        tourPrice.innerText = "新台幣 2500 元";
    }
}

async function getAttractionDataById(id){
    url = `/api/attraction/${id}`
    try{
        const response = await fetch(url);
        const attractionData = await response.json();
        console.log(attractionData)
        return attractionData["data"]
    }
    catch(e){
        console.log(e)
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

const id = window.location.pathname.split("/")[2]

addAttractionData(id)
.then(()=>{
    showSlide(imageIndex)
})
.catch((e)=>{console.log(e)})