
const container=document.querySelector('.container')
const ulActors=document.querySelector('#actors')         //----lista de actori

async function getData(callback) {
    let data=await fetch('/get_actors')
    let dataJson=await data.json()
    callback(dataJson)
}
function showTable(data){
    for(let i of data){
        let films=i.string_agg.split(',');

        let liNameActor=document.createElement('li');  //----numele fiecarui actor
         liNameActor.addEventListener('click',function () {
                    ulMovies.classList.toggle('active')
        })
        liNameActor.classList.add('name_actor');
        liNameActor.innerHTML=i.name;
        ulActors.appendChild(liNameActor);
        container.appendChild(ulActors);

        const ulMovies=document.createElement('ul')        //---lista de filme ale actorului
        ulMovies.classList.add('movies')

        for ( let film=0; film<films.length;film++){
            let liActorMovie=document.createElement('li')     //----numele fiecarui film
            liActorMovie.classList.add('actor_movie')
            liActorMovie.innerHTML=films[film]
            ulMovies.appendChild(liActorMovie)
            ulActors.appendChild(ulMovies)
            container.appendChild(ulActors)
        }
    }
}

async function main() {
    await getData(showTable)
}
main()