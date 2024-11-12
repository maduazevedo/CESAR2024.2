const colaboradorCheck = document.getElementById("colaborador");
const estudanteCheck = document.getElementById("discente");
const professorCheck = document.getElementById("docente");

const colaboradorArea = document.querySelector(".colaborator-area");
const estudanteArea = document.querySelector(".student-area");
const professorArea = document.querySelector(".teacher-area");

// Função para exibir ou esconder a área com base no checkbox
function toggleArea(area, checkbox) {
    if (checkbox.checked) {
        area.classList.remove("hide");
    } else {
        area.classList.add("hide");
    }
}

// Adiciona eventos para mostrar ou esconder as áreas conforme selecionado
colaboradorCheck.addEventListener("change", () => toggleArea(colaboradorArea, colaboradorCheck));
estudanteCheck.addEventListener("change", () => toggleArea(estudanteArea, estudanteCheck));
professorCheck.addEventListener("change", () => toggleArea(professorArea, professorCheck));
