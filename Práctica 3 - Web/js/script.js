//Comprueba si le viene por parámetros un nombre o ID, y lo busca
buscarPorParams();

const colors = {
    fire: '#dd5a5a',
    grass: '#6de07e',
    electric: '#d4dd5a',
    water: '#5ab4dd',
    steel: '#c5c5c5',
    ghost: '#8f39c9',
    dark: '#3f3f3f',
    ice: '#7fd2f3',
    ground: '#d48645',
    rock: '#aa7d59',
    fairy: '#ed93c7',
    poison: '#7f00d4',
    bug: '#a4dd5a',
    dragon: '#5f95c7',
    psychic: '#dd5aab',
    flying: '#97b3e6',
    fighting: '#dd2d2d',
    normal: '#F5F5F5'
};

function buscarPorParams(){
    var params = new URLSearchParams(window.location.search);
    var nombre_id = params.get("id_or_name");
    if (nombre_id != null){
        buscarPokemon(nombre_id);
        return;
    }
    //Si no tenemos nombre_id, no podemos realizar una búsqueda directa
    //Hacemos una búsqueda avanzada
    var iniciales = params.get("iniciales");
    var tipo = params.get("tipo");
    //Con que haya alguno de los parámetros, ya se puede realizar la búsqueda
    if (!((iniciales == null) && (tipo == null))){
        buscarAvanzado(iniciales, tipo);
        return;
    }
}

document.querySelector('button#busqueda_simple').addEventListener('click', event => {
    var nombre_id = document.querySelector('input#id_or_name').value;
    window.location.href = ('?id_or_name=' + nombre_id);
});

document.querySelector('button#busqueda_avanzada').addEventListener('click', event =>{
    //TODO: controlar que pasa si no buscamos por iniciales
    var iniciales = document.querySelector('input#iniciales').value;
    var tipo = document.querySelector('input#tipo').value;
    var selectedTipo;
    switch (tipo){
        case 'Agua': selectedTipo = 'water'; break;
        case 'Fuego': selectedTipo = 'fire'; break;
        case 'Planta': selectedTipo = 'grass'; break;
        case 'Normal': selectedTipo = 'normal'; break;
        case 'Fantasma': selectedTipo = 'ghost'; break;
        case 'Siniestro': selectedTipo = 'dark'; break;
        case 'Lucha': selectedTipo = 'fighting'; break;
        case 'Hada': selectedTipo = 'fairy'; break;
        case 'Psíquico': selectedTipo = 'psychic'; break;
        case 'Hielo': selectedTipo = 'ice'; break;
        case 'Dragón': selectedTipo = 'dragon'; break;
        case 'Roca': selectedTipo = 'rock'; break;
        case 'Tierra': selectedTipo = 'ground'; break;
        case 'Acero': selectedTipo = 'steel'; break;
        case 'Volador': selectedTipo = 'flying'; break;
        case 'Bicho': selectedTipo = 'bug'; break;
        case 'Eléctrico': selectedTipo = 'electric'; break;
        case 'Veneno': selectedTipo = 'poison'; break;
        default : selectedTipo = null; break;
    }
    
    //No meter los parámetros que estén vacíos
    var isFirst = true;
    var resultURL = '';
    if (iniciales != ""){
        if (isFirst){
            resultURL = resultURL + '?';
            isFirst = false;
        }else{
            resultURL = resultURL + '&';
        }
        resultURL = resultURL + 'iniciales=' + iniciales;
    }
    if (selectedTipo != null){
        if (isFirst){
            resultURL = resultURL + '?';
            isFirst = false;
        }else{
            resultURL = resultURL + '&';
        }
        resultURL = resultURL + 'tipo=' + selectedTipo;
    }
    window.location.href = resultURL;
});

function buscarPokemon(nombre_id){
    var nombre_lower = nombre_id.toLowerCase();
    fetch(`https://pokeapi.co/api/v2/pokemon/${nombre_lower}`)
    .then(response => {
        switch (response.status){
            case 200:
                response.json().then(pokemon => mostrarPokemon(pokemon));
                break;
            case 404:
                console.log("not found error");
                throw Error('not found');
            case 500:
                console.log("server error");
                throw Error('server');
            default:
                console.log("network error");
                throw Error('network');
            }
        })
    .catch(error => {
        console.log('Error: ' + error.message);
        switch (error.message){
            case 'not found':
                document.getElementById("error_busqueda_simple").style.display = "block";
                break;
            case 'server':
            case 'network':
            default:
                document.getElementById("error_red").style.display = "block";
                break;
        }
    });
}


function buscarAvanzado(iniciales, tipo){
    //son 898 en total
    document.getElementById("wrapper_resultados_avanzados").style.display = "block";
    var foundAny = false;
    for (let index = 1; index <= 898; index++) {
        fetch(`https://pokeapi.co/api/v2/pokemon/${index}`)
        .then(response => {
            response.json()
            .then(pokemon => {
                if ((matchesIniciales(pokemon.name, iniciales)) && (matchesTipo(pokemon.types, tipo))){
                    foundAny = true;
                    mostrarPokemons(pokemon);
                }
                if ((index==898) && (!foundAny)){
                    document.getElementById("error_busqueda_avanzada").style.display = "block";
                }
            })
        })
        .catch(function(error){
            console.log('Error en la petición al servidor: ' + error.message);
            document.getElementById("error_red").style.display = "block";
        });
    }
}

