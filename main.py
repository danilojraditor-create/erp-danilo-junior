<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERP Danilo & Junior Elétrica</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-900 text-slate-100 font-sans">

    <div class="flex h-screen overflow-hidden">
        <div class="w-64 bg-slate-950 p-5 flex flex-col justify-between hidden md:flex border-r border-slate-800">
            <div>
                <div class="flex items-center gap-3 mb-8">
                    <div class="bg-amber-500 text-slate-950 p-2 rounded-lg font-bold text-xl">D&J</div>
                    <div>
                        <h1 class="font-bold text-sm leading-tight text-white">Danilo & Junior</h1>
                        <p class="text-xs text-amber-500">Serviços Elétricos</p>
                    </div>
                </div>
                <nav class="space-y-1">
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg bg-amber-500 text-slate-950 font-medium"><i class="fa-solid fa-chart-pie w-5"></i> Dashboard</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-users w-5"></i> Clientes</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-file-invoice-dollar w-5"></i> Orçamentos</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-screwdriver-wrench w-5"></i> Ordens de Serviço</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-boxes-stacked w-5"></i> Estoque</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-toolbox w-5"></i> Ferramentas</a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-900 hover:text-white transition"><i class="fa-solid fa-dollar-sign w-5"></i> Financeiro</a>
                </nav>
            </div>
            <div class="border-t border-slate-800 pt-4 text-xs text-slate-500">
                <p>Usuário: <strong>Júnior</strong></p>
                <p>Status: <span class="text-emerald-500">Online</span></p>
            </div>
        </div>

        <div class="flex-1 flex flex-col overflow-y-auto">
            <header class="bg-slate-950 px-6 py-4 flex items-center justify-between border-b border-slate-800">
                <h2 class="text-xl font-bold text-white">Painel Geral</h2>
                <div class="flex items-center gap-4">
                    <button class="bg-slate-900 px-4 py-2 rounded-lg text-sm border border-slate-800 hover:border-slate-700"><i class="fa-solid fa-plus text-amber-500 mr-2"></i>Nova OS</button>
                    <div class="w-10 h-10 rounded-full bg-amber-500 text-slate-950 font-bold flex items-center justify-center">JR</div>
                </div>
            </header>

            <main class="p-6 space-y-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <p class="text-xs text-slate-400 uppercase font-semibold">Receita do Mês</p>
                        <p class="text-2xl font-bold text-white mt-1">R$ 48.500,00</p>
                        <span class="text-emerald-500 text-xs"><i class="fa-solid fa-arrow-trend-up"></i> +12% em relação a Junho</span>
                    </div>
                    <div class="bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <p class="text-xs text-slate-400 uppercase font-semibold">Despesas do Mês</p>
                        <p class="text-2xl font-bold text-white mt-1">R$ 18.200,00</p>
                        <span class="text-emerald-500 text-xs">Dentro do esperado</span>
                    </div>
                    <div class="bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <p class="text-xs text-slate-400 uppercase font-semibold">Lucro Real</p>
                        <p class="text-2xl font-bold text-amber-500 mt-1">R$ 30.300,00</p>
                        <span class="text-slate-400 text-xs">Margem de 62.4%</span>
                    </div>
                    <div class="bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <p class="text-xs text-slate-400 uppercase font-semibold">Serviços em Execução</p>
                        <p class="text-2xl font-bold text-white mt-1">7 Ativos</p>
                        <span class="text-amber-500 text-xs"><i class="fa-solid fa-clock"></i> 3 aguardando equipe</span>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <h3 class="text-lg font-bold text-white mb-4"><i class="fa-solid fa-calendar-day text-amber-500 mr-2"></i> Agenda de Serviços de Hoje</h3>
                        <div class="space-y-3">
                            <div class="p-4 bg-slate-900 rounded-lg border-l-4 border-amber-500 flex justify-between items-center">
                                <div>
                                    <h4 class="font-bold text-sm text-white">Instalação de Subestação e Quadros</h4>
                                    <p class="text-xs text-slate-400">Condomínio Solar das Palmeiras • 08:30</p>
                                </div>
                                <span class="bg-amber-500/10 text-amber-500 text-xs px-2.5 py-1 rounded-full font-medium">Em Andamento</span>
                            </div>
                            <div class="p-4 bg-slate-900 rounded-lg border-l-4 border-slate-600 flex justify-between items-center">
                                <div>
                                    <h4 class="font-bold text-sm text-white">Manutenção Preventiva de Disjuntores</h4>
                                    <p class="text-xs text-slate-400">Supermercado Líder Doca • 14:00</p>
                                </div>
                                <span class="bg-slate-800 text-slate-400 text-xs px-2.5 py-1 rounded-full font-medium">Agendado</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-slate-950 p-5 rounded-xl border border-slate-800">
                        <h3 class="text-lg font-bold text-white mb-4"><i class="fa-solid fa-circle-exclamation text-rose-500 mr-2"></i> Alertas do Estoque</h3>
                        <div class="space-y-3">
                            <div class="p-3 bg-rose-500/10 rounded-lg border border-rose-500/20 flex justify-between items-center">
                                <div>
                                    <h4 class="font-bold text-xs text-rose-400">Cabo Flexível 4mm²</h4>
                                    <p class="text-[10px] text-slate-400">Estoque: 15 metros (Min: 50m)</p>
                                </div>
                                <span class="bg-rose-500 text-slate-950 text-[10px] px-2 py-0.5 rounded font-bold">COMPRAR</span>
                            </div>
                            <div class="p-3 bg-rose-500/10 rounded-lg border border-rose-500/20 flex justify-between items-center">
                                <div>
                                    <h4 class="font-bold text-xs text-rose-400">Disjuntor NEMA 50A</h4>
                                    <p class="text-[10px] text-slate-400">Estoque: 2 unidades (Min: 5un)</p>
                                </div>
                                <span class="bg-rose-500 text-slate-950 text-[10px] px-2 py-0.5 rounded font-bold">COMPRAR</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>

</body>
</html>
