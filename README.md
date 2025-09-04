<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockMaster - Gestion de Stock</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#4F46E5',
                        secondary: '#10B981',
                        danger: '#EF4444',
                        warning: '#F59E0B',
                        info: '#3B82F6'
                    }
                }
            }
        }
    </script>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <script src="https://unpkg.com/feather-icons"></script>
    <style>
        .sidebar {
            transition: all 0.3s ease;
        }
        .sidebar-collapsed {
            width: 80px;
        }
        .sidebar-expanded {
            width: 260px;
        }
        .main-content {
            transition: margin-left 0.3s ease;
        }
        .content-expanded {
            margin-left: 260px;
        }
        .content-collapsed {
            margin-left: 80px;
        }
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                z-index: 50;
            }
            .sidebar-expanded {
                width: 260px;
            }
            .main-content {
                margin-left: 0 !important;
            }
        }
    </style>
</head>
<body class="bg-gray-50">
    <div id="app" class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <div class="sidebar sidebar-expanded bg-white shadow-md">
            <div class="flex items-center justify-between p-4 border-b">
                <div class="flex items-center space-x-2">
                    <i data-feather="box" class="text-primary w-6 h-6"></i>
                    <span class="text-xl font-bold text-gray-800">StockMaster</span>
                </div>
                <button id="toggle-sidebar" class="text-gray-500 hover:text-gray-700">
                    <i data-feather="chevron-left"></i>
                </button>
            </div>
            <nav class="p-4 space-y-1">
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg bg-primary/10 text-primary">
                    <i data-feather="home"></i>
                    <span>Tableau de bord</span>
                </a>
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                    <i data-feather="package"></i>
                    <span>Produits</span>
                </a>
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                    <i data-feather="layers"></i>
                    <span>Catégories</span>
                </a>
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                    <i data-feather="activity"></i>
                    <span>Mouvements</span>
                </a>
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                    <i data-feather="bell"></i>
                    <span>Alertes</span>
                </a>
                <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                    <i data-feather="file-text"></i>
                    <span>Rapports</span>
                </a>
                <div class="pt-4 border-t">
                    <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                        <i data-feather="settings"></i>
                        <span>Paramètres</span>
                    </a>
                    <a href="#" class="flex items-center space-x-3 p-2 rounded-lg text-gray-600 hover:bg-gray-100">
                        <i data-feather="log-out"></i>
                        <span>Déconnexion</span>
                    </a>
                </div>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="main-content content-expanded flex-1 flex flex-col overflow-hidden">
            <!-- Top Navigation -->
            <header class="bg-white shadow-sm">
                <div class="flex items-center justify-between p-4">
                    <div class="flex items-center space-x-4">
                        <button id="mobile-menu-button" class="md:hidden text-gray-500">
                            <i data-feather="menu"></i>
                        </button>
                        <h1 class="text-xl font-semibold text-gray-800">Tableau de bord</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <div class="relative">
                            <button class="text-gray-500 hover:text-gray-700">
                                <i data-feather="bell"></i>
                                <span class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
                            </button>
                        </div>
                        <div class="flex items-center space-x-2">
                            <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white">
                                <span>AD</span>
                            </div>
                            <span class="hidden md:inline text-sm font-medium">Admin</span>
                        </div>
                    </div>
                </div>
            </header>

            <!-- Page Content -->
            <main class="flex-1 overflow-y-auto p-4">
                <!-- Stats Cards -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-500">Produits en stock</p>
                                <p class="text-2xl font-bold">1,248</p>
                            </div>
                            <div class="p-3 rounded-full bg-blue-50 text-blue-500">
                                <i data-feather="package"></i>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-500">Stocks faibles</p>
                                <p class="text-2xl font-bold text-warning">24</p>
                            </div>
                            <div class="p-3 rounded-full bg-yellow-50 text-yellow-500">
                                <i data-feather="alert-triangle"></i>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-500">Produits expirés</p>
                                <p class="text-2xl font-bold text-danger">8</p>
                            </div>
                            <div class="p-3 rounded-full bg-red-50 text-red-500">
                                <i data-feather="alert-octagon"></i>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm text-gray-500">Mouvements aujourd'hui</p>
                                <p class="text-2xl font-bold">42</p>
                            </div>
                            <div class="p-3 rounded-full bg-green-50 text-green-500">
                                <i data-feather="activity"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recent Activity and Low Stock -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-lg font-semibold">Activité récente</h2>
                            <button class="text-sm text-primary hover:underline">Voir tout</button>
                        </div>
                        <div class="space-y-4">
                            <div class="flex items-start space-x-3">
                                <div class="p-2 rounded-full bg-blue-50 text-blue-500">
                                    <i data-feather="plus" class="w-4 h-4"></i>
                                </div>
                                <div>
                                    <p class="text-sm font-medium">Nouveau produit ajouté</p>
                                    <p class="text-xs text-gray-500">Aspirateur Dyson V11 - 15 unités</p>
                                    <p class="text-xs text-gray-400">Il y a 2 minutes</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <div class="p-2 rounded-full bg-green-50 text-green-500">
                                    <i data-feather="arrow-up" class="w-4 h-4"></i>
                                </div>
                                <div>
                                    <p class="text-sm font-medium">Entrée de stock</p>
                                    <p class="text-xs text-gray-500">+50 écouteurs sans fil Sony</p>
                                    <p class="text-xs text-gray-400">Il y a 1 heure</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <div class="p-2 rounded-full bg-red-50 text-red-500">
                                    <i data-feather="arrow-down" class="w-4 h-4"></i>
                                </div>
                                <div>
                                    <p class="text-sm font-medium">Sortie de stock</p>
                                    <p class="text-xs text-gray-500">-12 smartphones Samsung Galaxy S22</p>
                                    <p class="text-xs text-gray-400">Il y a 3 heures</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-lg font-semibold">Stocks faibles</h2>
                            <button class="text-sm text-primary hover:underline">Voir tout</button>
                        </div>
                        <div class="space-y-3">
                            <div class="flex items-center justify-between p-2 bg-yellow-50 rounded">
                                <div>
                                    <p class="text-sm font-medium">Batteries externes Anker</p>
                                    <p class="text-xs text-gray-500">5 restantes (seuil: 10)</p>
                                </div>
                                <button class="text-xs text-primary hover:underline">Commander</button>
                            </div>
                            <div class="flex items-center justify-between p-2 bg-yellow-50 rounded">
                                <div>
                                    <p class="text-sm font-medium">Câbles USB-C</p>
                                    <p class="text-xs text-gray-500">3 restants (seuil: 15)</p>
                                </div>
                                <button class="text-xs text-primary hover:underline">Commander</button>
                            </div>
                            <div class="flex items-center justify-between p-2 bg-red-50 rounded">
                                <div>
                                    <p class="text-sm font-medium">Écouteurs Bluetooth</p>
                                    <p class="text-xs text-gray-500">0 restants (seuil: 5)</p>
                                </div>
                                <button class="text-xs text-primary hover:underline">Commander</button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script>
        // Initialize AOS animations
        AOS.init();
        
        // Initialize feather icons
        feather.replace();
        
        // Toggle sidebar
        const toggleSidebar = document.getElementById('toggle-sidebar');
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        
        toggleSidebar.addEventListener('click', () => {
            sidebar.classList.toggle('sidebar-collapsed');
            sidebar.classList.toggle('sidebar-expanded');
            mainContent.classList.toggle('content-collapsed');
            mainContent.classList.toggle('content-expanded');
            
            // Change icon based on state
            const icon = toggleSidebar.querySelector('i');
            if (sidebar.classList.contains('sidebar-collapsed')) {
                feather.replace();
                icon.setAttribute('data-feather', 'chevron-right');
            } else {
                feather.replace();
                icon.setAttribute('data-feather', 'chevron-left');
            }
            feather.replace();
        });
        
        // Mobile menu toggle
        mobileMenuButton.addEventListener('click', () => {
            sidebar.classList.toggle('hidden');
        });
    </script>
