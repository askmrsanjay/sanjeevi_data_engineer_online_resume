document.addEventListener('DOMContentLoaded', () => {
    const downloadBtn = document.getElementById('download-pdf');
    const resumeContent = document.getElementById('resume-content');
    const toggleEditBtn = document.getElementById('toggle-edit');
    const logoutBtn = document.getElementById('logout-admin');
    const navLinks = document.querySelectorAll('.nav-links a');

    let isEditMode = false;

    // --- 1. Admin Security Check ---
    const checkAdmin = () => {
        const uploadPdfBtn = document.getElementById('upload-pdf-btn');
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');

        if (localStorage.getItem('admin_access') === 'true') {
            toggleEditBtn.style.display = 'inline-block';
            logoutBtn.style.display = 'inline-block';
            if (uploadPdfBtn) uploadPdfBtn.style.display = 'inline-block';
            if (undoBtn) undoBtn.style.display = 'inline-block';
            if (redoBtn) redoBtn.style.display = 'inline-block';
        } else {
            toggleEditBtn.style.display = 'none';
            logoutBtn.style.display = 'none';
            if (uploadPdfBtn) uploadPdfBtn.style.display = 'none';
            if (undoBtn) undoBtn.style.display = 'none';
            if (redoBtn) redoBtn.style.display = 'none';
        }
    };

    // --- Secure Admin Hashing ---
    async function sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    document.querySelector('.logo').addEventListener('dblclick', async () => {
        const pass = prompt('Enter Admin Password:');
        if (pass) {
            // "Salt" is a secret key known only to the code
            const salt = 'sanjeevi_secret_99_resume_2024';
            const hashedInput = await sha256(pass + salt);
            const adminHash = 'f98cd6d69ad6897932b36f1f08a11eeacd3c1977c34762364e8bea3231aa0263';

            if (hashedInput === adminHash) {
                localStorage.setItem('admin_access', 'true');
                checkAdmin();
                alert('Admin Mode Activated!');
            } else {
                alert('Incorrect Password.');
            }
        }
    });

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('admin_access');
            alert('Logged out.');
            location.reload();
        });
    }

    checkAdmin();

    // --- 2. Persistence Logic ---
    const savedContent = localStorage.getItem('sanjeevi_resume_content');
    if (savedContent) {
        resumeContent.innerHTML = savedContent;
        // Fix: Ensure cert-items have spans for editing if they are from old save
        resumeContent.querySelectorAll('.cert-item').forEach(item => {
            if (!item.querySelector('span')) {
                const icon = item.querySelector('i');
                const text = item.textContent.trim();
                item.innerHTML = '';
                if (icon) item.appendChild(icon);
                const span = document.createElement('span');
                span.innerText = text;
                item.appendChild(document.createTextNode(' '));
                item.appendChild(span);
            }
        });
    }

    function save() {
        localStorage.setItem('sanjeevi_resume_content', resumeContent.innerHTML);
    }

    // --- 3. Live Edit Mode Logic ---
    toggleEditBtn.addEventListener('click', () => {
        isEditMode = !isEditMode;
        document.body.classList.toggle('edit-mode-active', isEditMode);
        toggleEditBtn.classList.toggle('active', isEditMode);

        document.querySelectorAll('.admin-only').forEach(btn => {
            btn.style.display = isEditMode ? 'inline-block' : 'none';
        });

        makeEditable();

        if (isEditMode) {
            toggleEditBtn.innerHTML = '<i class="fas fa-check"></i> Done';
        } else {
            toggleEditBtn.innerHTML = '<i class="fas fa-edit"></i> Edit Mode';
            save();
        }
    });

    function makeEditable(root = resumeContent) {
        root.querySelectorAll('h1, h2, h3, p, span:not(.add-tag), li, a:not(.social-link), .cert-item').forEach(el => {
            el.contentEditable = isEditMode;
        });
    }

    // --- 4. Dynamic Content Logic (History System) ---
    const historyStack = [];
    let historyIndex = -1;
    let isHistoryAction = false;

    function pushState() {
        if (isHistoryAction) return;
        // Optimization: Don't push if content is same as current pointer
        const currentState = resumeContent.innerHTML;
        if (historyIndex >= 0 && historyStack[historyIndex] === currentState) return;

        // If we are in the middle of the stack and make a new change, clear the "redo" part
        if (historyIndex < historyStack.length - 1) {
            historyStack.splice(historyIndex + 1);
        }

        historyStack.push(currentState);
        historyIndex++;

        // Keep stack size reasonable (e.g., 50 steps)
        if (historyStack.length > 50) {
            historyStack.shift();
            historyIndex--;
        }

        updateHistoryButtons();
        save();
    }

    function undo() {
        if (historyIndex > 0) {
            isHistoryAction = true;
            historyIndex--;
            resumeContent.innerHTML = historyStack[historyIndex];
            bindAllActions();
            makeEditable();
            updateHistoryButtons();
            save();
            isHistoryAction = false;
        }
    }

    function redo() {
        if (historyIndex < historyStack.length - 1) {
            isHistoryAction = true;
            historyIndex++;
            resumeContent.innerHTML = historyStack[historyIndex];
            bindAllActions();
            makeEditable();
            updateHistoryButtons();
            save();
            isHistoryAction = false;
        }
    }

    function updateHistoryButtons() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');
        if (undoBtn) undoBtn.disabled = historyIndex <= 0;
        if (redoBtn) redoBtn.disabled = historyIndex >= historyStack.length - 1;

        // Visual cue for disabled state
        if (undoBtn) undoBtn.style.opacity = undoBtn.disabled ? '0.3' : '1';
        if (redoBtn) redoBtn.style.opacity = redoBtn.disabled ? '0.3' : '1';
    }

    // Initialize first state
    setTimeout(() => pushState(), 500);

    function bindAllActions() {
        // Clear all existing delete buttons before re-binding
        document.querySelectorAll('.delete-btn').forEach(btn => btn.remove());

        const addExpBtn = document.getElementById('add-experience');
        const addProjBtn = document.getElementById('add-project');
        const addSkillBtn = document.getElementById('add-skill-card');
        const addCertBtn = document.getElementById('add-cert');

        if (addExpBtn) addExpBtn.onclick = () => addRow('timeline-container', '.timeline-item');
        if (addProjBtn) addProjBtn.onclick = () => addRow('projects-container', '.project-card');
        if (addSkillBtn) addSkillBtn.onclick = () => addRow('skills-container', '.skill-card');
        if (addCertBtn) addCertBtn.onclick = () => addRow('certs-container', '.cert-item');

        // Add Delete Buttons to Cards
        document.querySelectorAll('.timeline-item, .project-card, .skill-card, .cert-item').forEach(el => {
            addDeleteButton(el);
        });

        // Helper to bind "Add Sub-item" logic
        function setupAddButton(containerSelector, btnClass, promptText, tagName) {
            document.querySelectorAll(containerSelector).forEach(container => {
                let btn = container.querySelector('.' + btnClass);

                if (!btn) {
                    btn = document.createElement(tagName === 'li' ? 'li' : 'span');
                    btn.className = btnClass + ' admin-only';
                    btn.innerHTML = '<i class="fas fa-plus"></i> ' + (tagName === 'li' ? 'Add ' + btnClass.split('-')[1] : '');
                    if (tagName === 'li') {
                        btn.style.cursor = 'pointer';
                        btn.style.color = 'var(--primary)';
                        btn.style.listStyle = 'none';
                        btn.style.marginTop = '10px';
                    } else {
                        btn.style.cursor = 'pointer';
                    }
                    container.appendChild(btn);
                }

                btn.onclick = (e) => {
                    e.stopPropagation();
                    const value = prompt('Enter ' + promptText + ':');
                    if (value) {
                        const newItem = document.createElement(tagName === 'li' ? 'li' : 'span');
                        newItem.innerText = value;
                        container.insertBefore(newItem, btn);
                        if (isEditMode) makeEditable(newItem);
                        addDeleteButton(newItem);
                        pushState();
                    }
                };
                btn.style.display = isEditMode ? (tagName === 'li' ? 'block' : 'inline-block') : 'none';
            });
        }

        setupAddButton('.skill-card ul', 'add-skill-item', 'skill', 'li');
        setupAddButton('.timeline-content ul', 'add-resp-item', 'responsibility', 'li');
        setupAddButton('.project-tags', 'add-tag', 'tag name (e.g., Python)', 'span');

        document.querySelectorAll('.skill-card li:not(.add-skill-item), .timeline-content li:not(.add-resp-item), .project-tags span:not(.add-tag)').forEach(item => {
            addDeleteButton(item);
        });
    }

    function addDeleteButton(el) {
        if (el.querySelector('.delete-btn')) return;
        const delBtn = document.createElement('div');
        delBtn.className = 'delete-btn admin-only';
        delBtn.innerHTML = '<i class="fas fa-times"></i>';
        delBtn.onclick = (e) => {
            e.stopPropagation();
            el.remove();
            pushState();
        };
        el.appendChild(delBtn);
    }

    function addRow(containerId, itemClass) {
        const container = document.getElementById(containerId);
        const template = container.querySelector(itemClass).cloneNode(true);
        template.querySelectorAll('.delete-btn').forEach(b => b.remove());
        template.querySelectorAll('h3, p, span:not(.add-tag), li:not(.add-skill-item):not(.add-resp-item)').forEach(el => {
            if (el.innerText !== '+' && !el.querySelector('i')) el.innerText = 'New text...';
        });
        container.appendChild(template);
        if (isEditMode) makeEditable(template);
        bindAllActions();
        pushState();
    }

    bindAllActions();

    // UI Connections for History
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');
    if (undoBtn) undoBtn.addEventListener('click', undo);
    if (redoBtn) redoBtn.addEventListener('click', redo);

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
        if (!isEditMode) return;
        if (e.ctrlKey && e.key.toLowerCase() === 'z') {
            e.preventDefault();
            undo();
        }
        if (e.ctrlKey && (e.key.toLowerCase() === 'y' || (e.shiftKey && e.key.toLowerCase() === 'z'))) {
            e.preventDefault();
            redo();
        }
    });

    let inputDebounce;
    resumeContent.addEventListener('input', (e) => {
        if (isEditMode) {
            if (e.target.classList.contains('delete-btn')) return;
            clearTimeout(inputDebounce);
            inputDebounce = setTimeout(() => pushState(), 500);
        }
    });

    resumeContent.addEventListener('blur', () => { if (isEditMode) pushState(); }, true);

    // --- 5. PDF Download ---
    const uploadBtn = document.getElementById('upload-pdf-btn');
    const pdfInput = document.getElementById('pdf-upload');

    if (uploadBtn) {
        uploadBtn.addEventListener('click', () => pdfInput.click());
        pdfInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file && file.type === 'application/pdf') {
                const reader = new FileReader();
                reader.onload = (event) => {
                    localStorage.setItem('sanjeevi_custom_pdf', event.target.result);
                    alert('Custom PDF Resume Uploaded Successfully!');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    downloadBtn.addEventListener('click', () => {
        const customPdf = localStorage.getItem('sanjeevi_custom_pdf');

        // Bypass to custom PDF if uploaded
        if (customPdf) {
            const link = document.createElement('a');
            link.href = customPdf;
            link.download = 'azure_databricks_data_engineer.pdf';
            link.click();
            return;
        }

        const type = confirm('Download ATS-Friendly (Clean) Resume? \n(Cancel for Standard Design)') ? 'ats' : 'standard';

        const options = {
            margin: [5, 10, 5, 10], /* Reduced top/bottom margins */
            filename: `azure_databricks_data_engineer_${type.toUpperCase()}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2, useCORS: true, letterRendering: true },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
            pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
        };

        const wasEditMode = isEditMode;
        if (wasEditMode) document.body.classList.remove('edit-mode-active');
        if (type === 'ats') document.body.classList.add('is-ats');
        document.body.classList.add('is-printing');

        html2pdf().set(options).from(resumeContent).save().then(() => {
            document.body.classList.remove('is-printing');
            document.body.classList.remove('is-ats');
            if (wasEditMode) document.body.classList.add('edit-mode-active');
        });
    });

    // Smooth scroll and Reveal animations
    navLinks.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) targetElement.scrollIntoView({ behavior: 'smooth' });
        });
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('revealed'); });
    }, { threshold: 0.1 });

    document.querySelectorAll('.section, .skill-card, .timeline-item, .project-card, .cert-item').forEach(el => {
        el.classList.add('reveal-init');
        observer.observe(el);
    });
});
