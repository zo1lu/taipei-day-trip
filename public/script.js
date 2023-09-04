async function getMrtsList(){
    url="http://127.0.0.1:3000/api/mrts"
    try{
        const response = await fetch(url);
        const mrts = await response.json();
        console.log(mrts.data)
        return mrts.data
    }catch(e){
        console.log(e)
    }
    
}
async function getAttractionsbyPage(pageNumber,keyword){
    url = `http://127.0.0.1:3000/api/attractions?page=${pageNumber}&keyword=${keyword}`;
    try{
        const response = await fetch(url);
        const attractions = await response.json();
        console.log(attractions.data)
        return attractions.data
    }
    catch(e){
        console.log(e)
    }
    
}

// getAttractionsbyPage(0)
// getMrtsList()

async function createAttractionsList(){
    const attractionsListContainer = document.getElementById("attractions_list_container")
    const attractionsData = await getAttractionsbyPage(0,"")
    attractionsData.forEach(attraction=>{
        const imageUrl = attraction.images[0].replace(/["]/g, '');
        const attractionCard = document.createElement("div");
        attractionCard.className = "attraction__card";
        const attractionLink = document.createElement("a");
        attractionLink.className = "attraction__link";
        attractionLink.style.cssText = `background-image:url(${imageUrl})`;
        const attractionName = document.createElement("p");
        attractionName.className = "attraction__name";
        attractionName.innerText = attraction.name;
        attractionLink.appendChild(attractionName);

        const attractionInfo = document.createElement("div");
        attractionInfo.className = "attraction__info";

        const attractionMrt = document.createElement("p");
        attractionMrt.className = "attraction__mrt";
        attractionMrt.innerText = attraction.mrt || ""

        const attractionCategory = document.createElement("p");
        attractionCategory.className = "attraction__category";
        attractionCategory.innerText = attraction.category;

        attractionInfo.appendChild(attractionMrt);
        attractionInfo.appendChild(attractionCategory);
        attractionCard.appendChild(attractionLink);
        attractionCard.appendChild(attractionInfo);
        attractionsListContainer.appendChild(attractionCard);

    })

}
async function createMrtsList(){
    const mrtsListWrapper = document.getElementById("mrts_list_wrapper");
    const mrtData = await getMrtsList();
    const searchInput = document.getElementById("search_input")
    mrtData.forEach(mrt => {
        const mrt_link = document.createElement("a")
        mrt_link.addEventListener("click",()=>{
            searchInput.setAttribute("value",mrt)
            // serchbymrtname
        })
        mrt_link.className = "mrts-list__link"
        mrt_link.innerText = mrt
        mrtsListWrapper.appendChild(mrt_link)
    });
}
createMrtsList()
createAttractionsList()

function moveRight(){
    const container = document.getElementById("mrts_list_wrapper");
    const width = container.offsetWidth - 50;
    container.scrollLeft+=width;
}

function moveLeft(){
    const container = document.getElementById("mrts_list_wrapper");
    const width = container.offsetWidth - 50;
    container.scrollLeft-=width;
}