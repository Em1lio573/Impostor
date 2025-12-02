from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "clave_secreta_ecuador_master_mega_123"

# --- DATOS DEL JUEGO (BASE DE DATOS AMPLIADA) ---
DATA_ECUADOR = {
    "🇪🇨 Comida Típica": [
        "Encebollado", "Cuy Asado", "Bolón de Verde", "Fanesca", "Guatita", 
        "Ceviche de Camarón", "Hornado", "Llapingachos", "Morocho", 
        "Tigrillo", "Locro de Papa", "Tripa Mishqui", "Humitas", "Chugchucaras",
        "Yahuarlocro", "Seco de Pollo", "Seco de Chivo", "Chaulafan", "Muchines de Yuca",
        "Corviche", "Cazuela de Pescado", "Sango de Camarón", "Caldo de Salchicha",
        "Empanada de Viento", "Empanada de Morocho", "Pristiños", "Higos con Queso",
        "Espumilla", "Colada Morada", "Pan de Yuca", "Chifles", "Patacones",
        "Salprieta", "Viche Manabita", "Tongas", "Ayampaco", "Maito"
    ],
    "🇪🇨 Lugares Típicos": [
        "Islas Galápagos", "Mitad del Mundo", "El Panecillo", "Malecón 2000", 
        "Cotopaxi", "Baños de Agua Santa", "Montañita", "La Ronda", 
        "Parque La Carolina", "Chimborazo", "Laguna del Quilotoa", "Mercado Artesanal",
        "Catedral de Cuenca", "Parque Nacional Yasuní", "Nariz del Diablo", 
        "Ruinas de Ingapirca", "Laguna de Cuicocha", "El Cajas", "Puerto Ayora",
        "Playa de los Frailes", "Malecón del Salado", "Cerro Santa Ana", "Teleférico de Quito",
        "Basílica del Voto Nacional", "Parque Centenario", "Las Peñas", "Mindo",
        "Papallacta", "Salinas", "Atacames", "Tena", "Puyo"
    ],
    "🍻 Farra y Chupa": [
        "Pilsener", "Club Verde", "Zhumir", "Pájaro Azul", "Aguardiente", 
        "Michelada", "Canelazo", "Norteño", "Biela", "Caña Manabita",
        "Jager", "Punta", "Chicha", "Guanchaca", "Cristal", "Switch",
        "Rompe Colchón", "7 Espíritus", "Blue", "Corona", "Vino Hervido"
    ],
    "🛒 Marcas Ecuatorianas": [
        "Marathon", "Supermaxi", "Mi Comisariato", "Banco Pichincha", 
        "Tía", "Sweet & Coffee", "Manicho", "Tango", "Tropical", "Güitig",
        "Fioravanti", "Pinguino", "Deja", "Lomito", "Ruffles (versión local)",
        "Toni", "Nutri Leche", "Indurama", "Plumrose", "Real", "Vanamps",
        "Sumesa", "Ile", "La Tablita del Tártaro", "Candu", "Buestán"
    ],
    "🗣️ Jerga Ecuatoriana": [
        "Chuchaqui", "Cholo", "Aniñado", "Mandarina", "Bacán", 
        "Churo", "Acolitar", "Cachas", "Simón", "Lámpara",
        "Caleta", "Camello", "Pelada", "Suco", "Mushpa", 
        "Visaje", "Lamparoso", "De ley", "Canguil", "Chapa",
        "Choro", "Sapo", "Once", "Biela", "Jama", "Ruco",
        "Pana", "Yunta", "Broder", "Ñaño", "Vajilla", "Foca"
    ]
}

