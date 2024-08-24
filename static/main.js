const fileElem=document.querySelector('#fileElem');
const wait=document.querySelector('#wait');

function add(){
    if(fileElem){
        fileElem.click();
        wait.showModal()
        setTimeout(()=>{
            wait.close()
        },1000)
    };
}