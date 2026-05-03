const API_URL = 'http://127.0.0.1:5000';

let scene, camera, renderer, room, accentWall, tv;
let is3DVisible = true;
let selectedFile = null;
let threeInitialized = false;

document.addEventListener('DOMContentLoaded', () => {
    initUpload();
    initPreferences();
    initGenerateButton();
    init3DPreview();
});

function initUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const roomImage = document.getElementById('roomImage');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImage = document.getElementById('removeImage');

    uploadArea.addEventListener('click', () => {
        roomImage.click();
    });

    roomImage.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelect(e.target.files[0]);
        }
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    removeImage.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        previewContainer.style.display = 'none';
        uploadArea.querySelector('.upload-placeholder').style.display = 'flex';
        roomImage.value = '';
        updateGenerateButton();
    });

    function handleFileSelect(file) {
        if (!file.type.match('image.*')) {
            showError('Please upload a valid image file');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            showError('File size must be less than 16MB');
            return;
        }

        selectedFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadArea.querySelector('.upload-placeholder').style.display = 'none';
            previewContainer.style.display = 'inline-block';
        };
        reader.readAsDataURL(file);

        updateGenerateButton();
    }
}

function initPreferences() {
    const colorTheme = document.getElementById('colorTheme');
    const style = document.getElementById('style');
    const budget = document.getElementById('budget');

    [colorTheme, style, budget].forEach(select => {
        select.addEventListener('change', updateGenerateButton);
    });
}

function updateGenerateButton() {
    const generateBtn = document.getElementById('generateBtn');
    const colorTheme = document.getElementById('colorTheme').value;
    const style = document.getElementById('style').value;
    const budget = document.getElementById('budget').value;

    generateBtn.disabled = !(selectedFile && colorTheme && style && budget);
}

function initGenerateButton() {
    const generateBtn = document.getElementById('generateBtn');

    generateBtn.addEventListener('click', generateDesign);
}

async function generateDesign() {
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const outputSection = document.getElementById('outputSection');
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.style.display = 'none';
    outputSection.style.display = 'none';

    generateBtn.disabled = true;
    loading.style.display = 'block';

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('color', document.getElementById('colorTheme').value);
    formData.append('style', document.getElementById('style').value);
    formData.append('budget', document.getElementById('budget').value);

    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to generate design');
        }

        displayOutput(data);
    } catch (error) {
        showError(error.message);
        console.error('Generation error:', error);
    } finally {
        loading.style.display = 'none';
        generateBtn.disabled = false;
    }
}

function displayOutput(data) {
    const outputSection = document.getElementById('outputSection');
    const generatedImage = document.getElementById('generatedImage');
    const suggestionsList = document.getElementById('suggestionsList');
    const threeContainer = document.getElementById('threeJsContainer');

    generatedImage.src = `${API_URL}${data.image_url}`;

    suggestionsList.innerHTML = '';
    data.suggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = `suggestion-item ${suggestion.priority}`;
        item.innerHTML = `
            <div class="suggestion-category">${suggestion.category}</div>
            <div class="suggestion-text">${suggestion.text}</div>
            <div class="suggestion-priority">Priority: ${suggestion.priority}</div>
        `;
        suggestionsList.appendChild(item);
    });

    if (!threeInitialized && threeContainer && typeof THREE !== 'undefined') {
        init3DScene(threeContainer);
        animate3D();
    }

    update3DScene();
    outputSection.style.display = 'block';
    outputSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function init3DPreview() {
    const toggleBtn = document.getElementById('toggle3D');

    toggleBtn.addEventListener('click', () => {
        const container = document.getElementById('threeJsContainer');
        is3DVisible = !is3DVisible;
        container.style.display = is3DVisible ? 'block' : 'none';
        toggleBtn.textContent = is3DVisible ? 'Hide 3D' : 'Show 3D';
    });
}

