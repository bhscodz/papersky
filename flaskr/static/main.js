const fileElem=document.querySelector('#file');
const wait=document.querySelector('#wait');
const input=document.querySelector('#file');
const form=document.querySelector('form');
const main_content=document.querySelector('main');
const pri_content=document.querySelector('#preview_holder');
const submit_button=document.querySelector('#submit');
const msg_list=document.querySelectorAll(".message");


function add(){
    if(fileElem){
        fileElem.click();
        wait.showModal()
        setTimeout(()=>{
            wait.close()
        },1000)
    };
}
function preview(){
    let article=document.createElement('article');
    let p_are=document.createElement('p');
    const curfile=input.files;
    for (const file of curfile) {
        let image = document.createElement("img");
        
        image.src = URL.createObjectURL(file);
        image.style.width='40%';
        image.style.height='30%';
        let cancel_button=document.createElement('button');
        cancel_button.textContent="cancel";
        cancel_button.classList.add('cancel_button');
        cancel_button.addEventListener('click',(e)=>{
            remove(e);
            article.remove();
        })
        article.appendChild(cancel_button);
        article.append(image);
        }
        article.append(p_are);
        pri_content.append(article);
    };

function remove(e){
    e.target.remove();
};
submit_button.addEventListener('click',(e)=>{
   if (input.files.length==0) {
        window.alert('please select file first')
        e.preventDefault();
   }
})
input.addEventListener('change',()=>{
    curfile=input.files;
    if (curfile.length!=0){
        console.log('changed')
        for(const file of curfile){
            console.log(file.size,file.name)
        } 
        preview()
    };
})
