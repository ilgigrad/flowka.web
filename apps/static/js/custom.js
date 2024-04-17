var colors={"danger":   "#d1313d",
            "warning":  "#e5625c",
            "alert":   "#f9bf76",
            "info":     "#34a9d4",
            "success":  "#dedd23"};
var colorIndexes=["danger","warning","alert","info","success"];

function textCount(elem) {

  var message=elem;
  if (message.hasAttribute("maxlength")){
    var maxLength=message.maxLength;
  }
  else {
    var maxLength=500;
  }

  count = (maxLength - message.value.length);
  oclass = ('counter','fl-txt-sm');
  rate =Math.floor(4*count/Math.max(maxLength,1));
  style = "color: "+colors[colorIndexes[rate]]+";";
  newdiv = document.createElement('div');
  newdiv.classList.add(oclass);
  newdiv.style=style;
  newdiv.setAttribute('id',elem+"_counter");
  newdiv.innerText = ' : '+Math.abs(count);
  olddiv=document.getElementById(elem+"_counter");
  olddiv ? olddiv.replaceWith(newdiv) : message.insertAdjacentElement('afterend', newdiv);
}


function getPasswords() {
		var pwds=[];
		var form=document.getElementById("id_PasswordForm");
		var inputs= form.getElementsByTagName("input");
		for(i in inputs){
      input=inputs[i];
			if (input.type=="password"){
				pwds.push(input);
			}
		}
		return pwds;
}

function passwordStrength() {
    //pwd = document.getElementById(idpassword);
		var pwds = getPasswords();

    var confirm=pwds.pop();
    var pwd = pwds.pop().value;
    var spwd = pwd.length>0 ? pwd[0] : "";
    for (var i=1; i<pwd.length; i++){
      spwd+= pwd[i]!=pwd[i-1] ? pwd[i] : "";
    }

      var score=Math.min((spwd.length*2),15);
    	var regexs=[];
    	regexs[0] = /[\{\}\#\$\&\~\\\·\^\|\€\-\*\\[\]\(\)\=\+\£\µ\!\?\,\;\:\§\'\°\@\"ÏÖÜËÄ\%\.]/;
    	regexs[1]=/[0-9]/;
			regexs[2]= /[A-Z]/;
      regexs[3]=/[a-z]/;
			var weight=[25,25,20,15];
    	for (var i in regexs){
      	var gotit = spwd.match(regexs[i]);
        if (gotit && gotit.length>0){
            score+=weight[i];
        }
    	}
		var strength= Math.floor(score/25);
		var style=[
			"width:"+score+"%;height:100%; background-color:"+colors["danger"]+";",
			"width:"+score+"%;height:100%; background-color:"+colors["warning"]+";",
			"width:"+score+"%;height:100%; background-color:"+colors["alert"]+";",
			"width:"+score+"%;height:100%; background-color:"+colors["info"]+";",
			"width:"+score+"%;height:100%; background-color:"+colors["success"]+";"];

    progressbar=document.getElementById('id_progress_bar');
    progressbar.setAttribute('style',style[strength]);
	return strength;

}

function passwordsMatch() {
    var pwds = getPasswords();
  	var pwd2 = pwds.pop();
  	var pwd1 = pwds.pop();
  	if (pwd1.value==pwd2.value && pwd1.value.length>5){
  		style="background-color: "+colors["success"]+";";
      match=1;
  	}
  	else {
  		style="border: "+colors["danger"]+" solid 1px;";
      match=0;String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
      }
  	}
  	pwd2.setAttribute("style",style);
  	pwd1.setAttribute("style",style);
    return match;
}

function okPassword(){
    match=passwordsMatch();
    strength=passwordStrength();
    if (match*strength>0){
      var style="btn btn-lg flowka btn-block";
      document.getElementById("id_submitPasswordForm").disabled=false;
      document.getElementById("id_submitPasswordForm").setAttribute("class",style);
    }
    else {
      var style="btn btn-lg fl-bg-light fl-txt-white btn-block";
      document.getElementById("id_submitPasswordForm").disabled=true;
      document.getElementById("id_submitPasswordForm").setAttribute("class",style);
    }
}

function submitForm(el) {
    if (typeof(el)==='string'){
      var oForm = document.getElementById(el);}
    else if (typeof(true)==='object' && el.tagName==='FORM') {
      var oForm = el;}
    else {
      oForm=el.closest('form');
    }
    if (oForm) {
        oForm.submit();
    }
    else {
        alert("DEBUG - could not find element " + formId);
    }
}



function submitSelected(el){
  //select one object, and submit it
  form=el.closest('form');
  selected=form.getElementsByClassName("fl_obj_selected");
  for (i in selected){
    selected[i].value=(el.id).replace(RegExp(/\D*/,'g'),'');
  }
  form.submit();
}

