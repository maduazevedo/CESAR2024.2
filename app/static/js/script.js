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
