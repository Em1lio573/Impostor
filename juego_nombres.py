from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "clave_secreta_ecuador_master_mega_123"
DICT_PASSWORD = "admin1234"  # <--- CLAVE DEL DICCIONARIO

# --- DATOS DEL JUEGO (Palabra, Pista Difícil) ---
DATA_ECUADOR = {
    "🇪🇨 Comida Típica": [
        ("Encebollado", "Levanta muertos con yuca y albácora"),
        ("Cuy Asado", "Roedor andino, manjar de fiesta"),
        ("Bolón de Verde", "Esfera matutina de masa y grasa divina"),
        ("Fanesca", "Doce granos y un pez penitente"),
        ("Guatita", "Mondongo bañado en salsa de cacahuate"),
        ("Ceviche de Camarón", "Crustáceos en sopa fría roja y ácida"),
        ("Hornado", "Cerdo entero con piel galleta"),
        ("Llapingachos", "Discos dorados de tubérculo serrano"),
        ("Morocho", "Espeso, blanco y se bebe caliente"),
        ("Tigrillo", "Majado al sartén, no es el animal"),
        ("Locro de Papa", "Crema andina que ama el aguacate"),
        ("Tripa Mishqui", "Intestinos al carbón de la esquina"),
        ("Humitas", "Pastel de choclo en su propio envoltorio"),
        ("Chugchucaras", "Todo lo que el cerdo puede ofrecer en un plato"),
        ("Yahuarlocro", "Sopa oscura que lleva sangre"),
        ("Seco de Pollo", "Guiso de ave, a veces con cerveza"),
        ("Seco de Chivo", "Guiso fuerte que suele ser borrego"),
        ("Chaulafan", "La fusión latina del arroz asiático"),
        ("Muchines de Yuca", "Tubérculo frito con corazón lácteo"),
        ("Corviche", "Óvalo de verde con alma de pescado"),
        ("Cazuela de Pescado", "Horneado de verde y mar en barro"),
        ("Sango de Camarón", "Espeso guiso verde con mariscos"),
        ("Caldo de Salchicha", "Sopa negra llena de embutidos"),
        ("Empanada de Viento", "Gigante, vacía y espolvoreada de blanco"),
        ("Empanada de Morocho", "Crocante maíz blanco relleno de carne"),
        ("Pristiños", "Corona frita bañada en miel"),
        ("Higos con Queso", "Fruta almibarada con compañero salado"),
        ("Espumilla", "Parece helado pero no se derrite"),
        ("Colada Morada", "Bebida espesa de frutos y harina negra"),
        ("Pan de Yuca", "Elástico, horneado y compañero del yogurt"),
        ("Chifles", "Monedas o tiras crujientes de verde"),
        ("Patacones", "Verde pisado y vuelto a freír"),
        ("Salprieta", "Polvo manabita de sabor intenso"),
        ("Viche Manabita", "La fanesca de la costa con mariscos"),
        ("Tongas", "Almuerzo completo envuelto para llevar"),
        ("Ayampaco", "Asado amazónico en hoja"),
        ("Maito", "Pescado al vapor en hoja bijao")
    ],
    "🇪🇨 Lugares Típicos": [
        ("Islas Galápagos", "Laboratorio viviente de Darwin"),
        ("Mitad del Mundo", "Un pie en el norte, otro en el sur"),
        ("El Panecillo", "La guardiana alada de la capital"),
        ("Malecón 2000", "Paseo moderno junto al gran río porteño"),
        ("Cotopaxi", "Cono perfecto de nieve y fuego"),
        ("Baños de Agua Santa", "Puerta a la selva y columpio al fin del mundo"),
        ("Montañita", "Capital del surf y la fiesta eterna"),
        ("La Ronda", "Callejón antiguo de poetas y canelazos"),
        ("Parque La Carolina", "Pulmón verde y deportivo de Quito"),
        ("Chimborazo", "El punto más cercano al espacio"),
        ("Laguna del Quilotoa", "Espejo esmeralda dentro de un volcán"),
        ("Mercado Artesanal", "Laberinto de tejidos y recuerdos"),
        ("Catedral de Cuenca", "Ladrillo visto y cúpulas celestes"),
        ("Parque Nacional Yasuní", "El lugar más biodiverso del planeta"),
        ("Nariz del Diablo", "El tren más difícil del mundo"),
        ("Ruinas de Ingapirca", "Huella Inca de piedra solar"),
        ("Laguna de Cuicocha", "Dos islotes en un cráter de agua"),
        ("El Cajas", "Páramo esponjoso de mil lagunas"),
        ("Puerto Ayora", "Corazón urbano de las islas encantadas"),
        ("Playa de los Frailes", "Media luna de arena virgen"),
        ("Malecón del Salado", "Brazo de mar y jardines en la ciudad"),
        ("Cerro Santa Ana", "444 escalones hacia el faro"),
        ("Teleférico de Quito", "Subida mecánica al Pichincha"),
        ("Basílica del Voto Nacional", "Gótico con tortugas y armadillos"),
        ("Parque Centenario", "Columna de la independencia en GYE"),
        ("Las Peñas", "Barrio de colores y adoquines porteños"),
        ("Mindo", "Paraíso de colibríes y mariposas"),
        ("Papallacta", "Calor volcánico en el frío páramo"),
        ("Salinas", "Edificios blancos frente al mar azul"),
        ("Atacames", "La playa de la fiesta y el ceviche"),
        ("Tena", "Capital de la canela y los ríos"),
        ("Puyo", "Puerta amazónica de Pastaza")
    ],
    "🍻 Farra y Chupa": [
        ("Pilsener", "La rubia que une al país"),
        ("Club Verde", "La premium de etiqueta esmeralda"),
        ("Zhumir", "Espíritu azuayo en botella"),
        ("Pájaro Azul", "Licor turquesa que no vuela"),
        ("Aguardiente", "Fuego líquido de caña"),
        ("Michelada", "Cerveza disfrazada de limonada salada"),
        ("Canelazo", "Calienta el cuerpo en la noche serrana"),
        ("Norteño", "El compañero fiel de las fiestas populares"),
        ("Biela", "Sinónimo callejero de la fría"),
        ("Caña Manabita", "Orgullo fuerte de la provincia costera"),
        ("Jager", "Licor de ciervo y hierbas"),
        ("Punta", "Destilado artesanal sin etiqueta"),
        ("Chicha", "Fermento ancestral masticado o hervido"),
        ("Guanchaca", "El abuelo rústico del aguardiente"),
        ("Cristal", "Aguardiente seco y transparente"),
        ("Switch", "Bebida barata de colores neón"),
        ("Rompe Colchón", "Coctel afrodisíaco marino"),
        ("7 Espíritus", "Bebida que promete ver fantasmas"),
        ("Blue", "El vodka premezclado de la juventud"),
        ("Corona", "La mexicana que pide limón"),
        ("Vino Hervido", "Bebida caliente de uva y especias")
    ],
    "🛒 Marcas Ecuatorianas": [
        ("Marathon", "Viste a la selección nacional"),
        ("Supermaxi", "La cadena del logo rojo y blanco"),
        ("Mi Comisariato", "El rival del logo rojo"),
        ("Banco Pichincha", "El gigante financiero amarillo"),
        ("Tía", "El vecino de precios bajos"),
        ("Sweet & Coffee", "Café y postres con logo rosa"),
        ("Manicho", "La fusión perfecta de cacao y maní"),
        ("Tango", "Dos galletas bailando con chocolate"),
        ("Tropical", "La gaseosa sabor frutilla nacional"),
        ("Güitig", "Milagro de la naturaleza con gas"),
        ("Fioravanti", "La roja clásica de las comidas"),
        ("Pinguino", "El ave que trae el frío dulce"),
        ("Deja", "Sinónimo de lavar ropa"),
        ("Lomito", "Atún premium en lata"),
        ("Ruffles", "Papas con ondas (versión local)"),
        ("Toni", "El gigante del yogurt"),
        ("Nutri Leche", "La vaca del cartón azul"),
        ("Indurama", "Cocinas y refris hechas en Cuenca"),
        ("Plumrose", "El jamón de la visita"),
        ("Real", "El rey de las sardinas y atunes"),
        ("Vanamps", "Los zapatos del colegio"),
        ("Sumesa", "Fresco solo y fideos"),
        ("Ile", "El sabor que pone la sazón"),
        ("La Tablita del Tártaro", "Carne al carbón en patio de comidas"),
        ("Candu", "El chicle o caramelo de la infancia"),
        ("Buestán", "Cuero y moda nacional")
    ],
    "🗣️ Jerga Ecuatoriana": [
        ("Chuchaqui", "Penitencia física post-farra"),
        ("Cholo", "Identidad mestiza o insulto clasista"),
        ("Aniñado", "Vive en burbuja y tiene plata"),
        ("Mandarina", "Sometido a la voluntad de ella"),
        ("Bacán", "Máximo elogio de aprobación"),
        ("Churo", "Rizo capilar o caracol"),
        ("Acolitar", "Verbo de solidaridad y compañía"),
        ("Cachas", "Verbo de entendimiento"),
        ("Simón", "Afirmación callejera"),
        ("Lámpara", "Objeto luminoso o situación bochornosa"),
        ("Caleta", "Refugio personal para dormir"),
        ("Camello", "Labor diaria para ganar dinero"),
        ("Pelada", "Sin pelo o pareja sentimental"),
        ("Suco", "Color de pelo claro"),
        ("Mushpa", "Lento de entendimiento (kichwa)"),
        ("Visaje", "Hacer muecas o bulto innecesario"),
        ("Lamparoso", "Le gusta llamar la atención"),
        ("De ley", "Certeza absoluta"),
        ("Canguil", "Maíz que explota"),
        ("Chapa", "Uniformado que cuida (o no)"),
        ("Choro", "Amigo de lo ajeno"),
        ("Sapo", "Anfibio o persona muy viva"),
        ("Once", "El café de la tarde"),
        ("Biela", "Pieza de motor o cerveza"),
        ("Jama", "Sustento alimenticio"),
        ("Ruco", "Dormido profundamente"),
        ("Pana", "Tela o amigo cercano"),
        ("Yunta", "Compañero inseparable de arado"),
        ("Broder", "Anglicismo de hermandad"),
        ("Ñaño", "Hermano de sangre o cariño"),
        ("Vajilla", "Caer pesado o mal"),
        ("Foca", "Hacer el ridículo en público")
    ]
}

