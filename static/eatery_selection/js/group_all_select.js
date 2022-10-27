const btn_start = document.getElementById("btn_start");
const search_location = document.getElementById("search_location");

const selectall = document.querySelector("input[name='all']");
const check = document.querySelectorAll("input[name='eatery_type']:checked")
const checkboxes = document.getElementsByName('eatery_type');
const eatery_location = document.getElementById("eatery_location");
const search_result = document.getElementById("search_result");

const checkbox_section = document.getElementById("checkbox_section");
const input_section = document.getElementById("input_section");
const url = eatery_location.getAttribute("data-url");
const form  = document.getElementById("option_form");

// 주소 검색
document.addEventListener("DOMContentLoaded", async() =>{

  try{
    const response = await fetch(url,{
      method:"GET"
    });
    const result = await response.json();
    
    if(result.success == false){
      alert(result.message);
    }else{
      result.eatery_location;
    }

    input_section.addEventListener("keyup",()=>{

      var txt = eatery_location.value;
      
      let locations = [];
      result.eatery_location.forEach(function(location){

        if(txt == ""){
          search_result.innerHTML = "<p class='form-text'>검색된 주소가 없습니다..</p>";

        }else if(location.indexOf(txt.trim()) > - 1){
          locations.push(location);
        }
      })

      const set = new Set(locations)

      if(locations.length == 0){
        search_result.innerHTML = "<p class='form-text'>검색된 주소가 없습니다..</p>";
      }else{
        search_result.innerHTML = "";
      }

      set.forEach(function(location){
        let div = document.createElement("div");
        div.id ="txt_location_section";
        div.class="col-2";
        div.innerHTML = `<button id="txt_location" onclick="selectLocation(this);" value="${location}" class="btn">${location}</button>`;
        search_result.appendChild(div);
      })


    })
    
  }catch(error){
    alert(error);
  }
})

function selectLocation(location){
  eatery_location.value = location.value;
  search_result.innerHTML = "";

}


btn_start.addEventListener("click", ()=>{
  if(validation() == false){
    return false;
  }
  form.submit();
})

function checkSelectAll(checkbox){
    if(checkbox.checked == false){
        selectall.checked = false;
    }
}

function selectAll(selectAll)  {
    checkboxes.forEach((checkbox) => {
      checkbox.checked = selectAll.checked;
    })
  }


checkbox_section.addEventListener("change",function(){
  document.getElementById("check_error").innerHTML = "";
  checkbox_section.style.borderColor = "lightgray";
})


eatery_location.addEventListener("input",function(){

  eatery_location.style.borderColor = "rgb(232,122,68)";

  if(eatery_location.value == ""){
    eatery_location.style.borderColor = "lightgray";
  }
})

function validation(){
  count_check = 0;

  for(i=0;i<checkboxes.length;i++){
    if(checkboxes[i].checked){
      count_check += 1;
    }
  }
  
  if(count_check == 0){
    document.getElementById("check_error").innerHTML = "<p style='color:red;'>종류를 하나 이상 선택해 주세요</p>";
    checkbox_section.style.borderColor = "red";
    return false;
  }

  return true;

}



