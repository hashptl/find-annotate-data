const uploadFile = document.getElementById('uploadFile');
const resultContainer = document.getElementById('resultContainer');
const loader = document.getElementById('loader');
const repeatedImagesContainer = document.getElementById('repeatedImagesContainer');
const repeatedImagesTable = document.getElementById('repeatedImagesTable');
const noRepeatedImagesMessage = document.getElementById('noRepeatedImagesMessage');

uploadFile.addEventListener('change', async () => {
    const file = uploadFile.files[0];
    if (file) {
        loader.classList.remove('hidden');
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://0.0.0.0:8000/process-annotations', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            loader.classList.add('hidden');
            resultContainer.classList.remove('hidden');

            document.getElementById('totalAnnotations').textContent = data.total_annotations;
            document.getElementById('totalAnnotatedImages').textContent = data.total_annotated_images;
            document.getElementById('totalRepeatedImages').textContent = data.total_repeated_images;

            // Handling repeated images table display
            if (data.total_repeated_images === 0) {
                repeatedImagesContainer.classList.add('hidden');
                noRepeatedImagesMessage.classList.remove('hidden');
            } else {
                repeatedImagesContainer.classList.remove('hidden');
                noRepeatedImagesMessage.classList.add('hidden');

                // Clear previous table content
                const tbody = repeatedImagesTable.querySelector('tbody');
                tbody.innerHTML = ''; 

                // Populate repeated images in table format
                for (const [imageId, count] of Object.entries(data.repeated_images)) {
                    const row = document.createElement('tr');
                    
                    const imgIdCell = document.createElement('td');
                    imgIdCell.textContent = imageId;  // Displaying the image ID instead of the image path
                    row.appendChild(imgIdCell);

                    const annotationCell = document.createElement('td');
                    annotationCell.textContent = `${count}`;  // Displaying the count of repeated images
                    row.appendChild(annotationCell);

                    tbody.appendChild(row);
                }
            }
        } catch (error) {
            loader.classList.add('hidden');
            alert('Error processing the file. Please try again.');
        }
    }
});