DATA_NORMAL = {
    "🐾 Animales": [
        ("León", "Gato gigante con corona capilar"),
        ("Pingüino", "Ave vestida de etiqueta invernal"),
        ("Elefante", "Memoria gigante y nariz manguera"),
        ("Tiburón", "Terror de las aletas en el mar"),
        ("Águila", "Reina de las alturas y la visión"),
        ("Perro", "Lealtad con cuatro patas y cola"),
        ("Gato", "Independencia felina doméstica"),
        ("Dinosaurio", "Lagarto terrible del pasado"),
        ("Canguro", "Boxeador saltarín con bolsillo"),
        ("Jirafa", "La vista más alta de la sabana"),
        ("Oso Polar", "Depredador blanco del hielo"),
        ("Tigre", "Cazador rayado de la jungla"),
        ("Ballena", "Gigante que canta bajo el agua"),
        ("Delfín", "Sonrisa permanente en el océano"),
        ("Gorila", "Espalda plateada de la niebla"),
        ("Mono", "Primate ágil y travieso"),
        ("Serpiente", "Se arrastra y muda de piel"),
        ("Cocodrilo", "Lágrimas falsas y mandíbula fuerte"),
        ("Hipopótamo", "Caballo de río muy peligroso"),
        ("Rinoceronte", "Tanque blindado con cuerno"),
        ("Cebra", "Código de barras con patas"),
        ("Koala", "Dormilón australiano de eucalipto"),
        ("Panda", "Oso bicolor comedor de bambú"),
        ("Lobo", "Aúlla a la luna en manada"),
        ("Zorro", "Astucia roja o ártica"),
        ("Camello", "Barco del desierto con joroba"),
        ("Caballo", "Noble transporte de crin"),
        ("Vaca", "Fábrica de leche y cuero"),
        ("Cerdo", "Inteligente, rosado y de granja"),
        ("Gallina", "Productora de huevos"),
        ("Pato", "Ave acuática que dice cuac"),
        ("Búho", "Vigilante nocturno de ojos grandes"),
        ("Murciélago", "Radar viviente que duerme colgado")
    ],
    "📍 Lugares Comunes": [
        ("Playa", "Frontera entre tierra y mar"),
        ("Escuela", "Fábrica de conocimiento básico"),
        ("Hospital", "Edificio de batas blancas y salud"),
        ("Banco", "Fortaleza del dinero"),
        ("Avión", "Pájaro de metal"),
        ("Cine", "Sala oscura de sueños proyectados"),
        ("Circo", "Carpa de risas y asombro"),
        ("Estación Espacial", "Hogar humano entre estrellas"),
        ("Supermercado", "Laberinto de pasillos y carritos"),
        ("Biblioteca", "Santuario del silencio y papel"),
        ("Gimnasio", "Templo del sudor y el músculo"),
        ("Cementerio", "Ciudad del silencio eterno"),
        ("Restaurante", "Cocina ajena para disfrutar"),
        ("Hotel", "Hogar temporal con servicio"),
        ("Aeropuerto", "Puerto de nubes y despedidas"),
        ("Museo", "Cápsula del tiempo y arte"),
        ("Teatro", "Drama y comedia en vivo"),
        ("Zoológico", "Colección de naturaleza viva"),
        ("Farmacia", "Tienda de remedios"),
        ("Panadería", "Aroma a levadura y horno"),
        ("Cafetería", "Lugar de encuentro y cafeína"),
        ("Universidad", "Alma mater del saber superior"),
        ("Oficina", "Cubículos y trabajo administrativo"),
        ("Cárcel", "Hotel de rejas involuntario"),
        ("Castillo", "Hogar de reyes y fantasmas"),
        ("Estadio", "Coliseo moderno de deportes"),
        ("Iglesia", "Campanario y fe"),
        ("Parque de Diversiones", "Adrenalina mecánica"),
        ("Submarino", "Tubo de acero bajo presión"),
        ("Barco Pirata", "Nave de bandera negra"),
        ("Cueva", "Boca oscura de la tierra")
    ],
    "🍕 Comida Internacional": [
        ("Pizza", "Disco italiano horneado"),
        ("Sushi", "Arte japonés de arroz y mar"),
        ("Hamburguesa", "Icono de comida rápida entre panes"),
        ("Helado", "Felicidad fría y cremosa"),
        ("Paella", "Sartén de arroz valenciano"),
        ("Tacos", "Tortilla doblada con relleno"),
        ("Chocolate", "El regalo de los dioses mayas"),
        ("Ensalada", "Bol de salud verde"),
        ("Espagueti", "Cuerdas comestibles de harina"),
        ("Hot Dog", "Embutido en pan alargado"),
        ("Lasaña", "Edificio de capas de pasta"),
        ("Burrito", "Paquete de harina relleno"),
        ("Curry", "Mezcla de especias india"),
        ("Ramen", "Fideos en caldo complejo"),
        ("Croissant", "Luna creciente de mantequilla"),
        ("Donas", "Toroide dulce y frito"),
        ("Papas Fritas", "Bastones dorados de tubérculo"),
        ("Pollo Frito", "Ave crujiente y dorada"),
        ("Filete", "Corte noble de carne"),
        ("Sopa", "Líquido reconfortante"),
        ("Pastel", "Celebración horneada"),
        ("Galletas", "Discos dulces de masa"),
        ("Sandwich", "Invento del Conde para jugar cartas"),
        ("Arroz Frito", "Wok y granos salteados"),
        ("Kebab", "Carne giratoria vertical"),
        ("Nachos", "Triángulos crujientes para dipear"),
        ("Quesadilla", "Queso fundido en tortilla"),
        ("Fondue", "Olla común para sumergir")
    ],
    "👮 Profesiones": [
        ("Médico", "Reparador de cuerpos humanos"),
        ("Policía", "Uniforme azul y placa"),
        ("Bombero", "Luchador contra el fuego"),
        ("Astronauta", "Explorador del vacío"),
        ("Profesor", "Sembrador de conocimiento"),
        ("Futbolista", "Estrella del balón"),
        ("Cocinero", "Alquimista de sabores"),
        ("Programador", "Traductor de lenguaje máquina"),
        ("Abogado", "Luchador de leyes y juicios"),
        ("Mecánico", "Doctor de motores"),
        ("Dentista", "Arquitecto de sonrisas"),
        ("Enfermero", "Mano derecha de la salud"),
        ("Piloto", "Conductor de nubes"),
        ("Carpintero", "Moldeador de madera"),
        ("Electricista", "Maestro de los cables"),
        ("Fontanero", "Héroe de las tuberías"),
        ("Granjero", "Productor de alimentos"),
        ("Científico", "Buscador de verdades empíricas"),
        ("Pintor", "Creador de imágenes con brocha"),
        ("Músico", "Organizador de sonidos"),
        ("Actor", "Profesional de la mentira escénica"),
        ("Escritor", "Arquitecto de palabras"),
        ("Juez", "Martillo de la justicia"),
        ("Soldado", "Guerrero profesional"),
        ("Arquitecto", "Diseñador de espacios"),
        ("Veterinario", "Médico de pacientes mudos"),
        ("Payaso", "Artista de la risa y el maquillaje"),
        ("Mago", "Ilusionista profesional"),
        ("Detective", "Buscador de pistas ocultas"),
        ("Espía", "Profesional del secreto")
    ],
    "🎸 Objetos": [
        ("Silla", "Trono cotidiano"),
        ("Teléfono", "Conexión de voz a distancia"),
        ("Reloj", "Contador de tiempo"),
        ("Espejo", "Reflejo de la realidad"),
        ("Guitarra", "Caja de resonancia y cuerdas"),
        ("Computadora", "Cerebro de silicio"),
        ("Lápiz", "Grafito envuelto en madera"),
        ("Zapato", "Protección para caminar"),
        ("Bicicleta", "Equilibrio sobre dos ruedas"),
        ("Cuchara", "Transporte de líquidos a la boca"),
        ("Mesa", "Plataforma de cuatro patas"),
        ("Cama", "Mueble de los sueños"),
        ("Lámpara", "Sol artificial doméstico"),
        ("Televisor", "Ventana al mundo electrónico"),
        ("Refrigeradora", "Caja de invierno"),
        ("Microondas", "Calentador de ondas invisibles"),
        ("Lavadora", "Torbellino de limpieza"),
        ("Coche", "Carruaje sin caballos"),
        ("Avión de Juguete", "Réplica voladora"),
        ("Muñeca", "Figura humana inanimada"),
        ("Pelota", "Esfera de juego"),
        ("Libro", "Cerebro de papel"),
        ("Cuaderno", "Memoria externa en blanco"),
        ("Mochila", "Caparazón de carga"),
        ("Gafas", "Escudos para la vista"),
        ("Sombrero", "Techo personal"),
        ("Paraguas", "Escudo contra el agua"),
        ("Llave", "Diente de metal que abre"),
        ("Billetera", "Bolsillo del valor"),
        ("Cámara", "Ojo que congela el tiempo")
    ]
}