</body>
</html><!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion - StockMaster</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <script src="https://unpkg.com/feather-icons"></script>
    <style>
        .auth-bg {
            background-image: linear-gradient(rgba(79, 70, 229, 0.8), rgba(79, 70, 229, 0.8)), url('http://static.photos/office/1200x630/42');
            background-size: cover;
            background-position: center;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div class="min-h-screen flex flex-col md:flex-row">
        <!-- Left Side - Background Image -->
        <div class="md:w-1/2 auth-bg text-white p-12 hidden md:flex flex-col justify-between">
            <div>
                <div class="flex items-center space-x-2">
                    <i data-feather="box" class="w-8 h-8"></i>
                    <span class="text-2xl font-bold">StockMaster</span>
                </div>
            </div>
            <div class="max-w-md">
                <h2 class="text-3xl font-bold mb-4">Gérez votre stock efficacement</h2>
                <p class="text-blue-100">Une solution complète pour suivre, gérer et optimiser votre inventaire en temps réel.</p>
            </div>
            <div class="flex space-x-4">
                <a href="#" class="text-blue-200 hover:text-white">
                    <i data-feather="info"></i>
                </a>
                <a href="#" class="text-blue-200 hover:text-white">
                    <i data-feather="help-circle"></i>
                </a>
                <a href="#" class="text-blue-200 hover:text-white">
                    <i data-feather="mail"></i>
                </a>
            </div>
        </div>

        <!-- Right Side - Login Form -->
        <div class="md:w-1/2 flex items-center justify-center p-8">
            <div class="w-full max-w-md">
                <div class="md:hidden mb-8 text-center">
                    <div class="flex items-center justify-center space-x-2 mb-4">
                        <i data-feather="box" class="w-8 h-8 text-indigo-600"></i>
                        <span class="text-2xl font-bold text-gray-800">StockMaster</span>
                    </div>
                    <h2 class="text-xl font-semibold text-gray-700">Connectez-vous à votre compte</h2>
                </div>

                <div class="bg-white rounded-lg shadow-md p-8">
                    <h1 class="text-2xl font-bold text-gray-800 mb-6">Connexion</h1>
                    
                    <form>
                        <div class="mb-4">
                            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                            <div class="relative">
                                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <i data-feather="mail" class="h-5 w-5 text-gray-400"></i>
                                </div>
                                <input type="email" id="email" class="pl-10 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="votre@email.com">
                            </div>
                        </div>
                        
                        <div class="mb-6">
                            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
                            <div class="relative">
                                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <i data-feather="lock" class="h-5 w-5 text-gray-400"></i>
                                </div>
                                <input type="password" id="password" class="pl-10 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" placeholder="••••••••">
                            </div>
                        </div>
                        
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center">
                                <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                                <label for="remember-me" class="ml-2 block text-sm text-gray-700">Se souvenir de moi</label>
                            </div>
                            
                            <div class="text-sm">
                                <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">Mot de passe oublié?</a>
                            </div>
                        </div>
                        
                        <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Se connecter
                        </button>
                    </form>
                    
                    <div class="mt-6">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center text-sm">
                                <span class="px-2 bg-white text-gray-500">Ou continuez avec</span>
                            </div>
                        </div>
                        
                        <div class="mt-6 grid grid-cols-2 gap-3">
                            <div>
                                <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                                    <i data-feather="github" class="h-5 w-5"></i>
                                </a>
                            </div>
                            
                            <div>
                                <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                                    <i data-feather="google" class="h-5 w-5"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8 text-center">
                    <p class="text-sm text-gray-600">
                        Pas encore de compte? 
                        <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">Créer un compte</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        feather.replace();
    </script>
</body>
</html>
