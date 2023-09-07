let nextPageNum = 0;
let currentKeyword = "";

async function getMrtsList(){
    url="/api/mrts"
    try{
        const response = await fetch(url);
        const mrts = await response.json();
        return mrts.data
    }catch(e){
        console.log(e)
    }
    
}
async function getAttractionsbyPage(pageNumber,keyword){
    url = `/api/attractions?page=${pageNumber}&keyword=${keyword}`;
    try{
        const response = await fetch(url);
        const attractions = await response.json();
        return attractions
    }
    catch(e){
        console.log(e)
    }
}

async function addAttractionCards(pageNum,keyword){
    const attractionsListContainer = document.getElementById("attractions_list_container")
    const fetchedData = await getAttractionsbyPage(pageNum,keyword)
    const attractionsData = fetchedData.data
    const nextPage = fetchedData.nextPage

    if (attractionsData.length == 0){
        const errorMessageContainer = document.createElement("div");
        errorMessageContainer.className = "attraction__message";
        const errorMessage = document.createElement("p");
        errorMessage.className = "attraction__error";
        errorMessage.innerText = "查無資料"
        errorMessageContainer.appendChild(errorMessage)
        attractionsListContainer.appendChild(errorMessageContainer)
    }else{
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
    nextPageNum = nextPage
    currentKeyword = keyword
}
async function createMrtsList(){
    const mrtsListWrapper = document.getElementById("mrts_list_wrapper");
    const mrtData = await getMrtsList();
    const searchInput = document.getElementById("search_input")
    mrtData.forEach(mrt => {
        const mrt_link = document.createElement("a")
        mrt_link.addEventListener("click",()=>{
            searchInput.value = mrt
            // serch by mrt name
            searchByKeyword()
        })
        mrt_link.className = "mrts-list__link"
        mrt_link.innerText = mrt
        mrtsListWrapper.appendChild(mrt_link)
    });
}

function firstLoad(){
    const attractionsListContainer = document.getElementById("attractions_list_container");
    attractionsListContainer.textContent = "";
    addAttractionCards(0,"")
    .then(()=>{
        buildObserve(observer)
    })
    .catch((e)=>{
        console.log(e)
    })
    
}

function searchByKeyword(){
    const attractionsListContainer = document.getElementById("attractions_list_container");
    const key = document.getElementById("search_input").value;
    attractionsListContainer.textContent = "";
    addAttractionCards(0,key)
    .then(()=>{
        buildObserve(observer)
    })
    .catch((e)=>{
        console.log(e)
    })
}

const callback = (entries)=>{
    if(entries[0].isIntersecting && Math.floor(entries[0].intersectionRatio) === 1){
        observer.disconnect();
        if (nextPageNum) {
            observer.unobserve(entries[0].target)
            addAttractionCards(nextPageNum,currentKeyword)
            .then(()=>{
                const cards = document.getElementById("attractions_list_container").children
                const target = cards.item(cards.length-1)
                observer.observe(target);
            })
            .catch((e)=>{console.log(e)})
        }
    }
}
const observer = new IntersectionObserver(callback,{ threshold: 1.0 });

const buildObserve = (_observer)=>{
    const cards = document.getElementById("attractions_list_container").children
    const count = document.getElementById("attractions_list_container").childElementCount
    const target = cards.item(count-1)
    _observer.observe(target)
}

function moveRight(){
    const container = document.getElementById("mrts_list_wrapper");
    const width = container.offsetWidth - 50;
    container.scrollLeft += width;
}

function moveLeft(){
    const container = document.getElementById("mrts_list_wrapper");
    const width = container.offsetWidth - 50;
    container.scrollLeft -= width;
}

createMrtsList()
firstLoad()