document.addEventListener("DOMContentLoaded", () => {
    let burgermenu=document.querySelector(".burger-menu");
    let popupmenu=document.querySelector(".popup-menu");
    burgermenu.addEventListener('click',()=>{
        popupmenu.classList.toggle('active');
    });

    let closeicon=document.querySelector(".close-icon")
    closeicon.addEventListener('click',()=>{
        popupmenu.classList.remove('active');
    });

    const apiUrl = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
    const promotionsContainer = document.querySelector(".Promotions");
    const titlesContainer = document.querySelector(".Titles");
    const loadMoreButton = document.querySelector(".load-more");

    let spots = [];
    let loadedSpots=0;

    //取得資料並處理
    fetch(apiUrl).then(response=>response.json())
    .then(data=>{
        spots = data.data.results;
        renderInitialContent();
    })
    .catch(error => console.error("Error fetching data:", error));
    
    //插入圖片內容
    function renderInitialContent(){
        if(spots && spots.length>0){
            spots.slice(0,3).forEach(spot=>{
                const spotName = spot.stitle;
                const imageUrl = getFirstImgUrl(spot.filelist);
                addSpotToContainer(promotionsContainer,"promotion",spotName,imageUrl);
            });

            spots.slice(3, 13).forEach(spot => {  // 顯示 10 個 title
                const spotName = spot.stitle;
                const imageUrl = getFirstImgUrl(spot.filelist);
                addSpotToContainer(titlesContainer, "title", spotName, imageUrl);
            });
            
            currentIndex = 13;
            loadMoreButton.style.display="block";
        }
    }

    loadMoreButton.addEventListener("click",()=>{
        loadMoreContent(10);
    });

    function loadMoreContent(count) {
        const nextBatch = spots.slice(currentIndex, currentIndex + count);
        nextBatch.forEach(spot => {
            const spotName = spot.stitle;
            const imageUrl = getFirstImgUrl(spot.filelist); // 使用 filelist 抓取圖片
            addSpotToContainer(titlesContainer, "title", spotName, imageUrl);
        });
    
        currentIndex += count;
    
        if (currentIndex >= spots.length) {
            loadMoreButton.style.display = "none"; // 隱藏 load more 按鈕
        }
    }
    

    function getFirstImgUrl(filelist) {
       
        if (!filelist || filelist.length === 0) {
            return "./image.jpg"; 
        }

        if (typeof filelist === "string") {
            filelist = filelist.split(" "); 
        }

        if (Array.isArray(filelist)) {
          
            const regex = /https?:\/\/[^\s]+?\.(?:jpg|jpeg|png|JPG|PNG|JPEG)/g;
            const matchedUrls = filelist.join(" ").match(regex); 

            if (matchedUrls && matchedUrls.length > 0) {
                return matchedUrls[0]; 
            } else {
                return "./image.jpg"; 
            }
        } else {
            return "./image.jpg"; 
        }
    }
    
    
    

    function addSpotToContainer(container, className, spotName, imageUrl){
        const card= document.createElement("div");
        card.classList.add(className);
    
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = spotName;
        
        const spotNameElement = document.createElement("p");
        spotNameElement.textContent = spotName
    
        card.appendChild(img);
        card.appendChild(spotNameElement);
        container.appendChild(card);
    }
});