function matchesIniciales(pokemon_name, iniciales){
    if (iniciales == null){
        return true;
    }
    var inicial = pokemon_name.charAt(0);
    var iniciales_lower = iniciales.toLowerCase();
    for (let index = 0; index < 3; index++) {
        if (inicial == iniciales_lower.charAt(index)){
            return true;
        }
    }
    return false;
}

function matchesTipo(pokemon_types, tipo){
    if (tipo == null){
        return true;
    }
    var tipo1 = pokemon_types[0].type.name.toLowerCase();
    var tipo2;
    
    try{
        tipo2 = pokemon_types[1].type.name.toLowerCase();
    }catch(error){
        tipo2 = "";
    }
    
    if((tipo1 == tipo) || (tipo2 == tipo)){
        return true;
    }else{
        return false;
    }
}

function mostrarPokemons(pokemon){
    var itemHTML = "";

    itemHTML = 
    `<div class="pokemon_matched">
        <img class="pokemon_sprite_avanzado" src="`;
    
        var sprite_address = pokemon['sprites']['front_default']
    if (sprite_address == null){
        sprite_address = "images/pikachu_buscando.jpg";
    }

    itemHTML = itemHTML + sprite_address;

    itemHTML = itemHTML +
    `" alt="Sprite del Pokémon">
        <div class="pokemon_id_name_avanzado"><p>`;

    itemHTML = itemHTML + pokemon.id + "#" + pokemon.name;

    itemHTML = itemHTML + 
    `</p></div>
        <a class="a_lupita" href="`;

    itemHTML = itemHTML + "?id_or_name=" + pokemon.id;

    itemHTML = itemHTML +
    `   "><img src="images/lupa.png" alt="Icono de búsqueda simple" class="lupita"></a>
    </div>`;
        
    document.getElementById("resultados_avanzados").insertAdjacentHTML("beforeend", itemHTML);
}

//Mostramos los datos obtenidos de la API
function mostrarPokemon(pokemon){
    //Sprite del pokemon
    var img = document.getElementById('pokemon_sprite');
    var imgsource = pokemon['sprites']['other']['official-artwork']['front_default']
    if (imgsource == null){
        imgsource = pokemon['sprites']['front_default'];
    }
    if (imgsource == null){
        imgsource = "images/pikachu_buscando.jpg"
    }
    img.setAttribute("src", imgsource);

    //ID y nombre
    var id = document.getElementById('pokemon_id_name').getElementsByTagName("p")[0];
    var nombreBonito = document.getElementById('pokemon_id_name').getElementsByTagName("p")[1];
    var name;
    id.textContent = "ID#" + pokemon.id;
    name = pokemon.name;
    nombreBonito.textContent = name.charAt(0).toUpperCase() + name.slice(1);

    //Primer tipo
    var tipo = document.getElementById('pokemon_types').getElementsByTagName("p")[0];
    tipo.textContent = traducirTipo(pokemon.types[0].type.name);
    var color1 = colors[pokemon.types[0].type.name];
    document.getElementById('tipo1').style.backgroundColor = color1;

    //Segundo tipo, a veces no existente y por ello debemos contemplar la posibilidad
    var tipo2;
    try {
        var tipo2 = document.getElementById('pokemon_types').getElementsByTagName("p")[1];
        tipo2.textContent = traducirTipo(pokemon.types[1].type.name);
        var color2 = colors[pokemon.types[1].type.name];
        document.getElementById('tipo2').style.backgroundColor = color2;
        document.getElementById("tipo2").style.visibility = "visible";
    }
    catch (error) {
        if(error){
            document.getElementById("tipo2").style.visibility = "hidden";
        }
    }
    

    //Estatura y peso
    var estatura = document.getElementById('pokemon_fisico').getElementsByTagName("p")[0];
    var peso = document.getElementById('pokemon_fisico').getElementsByTagName("p")[1];
    var estaturaAux = pokemon.height;
    var pesoAux = pokemon.weight;
    
    estatura.textContent = "Estatura: " + (estaturaAux / 10) + "m";
    peso.textContent = "Peso: " + (pesoAux / 10) + "kg";
    
    document.getElementById("wrapper_resultados").style.display = "block";
}

function traducirTipo(tipo){
    switch (tipo){
        case 'water': return 'Agua';
        case 'fire': return 'Fuego';
        case 'grass': return 'Planta';
        case 'normal': return 'Normal';
        case 'ghost': return 'Fantasma';
        case 'dark': return 'Siniestro';
        case 'fighting': return 'Lucha';
        case 'fairy': return 'Hada';
        case 'psychic': return 'Psíquico';
        case 'ice': return 'Hielo';
        case 'dragon': return 'Dragón';
        case 'rock': return 'Roca';
        case 'ground': return 'Tierra';
        case 'steel': return 'Acero';
        case 'flying': return 'Volador';
        case 'bug': return 'Bicho';
        case 'electric': return 'Eléctrico';
        case 'poison': return 'Veneno';
        default : return null;
    }
}