function selector(el,listName,idLinkedButtons){
  //select many objects, feed a list and activate the button for submission
    objLists=document.getElementsByName(listName);
    objList=objLists[0];
    objId=el.id;
     var newList = objList.getAttribute("value").length==0 ? [] : objList.getAttribute("value").split(',');
     if (newList.includes(objId)){
       newList.splice(newList.indexOf(objId),1);
       el.classList.remove("fl-selected");
      }
     else {
       newList.push(objId);
       el.classList.add("fl-selected");
      }
      for (i in objLists) {
        objList=objLists[i];
        objList.value=newList.toString();
      }
     for (i in idLinkedButtons){
       idLinkedButton=document.getElementById(idLinkedButtons[i]);
       if (newList.length>0){
         idLinkedButton.classList.add("fl-pointer");
         idLinkedButton.classList.remove("disabled");
         idLinkedButton.disabled=false;
         idLinkedButton.setAttribute("tabindex","0");
       }
       else {
         idLinkedButton.classList.remove("fl-pointer");
         idLinkedButton.classList.add("disabled");
         idLinkedButton.disabled=true;
         idLinkedButton.setAttribute("tabindex","-1");
       }
     }
}

function clickOnHover(e) {
 e.click();
}

function clickIt(target_id) {
 var target=document.getElementById(target_id);
 target.click();
}

function exists(elem) {
 return (typeof(elem) != 'undefined' && elem != null);
}

function eraseChilds(elem){
 while (elem.lastChild) {
     elem.removeChild(elem.lastChild);
 }
}

function selectTab(el){
 //change the active tab
 let actives=el.parentElement.getElementsByClassName("active");
 for (let i = 0; i < actives.length; i++) {
   actives[i].classList.remove('active');
 }
 el.classList.add('active');
}

function scrollIt(el){
 //look for a ascendant that has something like *scroll* in its class
 let scroller=el.parentElement;
 while (scroller.classList.toString().search("scroll")<0) {
   scroller=scroller.parentElement;
   if (scroller===null){
     break;
   } //no more parent/ no scroller found -> exit
 }
 if (scroller !=null){ //no scroller found for this element -> pass
   var children=el.children;
   for (let child of children) {
     if (child.classList.contains("fl-tooltip")|child.classList.contains("fl-tooltip-flex")) {
       child.style.top=el.offsetTop-scroller.scrollTop+"px";
       child.style.left=el.offsetLeft-scroller.scrollLeft+"px";
       break;
     }
   }
 }
}

function scrollHeader(el,head){
 let header=document.getElementById(head);
 header.scrollLeft = el.scrollLeft;
}


function formAsDict(el) {
	let formsDict = {};
  let names = Array();
  let filter=['input','select','textarea','checkbox','button'];
  let selection=Array();
  for (let tag of filter){
    selection=selection.concat(Array.from(el.getElementsByTagName(tag)));
  }
	for( let formElem of selection) {
    if (el.contains(formElem) && !names.includes(formElem.getAttribute('name'))){
        names.push(formElem.getAttribute('name'));
      }
  }
  for (let name of names){
      elems=document.getElementsByName(name);
      if (elems.length>1){
        //checkbox multi / multi select
        var form=Array();
        for (let elem of elems){
          if (elem.classList.contains('fl-selected')){
          form.push(elem.value);
          }
        }
        if (form.length<=1){
          form=form[0];
        }
      }
      else{
          var form=elems[0].value;
      }

      formsDict[name]=form;
    }
 return formsDict;
}

function clickSelect(el,input_id,value) {
  //enable select when click on a button. the value is given to the related (hidden) element
  let siblings=el.parentElement.children;
  for (let child of siblings) {
    child.classList.remove("fl-selected");//remove all other selection
  }
  if (document.getElementById(input_id).value=="true" && value==true){
    document.getElementById(input_id).value=false;//this checkbox set false when click twice
    return(false);
  }
  else if (document.getElementById(input_id).value==value){
    document.getElementById(input_id).value=0; //this is select listbox set none when click twice
    return(false);
    }
  document.getElementById(input_id).value=value;
  el.classList.add("fl-selected");
  return(true);
}

function helpbar(helptitle='',helpdetails=''){
  document.getElementById('id_help_bar_title').innerHTML=helptitle;
  if (helptitle!='' && helpdetails!='') {
    helpdetails=' : '+helpdetails;
  }
  document.getElementById('id_help_bar_details').innerHTML=helpdetails;
}

String.prototype.capitalize = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
}

function quote(str){
  return( '\''+str+'\'');
}

function boolToggle(el,unique=false){
  el.classList.toggle('fl-selected');
  if (el.value.toLowerCase()=="true"){
    el.value=false;
  }
  else if (el.value.toLowerCase()=="false"){
    el.value=true;
  }

  if (unique){
    for (let child of el.parentElement.children) {
      if (child.id!=el.id){
        child.classList.remove("fl-selected");//remove all other selection
        if (Boolean(child.value) && child.value.toLowerCase()=="true"){
          child.value=false;
        }
      }
    }
  }

}

function select(el){
  el.value=el.options[el.selectedIndex].value;
}

function removeElem(id){
  while (true){
    var el=document.getElementById(id);
    if (el == null){
      break;
    }
    el.parentElement.removeChild(el);
  }
}
