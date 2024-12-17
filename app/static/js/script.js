document.addEventListener('DOMContentLoaded', () => {
    // Seleção dos elementos dos checkboxes
    const colaboradorCheck = document.getElementById("colaborador");
    const estudanteCheck = document.getElementById("discente");
    const professorCheck = document.getElementById("docente");

    // Seleção das áreas de entrada correspondentes
    const colaboradorArea = document.querySelector(".colaborator-area");
    const estudanteArea = document.querySelector(".student-area");
    const professorArea = document.querySelector(".teacher-area");

    // Função para exibir ou esconder a área com base no checkbox
    function toggleArea(area, checkbox) {
        if (checkbox.checked) {
            area.classList.remove("hide"); // Exibe a área
        } else {
            area.classList.add("hide"); // Oculta a área
        }
    }

    // Adiciona eventos para mostrar ou esconder as áreas conforme selecionado
    colaboradorCheck.addEventListener("change", () => toggleArea(colaboradorArea, colaboradorCheck));
    estudanteCheck.addEventListener("change", () => toggleArea(estudanteArea, estudanteCheck));
    professorCheck.addEventListener("change", () => toggleArea(professorArea, professorCheck));

    // Inicializa a visibilidade das áreas conforme o estado inicial dos checkboxes
    toggleArea(colaboradorArea, colaboradorCheck);
    toggleArea(estudanteArea, estudanteCheck);
    toggleArea(professorArea, professorCheck);
});

// Seleciona todos os elementos de etapa (presumindo que tenham a classe .etapa)
const etapas = document.querySelectorAll('.etapa'); 

// Seleciona os botões de avançar e voltar
const btnAvancar = document.getElementById('btnAvancar');
const btnVoltar = document.getElementById('btnVoltar');

let etapaAtual = 0; // Índice da etapa atual, começando na primeira etapa (0)

// Adiciona a classe 'active' na primeira etapa durante a inicialização
if (etapas.length > 0) {
    etapas[etapaAtual].classList.add('active');
}

// Função para avançar para a próxima etapa
btnAvancar.addEventListener('click', () => {
    // Verifica se a etapa atual não é a última
    if (etapaAtual < etapas.length - 1) {
        etapas[etapaAtual].classList.remove('active'); // Remove 'active' da etapa atual
        etapaAtual++; // Avança para a próxima etapa
        etapas[etapaAtual].classList.add('active'); // Adiciona 'active' na nova etapa
        console.log('Avançou para a etapa:', etapaAtual + 1); // Log para depuração
    } else {
        console.log('Você já está na última etapa.');
    }
});

// Função para voltar para a etapa anterior
btnVoltar.addEventListener('click', () => {
    // Verifica se a etapa atual não é a primeira
    if (etapaAtual > 0) {
        etapas[etapaAtual].classList.remove('active'); // Remove 'active' da etapa atual
        etapaAtual--; // Retorna para a etapa anterior
        etapas[etapaAtual].classList.add('active'); // Adiciona 'active' na etapa anterior
        console.log('Voltou para a etapa:', etapaAtual + 1); // Log para depuração
    } else {
        console.log('Você já está na primeira etapa.');
    }
});