DATA_NORMAL = {
    "🐾 Animales": [
        "León", "Pingüino", "Elefante", "Tiburón", "Águila", 
        "Perro", "Gato", "Dinosaurio", "Canguro", "Jirafa",
        "Oso Polar", "Tigre", "Ballena", "Delfín", "Gorila", "Mono",
        "Serpiente", "Cocodrilo", "Hipopótamo", "Rinoceronte", "Cebra",
        "Koala", "Panda", "Lobo", "Zorro", "Camello", "Caballo",
        "Vaca", "Cerdo", "Gallina", "Pato", "Búho", "Murciélago"
    ],
    "📍 Lugares Comunes": [
        "Playa", "Escuela", "Hospital", "Banco", "Avión", 
        "Cine", "Circo", "Estación Espacial", "Supermercado", 
        "Biblioteca", "Gimnasio", "Cementerio", "Restaurante",
        "Hotel", "Aeropuerto", "Museo", "Teatro", "Zoológico",
        "Farmacia", "Panadería", "Cafetería", "Universidad",
        "Oficina", "Cárcel", "Castillo", "Estadio", "Iglesia",
        "Parque de Diversiones", "Submarino", "Barco Pirata", "Cueva"
    ],
    "🍕 Comida Internacional": [
        "Pizza", "Sushi", "Hamburguesa", "Helado", "Paella", 
        "Tacos", "Chocolate", "Ensalada", "Espagueti", "Hot Dog",
        "Lasaña", "Burrito", "Curry", "Ramen", "Croissant",
        "Donas", "Papas Fritas", "Pollo Frito", "Filete",
        "Sopa", "Pastel", "Galletas", "Sandwich", "Arroz Frito",
        "Kebab", "Nachos", "Quesadilla", "Fondue"
    ],
    "👮 Profesiones": [
        "Médico", "Policía", "Bombero", "Astronauta", "Profesor", 
        "Futbolista", "Cocinero", "Programador", "Abogado", "Mecánico",
        "Dentista", "Enfermero", "Piloto", "Carpintero", "Electricista",
        "Fontanero", "Granjero", "Científico", "Pintor", "Músico",
        "Actor", "Escritor", "Juez", "Soldado", "Arquitecto",
        "Veterinario", "Payaso", "Mago", "Detective", "Espía"
    ],
    "🎸 Objetos": [
        "Silla", "Teléfono", "Reloj", "Espejo", "Guitarra", 
        "Computadora", "Lápiz", "Zapato", "Bicicleta", "Cuchara",
        "Mesa", "Cama", "Lámpara", "Televisor", "Refrigeradora",
        "Microondas", "Lavadora", "Coche", "Avión de Juguete", "Muñeca",
        "Pelota", "Libro", "Cuaderno", "Mochila", "Gafas",
        "Sombrero", "Paraguas", "Llave", "Billetera", "Cámara"
    ]
}

# Unimos todo para buscar fácil la palabra secreta
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
            {% if step != 'setup' and step != 'dictionary' %}
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

                <!-- Nombres -->
                <div>
                    <label class="block text-gray-400 mb-2 font-bold text-sm uppercase tracking-wider">
                        <i class="fas fa-users mr-1"></i> Jugadores
                    </label>
                    <div id="players-container" class="space-y-2 max-h-48 overflow-y-auto pr-1">
                        <!-- Campos Iniciales (Ahora dinámicos para poder borrarlos si quieres) -->
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
                    <i class="fas fa-book mr-1"></i> Ver todas las palabras
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

            <!-- DICCIONARIO -->
            {% if step == 'dictionary' %}
            <div class="space-y-6">
                <div class="flex items-center justify-between">
                    <h2 class="text-xl font-bold text-white">📚 Diccionario</h2>
                    <a href="/" class="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm transition">
                        <i class="fas fa-arrow-left"></i> Volver
                    </a>
                </div>
                <div>
                    <h3 class="text-yellow-500 font-bold mb-3 border-b border-gray-700 pb-1">🇪🇨 Modo Ecuador</h3>
                    <div class="space-y-3">
                        {% for cat, words in data_ecu.items() %}
                        <div class="bg-gray-700/50 rounded-lg p-3">
                            <h4 class="text-blue-300 font-bold text-sm mb-2">{{ cat }}</h4>
                            <div class="flex flex-wrap gap-2">
                                {% for w in words %}
                                <span class="text-xs bg-gray-800 px-2 py-1 rounded text-gray-300 border border-gray-600">{{ w }}</span>
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
                                {% for w in words %}
                                <span class="text-xs bg-gray-800 px-2 py-1 rounded text-gray-300 border border-gray-600">{{ w }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                <div class="text-center pt-4">
                    <a href="/" class="block w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition btn-press">
                        Ir al Juego
                    </a>
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
                        
                        {% if num_impostors > 1 %}
                        <div class="mt-4 bg-red-900/50 p-2 rounded border border-red-500/30 text-xs text-red-200 animate-pulse">
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
    return render_template_string(HTML_TEMPLATE, step='dictionary', 
                                  data_ecu=DATA_ECUADOR, 
                                  data_norm=DATA_NORMAL)

@app.route('/setup', methods=['POST'])
def setup():
    # --- LOGICA DE NOMBRES POR DEFECTO ---
    raw_names = request.form.getlist('player_name')
    players = []
    
    # Recorremos cada input. Si está vacío, asignamos "Jugador X"
    for i, name in enumerate(raw_names):
        clean_name = name.strip()
        if not clean_name:
            clean_name = f"Jugador {i + 1}"
        players.append(clean_name)
    
    # Filtramos por si acaso quedara algo raro, pero con la lógica de arriba
    # siempre tendremos nombres. Solo aseguramos mínimo 3.
    if len(players) < 3:
        # Si por alguna razón fallara, redirigimos
        return redirect(url_for('home'))

    # Configuración del juego
    category = request.form.get('category')
    words = ALL_DATA.get(category, ["Error"])
    secret_word = random.choice(words)
    
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
    print("Iniciando juego en: http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
