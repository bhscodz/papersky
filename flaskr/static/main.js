const fileElem=document.querySelector('#file');
const wait=document.querySelector('#wait');
const input=document.querySelector('#file');
const form=document.querySelector('#file_form');
const main_content=document.querySelector('main');
const pri_content=document.querySelector('#preview_holder');
const submit_button=document.querySelector('#submit');
const msg_list=document.querySelectorAll(".message");
const toast_container=document.querySelector("#toast_container");

function gen_toast(message,category){
    let role='status';
    let way='polite';
    let background='text-bg-primary';
    let d=document.createElement('div');
    if(category=='error'){
        role='alert';
        way='assertive';
        background='text-bg-danger';
    }
    if(category=='success'){
        background='text-bg-success';
    };
    d.innerHTML=`<div class="toast ${background}" role=${role} aria-live=${way} aria-atomic="true" data-bs-delay="2000">
                    <div class="toast-header text-white bg-dark">
                        <strong class="me-auto">papersky</strong>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                        ${message}
                    </div>
                </div>`;
    toast_container.appendChild(d);
    setTimeout(()=>{$(d).fadeOut();},5000)
    return d;
};

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
    const curfile=input.files;
        for (const file of curfile) {
        let card=document.createElement('div');
        card.style.borderRadius='10px';
        card.style.border='2px solid white';
        card.style.width='300px';
        card.classList.add('card','bg-dark')
        let image = document.createElement("img");
        image.src = URL.createObjectURL(file);
        image.style.width='100%';
        image.style.height='auto';
        image.classList.add('card-img-top')
        let cancel_button=document.createElement('button');
        cancel_button.textContent="cancel";
        cancel_button.classList.add('cancel_button', 'btn', 'btn-primary');
        cancel_button.addEventListener('click',(e)=>{
            remove(e);
            card.remove();
            input.value='';
        })
        card.innerHTML=`
            <div class="card-body text-bg-dark">
                <h5 class='card-title'>${file.name}</h5>
                <p>size -- ${file.size}</p>
            </div>
        </div>`;
        card.appendChild(cancel_button);
        card.prepend(image);
        pri_content.append(card);
    }
};

function remove(e){
    e.target.remove();
};
submit_button.addEventListener('click',(e)=>{
   if (input.files.length==0) {
        window.alert('please select file first')
        e.preventDefault();
   }
   else{
    $.ajax({
        type: form.method,
        url: form.action,
        data: new FormData(form),
        contentType:"multipart/form-data",
        dataType:'json',
        processData:false,
        contentType:false,
        success: function (response) {
            pri_content.innerHTML='';
            gen_toast(response.data,response.status).firstChild.classList.add('show');
        },
        error: function (response) {
            console.log('failiure',response.data,response.status);
            gen_toast(response.data,response.status).firstChild.classList.add('show');
        }
    });
    console.log('submitted')
    /* form.submit() */
   };
})
input.addEventListener('change',()=>{
    curfile=input.files;
    if (curfile.length!=0){
        console.log('changed')
        for(const file of curfile){
            console.log(file.size,file.name,file)
        } 
        preview()
    };
})
