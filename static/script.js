const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const loadingState = document.getElementById('loading');
const resultSection = document.getElementById('result-section');
const previewImg = document.getElementById('preview-img');
const diagnosisBadge = document.getElementById('diagnosis-badge');
const confidenceText = document.getElementById('confidence-text');
const confidenceBar = document.getElementById('confidence-bar');
const resetBtn = document.getElementById('reset-btn');
const bboxOverlay = document.getElementById('bbox-overlay'); // YOLO Box layer

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) return alert('Please upload an image file.');

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
    };
    reader.readAsDataURL(file);

    dropZone.style.display = 'none';
    loadingState.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/predict', {
        method: 'POST',
        body: formData
    })
    .then(res => {
        if (!res.ok) throw new Error("API Error");
        return res.json();
    })
    .then(data => {
        showResults(data);
    })
    .catch(err => {
        alert("Error analyzing image.");
        resetUI();
    });
}

function showResults(data) {
    loadingState.style.display = 'none';
    resultSection.style.display = 'block';
    
    // Clear old YOLO boxes
    bboxOverlay.innerHTML = '';
    
    // Required to scale the coordinates from the physical image to the CSS display size
    const imgWidth = data.image_width;
    const imgHeight = data.image_height;

    setTimeout(() => {
        confidenceBar.style.width = data.parasite_probability;
        confidenceText.innerText = data.parasite_probability;
        
        if (data.parasite_detected) {
            diagnosisBadge.innerText = 'Parasite Detected';
            diagnosisBadge.className = 'badge danger';
            confidenceBar.style.background = 'var(--danger)';
            document.querySelector('.orb1').style.background = 'var(--danger)';
        } else {
            diagnosisBadge.innerText = 'Healthy Region';
            diagnosisBadge.className = 'badge success';
            confidenceBar.style.background = 'var(--success)';
            document.querySelector('.orb1').style.background = 'var(--success)';
        }
        
        // Calculate precisely where the image actually rendered inside the object-fit: contain CSS box
        const containerWidth = previewImg.clientWidth;
        const containerHeight = previewImg.clientHeight;
        const imgRatio = imgWidth / imgHeight;
        const containerRatio = containerWidth / containerHeight;
        
        let displayWidth, displayHeight, offsetX, offsetY;
        
        if (containerRatio > imgRatio) {
            displayHeight = containerHeight;
            displayWidth = displayHeight * imgRatio;
            offsetX = (containerWidth - displayWidth) / 2;
            offsetY = 0;
        } else {
            displayWidth = containerWidth;
            displayHeight = displayWidth / imgRatio;
            offsetX = 0;
            offsetY = (containerHeight - displayHeight) / 2;
        }

        const scaleX = displayWidth / imgWidth;
        const scaleY = displayHeight / imgHeight;
        
        if (data.detections && data.detections.length > 0) {
            data.detections.forEach(det => {
                const box = det.box;
                
                const boxEl = document.createElement('div');
                boxEl.className = 'bounding-box';
                boxEl.classList.add(det.label.toLowerCase().includes('parasite') ? 'box-danger' : 'box-safe');
                
                const left = (box.x1 * scaleX) + offsetX;
                const top = (box.y1 * scaleY) + offsetY;
                const width = (box.x2 - box.x1) * scaleX;
                const height = (box.y2 - box.y1) * scaleY;
                
                boxEl.style.left = `${left}px`;
                boxEl.style.top = `${top}px`;
                boxEl.style.width = `${width}px`;
                boxEl.style.height = `${height}px`;
                
                const labelEl = document.createElement('div');
                labelEl.className = 'box-label';
                labelEl.innerText = `${det.label} ${(det.confidence * 100).toFixed(0)}%`;
                
                boxEl.appendChild(labelEl);
                bboxOverlay.appendChild(boxEl);
            });
        }
        
    }, 100);
}

function resetUI() {
    resultSection.style.display = 'none';
    loadingState.style.display = 'none';
    dropZone.style.display = 'block';
    fileInput.value = '';
    confidenceBar.style.width = '0%';
    document.querySelector('.orb1').style.background = '#3b82f6';
    bboxOverlay.innerHTML = '';
}

resetBtn.addEventListener('click', resetUI);