function init3DScene(container) {
    if (!container || typeof THREE === 'undefined') {
        console.warn('Three.js not loaded or container missing');
        return false;
    }

    if (threeInitialized) {
        return true;
    }

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 400;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf1f5f9);

    camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.set(8, 6, 8);
    camera.lookAt(0, 2, 0);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.setClearColor(0xf1f5f9, 1);
    container.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    room = new THREE.Group();

    const floorGeometry = new THREE.PlaneGeometry(10, 8);
    const floorMaterial = new THREE.MeshStandardMaterial({
        color: 0x8B4513,
        roughness: 0.8
    });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = 0;
    floor.receiveShadow = true;
    room.add(floor);

    const wallMaterial = new THREE.MeshStandardMaterial({
        color: 0xf5f5f5,
        roughness: 0.9
    });

    const backWall = new THREE.Mesh(
        new THREE.PlaneGeometry(10, 5),
        wallMaterial
    );
    backWall.position.set(0, 2.5, -4);
    backWall.receiveShadow = true;
    room.add(backWall);

    const leftWall = new THREE.Mesh(
        new THREE.PlaneGeometry(8, 5),
        wallMaterial
    );
    leftWall.position.set(-5, 2.5, 0);
    leftWall.rotation.y = Math.PI / 2;
    leftWall.receiveShadow = true;
    room.add(leftWall);

    accentWall = new THREE.Mesh(
        new THREE.PlaneGeometry(10, 5),
        new THREE.MeshStandardMaterial({
            color: 0x6366f1,
            roughness: 0.7
        })
    );
    accentWall.position.set(0, 2.5, 4);
    accentWall.receiveShadow = true;
    room.add(accentWall);

    tv = new THREE.Mesh(
        new THREE.BoxGeometry(2, 1.2, 0.1),
        new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            roughness: 0.3,
            metalness: 0.5
        })
    );
    tv.position.set(0, 2, 3.5);
    tv.castShadow = true;
    room.add(tv);

    const tvStand = new THREE.Mesh(
        new THREE.BoxGeometry(2.5, 0.5, 0.4),
        new THREE.MeshStandardMaterial({
            color: 0x4a3728,
            roughness: 0.6
        })
    );
    tvStand.position.set(0, 0.25, 3.7);
    tvStand.castShadow = true;
    room.add(tvStand);

    scene.add(room);

    setupControls(renderer.domElement);

    threeInitialized = true;
    return true;
}

function setupControls(domElement) {
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let cameraAngle = { theta: Math.PI / 4, phi: Math.PI / 3 };
    let cameraDistance = 12;

    function updateCameraPosition() {
        camera.position.x = cameraDistance * Math.sin(cameraAngle.phi) * Math.cos(cameraAngle.theta);
        camera.position.y = cameraDistance * Math.cos(cameraAngle.phi);
        camera.position.z = cameraDistance * Math.sin(cameraAngle.phi) * Math.sin(cameraAngle.theta);
        camera.lookAt(0, 2, 0);
    }

    updateCameraPosition();

    domElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;

        cameraAngle.theta -= deltaX * 0.01;
        cameraAngle.phi = Math.max(0.1, Math.min(Math.PI - 0.1, cameraAngle.phi + deltaY * 0.01));

        updateCameraPosition();

        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    domElement.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomSpeed = 0.1;
        const newRadius = cameraDistance * (1 + (e.deltaY > 0 ? zoomSpeed : -zoomSpeed));
        if (newRadius > 5 && newRadius < 30) {
            cameraDistance = newRadius;
            updateCameraPosition();
        }
    }, { passive: false });
}

function update3DScene() {
    const colorSelect = document.getElementById('colorTheme').value.toLowerCase();

    if (!accentWall) return;

    const colorMap = {
        'purple luxury': 0x8B5CF6,
        'grey modern': 0x6B7280,
        'mint green': 0x6EE7B7,
        'navy blue': 0x1E3A5F,
        'terracotta': 0xE07A5F,
        'sage green': 0x9CAF88,
        'mustard yellow': 0xE4B44F,
        'blush pink': 0xF4ACB7,
        'teal': 0x2D8B8B,
        'charcoal': 0x374151
    };

    const newColor = colorMap[colorSelect] || 0x6366f1;
    accentWall.material.color.setHex(newColor);
}

function animate3D() {
    requestAnimationFrame(animate3D);

    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}