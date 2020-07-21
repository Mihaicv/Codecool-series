
const btnEditOverview=document.querySelector('#bt_edit_overview')
const txtOverview=document.querySelector('.textarea_overview')
const btnSend=document.querySelector('.submit_edit_ow')
const divOverw=document.querySelector('.overw')

btnEditOverview.addEventListener('click',function(){
   divOverw.classList.toggle('visible')
    txtOverview.getAttribute('id')
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

btnSend.addEventListener('click', function () {
        let idOverview=txtOverview.getAttribute('id')
        let textOverview=txtOverview.value
        let dataToPost={'idOverview':idOverview,'textOverview':textOverview}
        console.log(dataToPost)
        addData(dataToPost, '/edit_overview')
        divOverw.classList.remove('visible')

})