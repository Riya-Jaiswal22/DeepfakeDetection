document.getElementById('uploadForm').addEventListener('submit', handleSubmit);

function handleSubmit(event) {
    event.preventDefault(); 

    const fileInput = document.getElementById('fileInput');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const errorMessage = document.getElementById('errorMessage');


    resultContainer.innerHTML = '';
    errorMessage.textContent = '';

    loader.classList.remove('hidden');

    const formData = new FormData();
    formData.append('files[]', fileInput.files[0]); 

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        loader.classList.add('hidden'); 
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || 'An error occurred while uploading the file.');
            });
        }
        return response.json();
    })
    .then(data => {
        
        resultContainer.innerHTML = `
            <h2>Results:</h2>
            ${Object.entries(data.results).map(([filename, result]) => `
                <p>${filename}: ${result.isDeepfake ? 'Deepfake Detected' : 'No Deepfake Detected'}</p>
                <p>Confidence: ${result.confidence}%</p>
            `).join('')}
        `;
    })
    .catch(error => {
        loader.classList.add('hidden'); 
        errorMessage.textContent = error.message; 
    });
}

function previewImage(event) {
    const imagePreview = document.getElementById('imagePreview');
    const fileName = document.getElementById('fileName');
    const button = document.querySelector('button');

    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden'); 
            imagePreview.classList.add('visible'); 
            fileName.textContent = file.name; 
            button.disabled = false; 
        };

        reader.readAsDataURL(file);
    } else {
        imagePreview.classList.add('hidden'); 
        fileName.textContent = 'Choose an image'; 
        button.disabled = true; 
    }
}
