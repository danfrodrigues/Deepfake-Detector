const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const resultDiv = document.getElementById("result");
const uploadForm = document.getElementById("uploadForm");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      previewImage.hidden = false;
    };
    reader.readAsDataURL(file);
  }
});

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!fileInput.files.length) {
    alert("Selecione uma imagem!");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://127.0.0.1:8000/predict/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Erro na resposta do servidor");
    }

    const data = await response.json();

    resultDiv.innerHTML = `
      <p><strong>Predição:</strong> ${data.prediction}</p>
      <p><strong>Explicação:</strong> ${data.explanation}</p>
    `;
  } catch (err) {
    console.error(err);
    alert("Erro ao enviar imagem!");
  }
});
