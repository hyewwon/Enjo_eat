const btn_start = document.getElementById("btn_start");

const selectall = document.querySelector("input[name='all']");
const check = document.querySelectorAll("input[name='eatery_type']:checked")
const checkboxes = document.getElementsByName('eatery_type');
const eatery_location = document.getElementById("eatery_location");
const search_result = document.getElementById("search-result");

const search_container = document.getElementById("search-container");
const form  = document.getElementById("option_form");
var location_list = []

// 1. 음식점 종류 

// checkbox event
function checkSelectAll()  {
  const checkboxes = document.querySelectorAll('input[name="eatery_type"]');
  const checked = document.querySelectorAll('input[name="eatery_type"]:checked');
  const selectAll = document.querySelector('input[name="select_all"]');
  
  if(checkboxes.length === checked.length)  {
    selectAll.checked = true;
  }else {
    selectAll.checked = false;
  }

}

function selectAll(selectAll)  {
  const checkboxes = document.getElementsByName('eatery_type');
  
  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAll.checked
  })
}


// 2. 음식점 검색

// 주소 검색
document.addEventListener("DOMContentLoaded", async() =>{
  try{
    const response = await fetch("/get-group-location/",{
      method:"GET"
    });
    const result = await response.json();
    
    if(result.success == false){
      alert(result.message);
    }else{
      location_list = result.eatery_location
    }
    
  }catch(error){
    alert("주소 검색 오류.. 관리자에게 문의해주세요!");
  }
})

// 검색된 주소 표시
search_container.addEventListener("keyup",()=>{

  var txt = eatery_location.value;
  
  let matched_locations = [];
  location_list.forEach(function(location){

    if(txt == ""){
      search_result.innerHTML = "<p>검색된 주소가 없습니다.</p>";

    }else if(location.indexOf(txt.trim()) > - 1){
      matched_locations.push(location);
    }
  })

  const set = new Set(matched_locations)

  if(matched_locations.length == 0){
    search_result.innerHTML = "<p>검색된 주소가 없습니다.</p>";
  }else{
    search_result.innerHTML = "";
  }

  var cnt = 0
  set.forEach(function(location){
    cnt += 1
    let div = document.createElement("div");
    div.class="result-container";

    div.innerHTML = `
      <div class="custom-radio" onclick="setLocationValue('${location}');">
      <input type="radio" id="radio-${cnt}" value="${location}" name="tabs">
      <label class="radio-label" for="radio-${cnt}">
      <div class="radio-circle"></div>
      <span class="radio-text">${location}</span></label></div>
      `;
    search_result.appendChild(div);
  })

})


function setLocationValue(value){
  eatery_location.value = value;
}


// 3. 뽑기 시작

// 유효성 검사
function validation(){
  count_check = 0;
  for(i=0;i<checkboxes.length;i++){
    if(checkboxes[i].checked){
      count_check += 1;
    }
  }
  
  if(count_check == 0){
    return false;
  }

  return true;

}
// 뽑기 시작
btn_start.addEventListener("click", ()=>{
  if(validation() == false){
    return false;
  }
  form.submit();
})






