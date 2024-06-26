
const eatery_name = document.getElementById("eatery_name");
const show_location = document.getElementById("show_location");
const eatery_real_location = document.getElementById("eatery_real_location");
const eatery_type = document.getElementById("eatery_type");
const user_image = document.getElementById("user_image");
const comment = document.getElementById("comment");
const group_location = document.getElementById("group_location");

const copy_eatery_name = document.getElementById("copy_eatery_name");
const copy_show_location = document.getElementById("copy_show_location");
const copy_eatery_type = document.getElementById("copy_eatery_type");
const show_image = document.getElementById("show_image");

const crawl_image_title = document.getElementById("crawl_image_title");
const btn_image = document.getElementById("btn_image");
const crawl_image = document.getElementById("crawl_image");
const crawl_image_error  = document.getElementById("crawl_image_error");

const btn_submit = document.getElementById("btn_submit");

// 이미지 크롤링
btn_image.addEventListener("click",async() =>{
    if(crawl_image_title.value == ""){
        document.getElementById("crawl_image_error").innerHTML = "<p style='color:red;'>등록할 이미지에 관련된 텍스트를 입력해 주세요</p>"
        return false;
    }
    btn_image.disabled = true;
    crawl_image_title.readOnly = true;
    btn_image.value = "로딩중";
    crawl_image_error.innerHTML = "<p style=color:green;>잠시만 기다려 주세요...<p>";
    
    try{
        const response = await fetch(crawl_image_title.getAttribute("data-url")+"?crawl_image_title="+crawl_image_title.value,{
            method:"GET",
        })
        const result = await response.json()
        if(result.success == false){

            crawl_image_error.innerHTML = ""
            crawl_image_title.readOnly = false;
            btn_image.disabled = false;
            alert(result.message)

        }else{
            show_image.style.backgroundImage = `url('/${result.image_url}')`;
            show_image.style.backgroundSize = "200px";
            show_image.style.backgroundRepeat = "no-repeat";
            
            crawl_image.value = result.image_url;
            
            crawl_image_error.innerHTML = ""
            crawl_image_title.readOnly = false;

            btn_image.disabled = false;
            btn_image.value = "다른 이미지" 
        }
        
    }catch(error){
        crawl_image_error.innerHTML = ""
        crawl_image_title.readOnly = false;
        btn_image.disabled = false;
        btn_image.value= "이미지 넣기";
        alert(error + "실패 했습니다. 다시 시도 해주세요.");
    }
})

// 등록하기
btn_submit.addEventListener("click",async() =>{
    if(validation() == false){
        return false;
    }

    try{
        const data = new FormData(document.getElementById("regist_form"));
        if(!validation()){
            return false;
        }
        const response = await fetch('',{
            method:"POST",
            headers:{'X-CSRFToken': csrftoken},
            body:data
        })
        const result = await response.json();
        if(response.status == 400){
            alert(result.message)
        }else{
            location.href = result.url;
        }
        
    }catch(error){
        alert("로그인 실패.. 관리자에게 문의해주세요.");
    }
})


// 유효성 검사
function validation(){
    if(eatery_name.value == ""){
        eatery_name.focus();
        eatery_name.classList.add("is-invalid");
        document.getElementById("copy_eatery_name").innerHTML = "<p style=color:red;>음식점 이름을 입력해주세요<p>";
        return false;
    }
    if(eatery_type.value == ""){
        eatery_type.focus();
        eatery_type.classList.add("is-invalid");
        document.getElementById("copy_eatery_type").innerHTML = "<p style=color:red;>종류를 입력해주세요<p>";
        return false;
    }
    if(comment.value == ""){
        comment.focus();
        comment.classList.add("is-invalid");
        document.getElementById("comment_error").innerHTML = "<p style=color:red;>한 줄평을 입력해주세요<p>";
        return false;
    }
    if(eatery_real_location.value == ""){
        show_location.focus();
        show_location.classList.add("is-invalid");
        document.getElementById("copy_show_location").innerHTML = "<p style='color:red;font-size:13px;'>위치를 입력해주세요<p>";
        return false;
    }

    return true;
}

//이미지 바꾸기
$('#user_image').change(function(e){
    readPic(e)
}).siblings('label').css({'background-image': `url(${$('#user_image').val()})`})

//이미지 보이기
function readPic(input) {
    if (input.target.files && input.target.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            $("#show_image").css({'background-image': 'url('+e.target.result+')'})
            $("#show_image").css({"background-size":"200px"})
            $("#show_image").css({"background-repeat":"no-repeat"})
        }
        reader.readAsDataURL(input.target.files[0]);
    }
}


// 텍스트 쓰기
eatery_name.addEventListener("input",e =>{
    copy_eatery_name.innerHTML = "<p>"+eatery_name.value+"</p>";
})
show_location.addEventListener("input",e =>{
    copy_show_location.innerHTML = "<p>"+show_location.value+"</p>";
})
eatery_type.addEventListener("change",e =>{
    copy_eatery_type.innerHTML = "<p>"+eatery_type.options[eatery_type.selectedIndex].text+"</p>";
})

window.oninput = function(){
    crawl_image_error.innerHTML = "";
}
eatery_name.oninput = function(){
    eatery_name.classList.remove("is-invalid");
}
eatery_type.onchange = function(){
    eatery_type.classList.remove("is-invalid")
}
comment.oninput = function(){
    comment.classList.remove("is-invalid")
    document.getElementById("comment_error").innerHTML = "";
}
show_location.oninput = function(){
    show_location.classList.remove("is-invalid")

}


//----------------카카오 지도 api------------------------------------

// 마커를 담을 배열입니다
var markers = [];

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

// 키워드로 장소를 검색합니다
searchPlaces();

// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {

    var keyword = document.getElementById('keyword').value;

    if (!keyword.replace(/^\s+|\s+$/g, '')) {
        alert('키워드를 입력해주세요!');
        return false;
    }

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch( keyword, placesSearchCB); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title,) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });
            
            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };
            
            itemEl.onmouseout =  function () {
                infowindow.close();
            };
            
            itemEl.onclick = function(e){
                show_location.value = e.target.value;
                if(show_location.value == "undefined"){
                    show_location.value = "";
                    return false;
                }

                if(confirm("음식점 이름을 검색된 이름으로 바꿀까요?")){
                    eatery_name.value = title;
                    copy_eatery_name.innerHTML = "<p>"+eatery_name.value+"</p>";
                }
                copy_show_location.innerHTML = "<p>"+show_location.value+"</p>";
                eatery_real_location.value = bounds;
            }
            
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray" id="jibun">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
                
    itemStr += '  <span class="tel">' + places.phone  + '</span>' 
                    
    
    itemStr += `<button type="button" class="btn btn-warning" value="${places.address_name}" style="width:50px;">선택</button>` +
                '</div>';  

    el.innerHTML = itemStr;
    el.className = 'item';
    

    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage 
        });

    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

// 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}

    
