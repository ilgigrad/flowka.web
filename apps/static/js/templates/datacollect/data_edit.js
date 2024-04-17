function enlight(el=null) {
  for (let cell of document.getElementsByClassName('col-hov')){
    cell.classList.remove('col-hov');
  }
  for (let cell of document.getElementsByClassName('col-hov')){
    cell.classList.remove('col-hov');
  }// all col-hov are not removed after the first execution
  if (el){
    for (let cell of document.getElementsByName(el.getAttribute('name'))){
        cell.classList.add('col-hov');
    }
  }
}

function initColumn(responseText,args){

  let container = document.getElementById(args[0]);

  container.innerHTML = responseText;
    if (args[1] != null && responseText.search(/innerModal/)>-1){
      let column = document.getElementById(args[1]);
      $(column).modal('show');
    }
}

function clickColumn(url,uid,columnid) {
  var idColumn = 'id_'+uid+'_'+columnid+'_column';
  var idContainer = 'id_'+uid+'_container';
  var fullURL=url+uid+'/'+columnid;
  pageLoad(fullURL,initColumn,idContainer,idColumn);
}


function sendColumn(url,uid,columnid) {
  fullURL=url+uid+'/'+columnid;
  let formDict = formAsDict(document.getElementById('id_'+uid+'_'+columnid+'_form'));
    restSend(fullURL,'PUT',JSON.stringify(formDict));
    //sendSubColumns(uid,columnid);
  closeColumn('id_'+uid+'_'+columnid+'_column');
}


function closeColumn(id){
  var el=document.getElementById(id);
  $(el).modal('hide');
  $('body').removeClass('modal-open');
  $('.modal-backdrop').remove();
  removeElem(id);
}


function clickSubColumn(el,url,uid,columnid,name){
    removeElem('id_'+uid+'_'+columnid+'_'+name+'_subcontainer');
    if (el.classList.contains('fl-selected') && url!=''){
      openSubColumn(el,url,uid,columnid,name);
    }
}

function openSubColumn(el,url,uid,columnid,name){
    var subContainer=document.createElement('div');
    subContainer.id='id_'+uid+'_'+columnid+'_'+name+'_subcontainer';
    el.parentElement.parentElement.appendChild(subContainer);
    var fullURL=url+uid+'/'+columnid;
    pageLoad(fullURL,initColumn,subContainer.id);
}
