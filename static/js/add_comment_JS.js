
const adCommentJS=document.querySelector('.add_comment_js')
const formJS=document.querySelector('.form_commentJS');
const text_comment=document.querySelector('.text')
const saveBtn=document.querySelector('#save_btn')
const show_comments=document.querySelector('.show_comment')

adCommentJS.addEventListener('click',function(){
    formJS.classList.toggle('visible')
})
async function addData(data, url) {
    let response = await fetch(`${url}`, {
        method: "POST",
        mode: "cors",
        cache: "default",
        credentials: "include",
        headers: {"Content-Type": "application/json"},
        redirect: "follow",
        body: JSON.stringify(data)
    })
    // let result = await response.json()
    // console.log(result)
}

//GET
async function getdata(callback,id) {
    let rowData = await fetch(`/get_comment_JS/${id}`)
    let data = await rowData.json()
    callback(data)
}
saveBtn.addEventListener('click', ()=>{
    let id_text= text_comment.getAttribute('id')
    let text=text_comment.value
    let dataForFetchPost={'id_text': id_text, 'text':text}
    addData(dataForFetchPost, '/add_comment_JS')
    formJS.classList.remove('visible')
    location.reload();
})
function showComments(data){
    for(i=0;i<data.length;i++){
    let comment=document.createElement('li')
    comment.innerHTML=data[i].message
    show_comments.insertAdjacentElement('beforeend',comment)
    }
}
async function main(){
    let id_text=text_comment.getAttribute('id')
    getdata(showComments, id_text)
}
main()