# Unimos todo
ALL_DATA = {**DATA_ECUADOR, **DATA_NORMAL}

# --- DISEÑO HTML ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>El Impostor: Ultimate</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #1a202c; color: white; font-family: sans-serif; }
        .btn-press:active { transform: scale(0.98); }
        .fade-in { animation: fadeIn 0.5s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none; height: 20px; width: 20px; border-radius: 50%;
            background: #3b82f6; cursor: pointer; margin-top: -8px; box-shadow: 0 0 5px #000;
        }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%; height: 4px; cursor: pointer; background: #4b5563; border-radius: 2px;
        }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #2d3748; }
        ::-webkit-scrollbar-thumb { background: #4a5568; border-radius: 4px; }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
    <div class="w-full max-w-md bg-gray-800 rounded-2xl shadow-2xl overflow-hidden border border-gray-700 fade-in flex flex-col max-h-[90vh]">

        <!-- Header -->
        <div class="bg-gray-900 p-4 text-center border-b border-gray-700 flex justify-between items-center shrink-0 z-10">
            <h1 class="text-xl font-bold text-blue-400 mx-auto">
                <i class="fas fa-user-secret mr-2"></i>El Impostor
            </h1>
            {% if step != 'setup' and step != 'dict_auth' %}
            <a href="/" class="text-gray-500 hover:text-white text-xs"><i class="fas fa-times"></i> Salir</a>
            {% endif %}
        </div>

        <div class="p-6 overflow-y-auto grow">

            <!-- PASO 1: CONFIGURACIÓN -->
            {% if step == 'setup' %}
            <form action="/setup" method="POST" class="space-y-6">

                <!-- Selector de MODO -->
                <div class="bg-gray-700/50 p-3 rounded-xl border border-gray-600">
                    <label class="block text-gray-400 mb-2 font-bold text-xs uppercase tracking-widest">Modo de Juego</label>
                    <div class="flex gap-2">
                        <label class="flex-1 cursor-pointer">
                            <input type="radio" name="game_mode" value="ecu" class="peer hidden" checked onchange="updateCategories()">
                            <div class="text-center py-2 rounded-lg border border-gray-600 peer-checked:bg-yellow-600 peer-checked:border-yellow-400 peer-checked:text-white text-gray-400 transition">
                                🇪🇨 Ecuador
                            </div>
                        </label>
                        <label class="flex-1 cursor-pointer">
                            <input type="radio" name="game_mode" value="norm" class="peer hidden" onchange="updateCategories()">
                            <div class="text-center py-2 rounded-lg border border-gray-600 peer-checked:bg-blue-600 peer-checked:border-blue-400 peer-checked:text-white text-gray-400 transition">
                                🌎 Normal
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Categoría -->
                <div>
                    <label class="block text-blue-400 mb-2 font-bold text-sm uppercase tracking-wider">
                        <i class="fas fa-list-ul mr-1"></i> Categoría
                    </label>
                    <select id="category-select" name="category" class="w-full bg-gray-700 rounded-lg p-3 text-white border border-gray-600 focus:border-blue-500 outline-none">
                        <!-- Se llena con JS -->
                    </select>
                </div>

                <!-- Slider Probabilidad -->
                <div class="bg-gray-700/50 p-4 rounded-xl border border-gray-600">
                    <label class="block text-gray-400 mb-2 font-bold text-xs uppercase tracking-widest flex justify-between">
                        <span><i class="fas fa-dice mr-1"></i> Doble Impostor (5+ jug)</span>
                        <span id="prob-val" class="text-white">0%</span>
                    </label>
                    <input type="range" name="impostor_prob" min="0" max="100" value="0" step="10" 
                           oninput="document.getElementById('prob-val').innerText = this.value + '%'">
                </div>

                <!-- Toggle Pistas (Nuevo) -->
                <div class="bg-gray-700/50 p-4 rounded-xl border border-gray-600 flex items-center justify-between">
                    <label class="text-gray-400 font-bold text-xs uppercase tracking-widest flex items-center">
                        <i class="fas fa-lightbulb mr-2 text-yellow-500"></i> Habilitar Pistas
                    </label>
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" name="enable_hints" value="yes" class="sr-only peer">
                        <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-yellow-500"></div>
                    </label>
                </div>

                <!-- Nombres -->
                <div>
                    <label class="block text-gray-400 mb-2 font-bold text-sm uppercase tracking-wider">
                        <i class="fas fa-users mr-1"></i> Jugadores
                    </label>
                    <div id="players-container" class="space-y-2 max-h-48 overflow-y-auto pr-1">
                        <!-- Campos Iniciales -->
                        <div class="flex gap-2 items-center">
                             <input type="text" name="player_name" placeholder="Jugador 1 (Opcional)" class="w-full bg-gray-700 p-3 rounded-lg border border-gray-600 focus:border-blue-500 outline-none text-sm">
                             <button type="button" onclick="removePlayer(this)" class="text-red-400 hover:text-red-300 p-2"><i class="fas fa-trash"></i></button>
                        </div>
                        <div class="flex gap-2 items-center">
                             <input type="text" name="player_name" placeholder="Jugador 2 (Opcional)" class="w-full bg-gray-700 p-3 rounded-lg border border-gray-600 focus:border-blue-500 outline-none text-sm">
                             <button type="button" onclick="removePlayer(this)" class="text-red-400 hover:text-red-300 p-2"><i class="fas fa-trash"></i></button>
                        </div>
                        <div class="flex gap-2 items-center">
                             <input type="text" name="player_name" placeholder="Jugador 3 (Opcional)" class="w-full bg-gray-700 p-3 rounded-lg border border-gray-600 focus:border-blue-500 outline-none text-sm">
                             <button type="button" onclick="removePlayer(this)" class="text-red-400 hover:text-red-300 p-2"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>

                    <button type="button" onclick="addPlayerField()" class="mt-2 text-xs text-blue-400 hover:text-blue-300 font-bold w-full border border-dashed border-gray-600 p-2 rounded hover:bg-gray-700 transition">
                        <i class="fas fa-plus-circle"></i> Agregar Jugador
                    </button>
                    <p class="text-xs text-gray-500 mt-2 text-center">* Si dejas el nombre vacío, se pondrá automático.</p>
                </div>

                <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-blue-800 hover:from-blue-500 hover:to-blue-700 text-white font-bold py-4 rounded-xl transition btn-press shadow-lg shadow-blue-900/50">
                    JUGAR
                </button>
            </form>

            <div class="mt-6 pt-4 border-t border-gray-700 text-center">
                <a href="/dictionary" class="text-gray-400 hover:text-white text-sm font-semibold transition">
                    <i class="fas fa-lock mr-1"></i> Ver todas las palabras (Admin)
                </a>
            </div>

            <script>
                const catsEcu = {{ cat_ecu | tojson }};
                const catsNorm = {{ cat_norm | tojson }};

                function updateCategories() {
                    const mode = document.querySelector('input[name="game_mode"]:checked').value;
                    const select = document.getElementById('category-select');
                    select.innerHTML = '';
                    const list = (mode === 'ecu') ? catsEcu : catsNorm;
                    list.forEach(cat => {
                        const opt = document.createElement('option');
                        opt.value = cat;
                        opt.innerText = cat;
                        select.appendChild(opt);
                    });
                }

                function addPlayerField() {
                    const container = document.getElementById('players-container');
                    const count = container.children.length + 1;

                    const div = document.createElement('div');
                    div.className = 'flex gap-2 items-center fade-in';
                    div.innerHTML = `
                        <input type="text" name="player_name" placeholder="Jugador ${count} (Opcional)" 
                               class="w-full bg-gray-700 p-3 rounded-lg border border-gray-600 focus:border-blue-500 outline-none text-sm">
                        <button type="button" onclick="removePlayer(this)" class="text-red-400 hover:text-red-300 p-2 transition">
                            <i class="fas fa-trash"></i>
                        </button>
                    `;
                    container.appendChild(div);
                    container.scrollTop = container.scrollHeight;
                }

                function removePlayer(btn) {
                    const container = document.getElementById('players-container');
                    if (container.children.length <= 3) {
                        alert("Mínimo 3 jugadores ñaño, si no, no tiene chiste.");
                        return;
                    }
                    btn.parentElement.remove();
                }

                updateCategories();
            </script>
            {% endif %}

            <!-- AUTH DICCIONARIO -->
            {% if step == 'dict_auth' %}
            <div class="text-center space-y-6 pt-10">
                <div class="text-5xl text-red-500"><i class="fas fa-lock"></i></div>
                <h2 class="text-2xl font-bold text-white">Zona Protegida</h2>
                <p class="text-gray-400">Ingresa la clave para ver las palabras.</p>

                <form action="/dictionary/login" method="POST" class="space-y-4">
                    <input type="password" name="password" placeholder="Clave de Admin" 
                           class="bg-gray-700 p-4 rounded-xl text-center text-white text-xl w-full border border-gray-600 focus:border-red-500 outline-none">

                    {% if error %}
                    <p class="text-red-400 text-sm font-bold">{{ error }}</p>
                    {% endif %}

                    <button type="submit" class="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-4 rounded-xl transition btn-press">
                        DESBLOQUEAR
                    </button>
                </form>

                <a href="/" class="block text-gray-500 mt-4 text-sm">Cancelar</a>
            </div>
            {% endif %}

            <!-- DICCIONARIO -->
            {% if step == 'dictionary' %}
            <div class="space-y-6">
                <div class="flex items-center justify-between">
                    <h2 class="text-xl font-bold text-white">📚 Diccionario</h2>
                    <a href="/" class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm transition">
                        <i class="fas fa-arrow-left"></i> Volver
                    </a>
                </div>

                <div class="bg-green-900/30 border border-green-500/30 p-2 rounded text-center text-green-300 text-xs mb-4">
                    <i class="fas fa-unlock mr-1"></i> Acceso concedido
                </div>

                <div>
                    <h3 class="text-yellow-500 font-bold mb-3 border-b border-gray-700 pb-1">🇪🇨 Modo Ecuador</h3>
                    <div class="space-y-3">
                        {% for cat, words in data_ecu.items() %}
                        <div class="bg-gray-700/50 rounded-lg p-3">
                            <h4 class="text-blue-300 font-bold text-sm mb-2">{{ cat }}</h4>
                            <div class="flex flex-wrap gap-2">
                                {% for w, hint in words %}
                                <div class="text-xs bg-gray-800 px-2 py-1 rounded text-gray-300 border border-gray-600 flex items-center gap-2" title="{{ hint }}">
                                    <span>{{ w }}</span>
                                    <span class="text-gray-500 italic">({{ hint }})</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                <div>
                    <h3 class="text-blue-500 font-bold mb-3 border-b border-gray-700 pb-1 pt-4">🌎 Modo Normal</h3>
                    <div class="space-y-3">
                        {% for cat, words in data_norm.items() %}
                        <div class="bg-gray-700/50 rounded-lg p-3">
                            <h4 class="text-green-300 font-bold text-sm mb-2">{{ cat }}</h4>
                            <div class="flex flex-wrap gap-2">
                                {% for w, hint in words %}
                                <div class="text-xs bg-gray-800 px-2 py-1 rounded text-gray-300 border border-gray-600 flex items-center gap-2" title="{{ hint }}">
                                    <span>{{ w }}</span>
                                    <span class="text-gray-500 italic">({{ hint }})</span>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- ESPERA -->
            {% if step == 'wait' %}
            <div class="text-center space-y-8 py-4">
                <div class="w-24 h-24 bg-gray-700 rounded-full flex items-center justify-center mx-auto border-4 border-yellow-500 shadow-xl shadow-yellow-500/20 animate-pulse">
                    <span class="text-4xl">🤫</span>
                </div>
                <div>
                    <h2 class="text-xl text-gray-400">Turno de</h2>
                    <h1 class="text-4xl font-bold text-white mt-1 uppercase tracking-wider">{{ current_name }}</h1>
                </div>
                <div class="bg-yellow-900/30 border border-yellow-700/50 p-4 rounded-lg text-yellow-200 text-sm mx-4">
                    <i class="fas fa-eye-slash mr-1"></i> Asegúrate de que nadie mire.
                </div>
                <a href="/reveal/card" class="block w-full bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-4 rounded-xl transition btn-press">
                    VER MI ROL
                </a>
            </div>
            {% endif %}

            <!-- VER CARTA -->
            {% if step == 'card' %}
            <div class="text-center space-y-6">
                <div class="text-gray-400 text-xs uppercase tracking-widest">Rol de {{ current_name }}</div>

                <div class="p-8 rounded-2xl border-4 {{ 'border-red-500 bg-red-900/20' if is_impostor else 'border-green-500 bg-green-900/20' }} relative overflow-hidden shadow-2xl">

                    {% if is_impostor %}
                        <div class="absolute -right-6 -top-6 text-9xl text-red-500/10 rotate-12"><i class="fas fa-spider"></i></div>

                        <i class="fas fa-mask text-7xl text-red-500 mb-4 relative z-10 drop-shadow-lg"></i>
                        <h2 class="text-4xl font-black text-red-500 mb-2 uppercase relative z-10 tracking-tighter">IMPOSTOR</h2>
                        <p class="text-gray-300 relative z-10 font-bold">¡Disimula!</p>
                        <p class="text-sm text-red-300 mt-2 relative z-10">No sabes la palabra.</p>

                        <!-- Botón de Pista (SOLO IMPOSTOR) -->
                        {% if enable_hints %}
                        <div class="mt-4 pt-4 border-t border-red-500/30 relative z-10">
                            <p class="text-xs text-red-300 mb-2">Ayuda para mentir:</p>
                            <button onclick="document.getElementById('secret-hint').classList.toggle('hidden')" 
                                    class="text-xs text-yellow-400 hover:text-yellow-300 font-bold focus:outline-none transition border border-yellow-500/50 px-3 py-1 rounded-full bg-yellow-900/20">
                                <i class="fas fa-lightbulb mr-1"></i> VER PISTA
                            </button>
                            <p id="secret-hint" class="hidden text-sm text-yellow-200 italic mt-2 transition-all bg-black/40 p-2 rounded">
                                {{ hint }}
                            </p>
                        </div>
                        {% endif %}

                        {% if num_impostors > 1 %}
                        <div class="mt-4 bg-red-900/50 p-2 rounded border border-red-500/30 text-xs text-red-200 animate-pulse relative z-10">
                             ⚠️ Hay otro impostor...
                        </div>
                        {% endif %}

                    {% else %}
                        <div class="absolute -right-6 -top-6 text-9xl text-green-500/10 rotate-12"><i class="fas fa-shield-alt"></i></div>

                        <i class="fas fa-user-check text-7xl text-green-500 mb-4 relative z-10 drop-shadow-lg"></i>
                        <h2 class="text-2xl font-bold text-green-400 mb-2 relative z-10 uppercase">Ciudadano</h2>

                        <div class="bg-gray-900/80 p-4 rounded-xl mt-6 border border-green-500/30 relative z-10 shadow-inner">
                            <p class="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Palabra Secreta</p>
                            <p class="text-2xl font-black text-white tracking-wide break-words leading-none">{{ word }}</p>
                        </div>
                    {% endif %}
                </div>

                <a href="/next_player" class="block w-full bg-gray-600 hover:bg-gray-500 text-white font-bold py-4 rounded-xl transition btn-press">
                    {{ '¡A JUGAR!' if is_last else 'OCULTAR Y SIGUIENTE ⏩' }}
                </a>
            </div>
            {% endif %}

            <!-- JUEGO -->
            {% if step == 'game' %}
            <div class="text-center space-y-5">
                <div class="inline-block px-4 py-2 bg-blue-900/40 rounded-full text-blue-300 text-xs border border-blue-800">
                    Tema: <strong class="text-white">{{ category }}</strong>
                </div>

                <h2 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-blue-400 to-red-400 drop-shadow-sm">
                    ¡A DEBATIR!
                </h2>

                <div class="bg-gray-700/30 p-4 rounded-xl border border-gray-600">
                    <h3 class="text-gray-400 text-xs uppercase mb-3 font-bold">Jugadores</h3>
                    <div class="flex flex-wrap gap-2 justify-center">
                        {% for p in players %}
                        <span class="bg-gray-800 px-3 py-1 rounded-lg text-sm text-gray-300 border border-gray-600 shadow-sm">
                            <i class="fas fa-user text-xs mr-1 text-gray-500"></i> {{ p }}
                        </span>
                        {% endfor %}
                    </div>
                </div>

                <div class="py-2">
                    <div id="timer" class="text-6xl font-mono font-bold text-yellow-500 drop-shadow-lg">05:00</div>
                    <p class="text-xs text-gray-500 mt-1 uppercase tracking-widest">Tiempo Restante</p>
                </div>

                <a href="/result" class="block w-full bg-red-600 hover:bg-red-500 text-white font-bold py-4 rounded-xl transition btn-press shadow-lg shadow-red-900/50 mt-4">
                    🛑 TERMINAR Y REVELAR
                </a>
            </div>
            <script>
                let timeLeft = 300;
                const timerEl = document.getElementById('timer');
                setInterval(() => {
                    if(timeLeft <= 0) return;
                    timeLeft--;
                    const m = Math.floor(timeLeft / 60).toString().padStart(2, '0');
                    const s = (timeLeft % 60).toString().padStart(2, '0');
                    timerEl.textContent = `${m}:${s}`;
                    if(timeLeft < 60) timerEl.classList.add('text-red-500');
                }, 1000);
            </script>
            {% endif %}

            <!-- RESULTADO -->
            {% if step == 'result' %}
            <div class="text-center space-y-8">
                <h2 class="text-3xl font-bold text-white mb-2">La Verdad</h2>

                <div class="bg-gradient-to-b from-gray-700 to-gray-800 p-8 rounded-3xl border border-gray-600 shadow-2xl relative overflow-hidden">

                    <p class="text-gray-400 text-xs mb-4 uppercase tracking-widest font-bold">Los Impostores eran</p>

                    {% for name in impostor_names %}
                        <div class="text-4xl font-black text-red-500 mb-2 drop-shadow-md animate-pulse">{{ name }}</div>
                    {% endfor %}
                </div>

                <div class="bg-gray-800 p-4 rounded-xl border border-gray-700 flex flex-col items-center">
                    <p class="text-gray-500 text-[10px] uppercase mb-1">La palabra era</p>
                    <p class="text-2xl font-bold text-blue-300">{{ word }}</p>
                </div>

                <a href="/" class="block w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition btn-press mt-8 shadow-lg">
                    🔄 JUGAR OTRA VEZ
                </a>
            </div>
            {% endif %}

        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    session.clear()
    return render_template_string(HTML_TEMPLATE, step='setup',
                                  cat_ecu=list(DATA_ECUADOR.keys()),
                                  cat_norm=list(DATA_NORMAL.keys()))


@app.route('/dictionary')
def dictionary():
    if session.get('dict_access'):
        return render_template_string(HTML_TEMPLATE, step='dictionary',
                                      data_ecu=DATA_ECUADOR,
                                      data_norm=DATA_NORMAL)
    else:
        return render_template_string(HTML_TEMPLATE, step='dict_auth')


@app.route('/dictionary/login', methods=['POST'])
def dictionary_login():
    password = request.form.get('password')
    if password == DICT_PASSWORD:
        session['dict_access'] = True
        return redirect(url_for('dictionary'))
    else:
        return render_template_string(HTML_TEMPLATE, step='dict_auth', error="Clave Incorrecta ñaño")


@app.route('/setup', methods=['POST'])
def setup():
    # 1. NOMBRES POR DEFECTO
    raw_names = request.form.getlist('player_name')
    players = []

    for i, name in enumerate(raw_names):
        clean_name = name.strip()
        if not clean_name:
            clean_name = f"Jugador {i + 1}"
        players.append(clean_name)

    if len(players) < 3:
        return redirect(url_for('home'))

    # 2. SELECCIÓN DE PALABRA Y PISTA
    category = request.form.get('category')
    # Obtenemos la lista de tuplas (palabra, pista)
    words = ALL_DATA.get(category, [("Error", "Sin pista")])

    selected_pair = random.choice(words)
    secret_word = selected_pair[0]
    secret_hint = selected_pair[1]

    # 3. LÓGICA DE IMPOSTORES
    prob_double = int(request.form.get('impostor_prob', 0))
    num_impostors = 1

    if len(players) >= 5:
        chance = random.randint(1, 100)
        if chance <= prob_double:
            num_impostors = 2

    impostor_indices = random.sample(range(len(players)), num_impostors)

    session['players'] = players
    session['category'] = category
    session['secret_word'] = secret_word
    session['secret_hint'] = secret_hint
    session['impostor_indices'] = impostor_indices
    session['current_idx'] = 0

    return redirect(url_for('reveal_wait'))


@app.route('/reveal/wait')
def reveal_wait():
    current_idx = session.get('current_idx')
    players = session.get('players')

    if current_idx >= len(players):
        return redirect(url_for('game_phase'))

    return render_template_string(HTML_TEMPLATE,
                                  step='wait',
                                  current_name=players[current_idx])


@app.route('/reveal/card')
def reveal_card():
    current_idx = session.get('current_idx')
    impostor_indices = session.get('impostor_indices')
    players = session.get('players')

    is_impostor = (current_idx in impostor_indices)
    is_last = (current_idx == len(players) - 1)

    return render_template_string(HTML_TEMPLATE,
                                  step='card',
                                  current_name=players[current_idx],
                                  is_impostor=is_impostor,
                                  num_impostors=len(impostor_indices),
                                  word=session.get('secret_word'),
                                  hint=session.get('secret_hint'),
                                  is_last=is_last)


@app.route('/next_player')
def next_player():
    session['current_idx'] += 1
    return redirect(url_for('reveal_wait'))


@app.route('/game')
def game_phase():
    return render_template_string(HTML_TEMPLATE,
                                  step='game',
                                  players=session.get('players'),
                                  category=session.get('category'))


@app.route('/result')
def result():
    players = session.get('players')
    impostor_indices = session.get('impostor_indices')
    impostor_names = [players[i] for i in impostor_indices]

    return render_template_string(HTML_TEMPLATE,
                                  step='result',
                                  impostor_names=impostor_names,
                                  word=session.get('secret_word'))


if __name__ == '__main__':
    # Usamos 5001 localmente para evitar conflictos
    app.run(debug=True, port=5001)
