document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('queryForm');
    const originInput = document.getElementById('origin');
    const destinationInput = document.getElementById('destination');
    const detailsInput = document.getElementById('details');
    
    const resultsSection = document.getElementById('resultsSection');
    const resultContent = document.getElementById('resultContent');
    const generateTime = document.getElementById('generateTime');
    const resultTitle = document.getElementById('resultTitle');

    const loadingSection = document.getElementById('loadingSection');
    const loadingText = document.getElementById('loadingText');

    const historyList = document.getElementById('historyList');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    // Loading Text cycler
    const loadingMessages = [
        "Analyzing destinations...",
        "Finding the best spots...",
        "Checking routes and flights...",
        "Curating activities...",
        "Finalizing your perfect itinerary..."
    ];
    let loadingInterval;

    // Load History
    const loadHistory = () => {
        historyList.innerHTML = '';
        const history = JSON.parse(localStorage.getItem('tripHistory')) || [];
        
        if (history.length === 0) {
            historyList.innerHTML = '<p style="color:var(--text-secondary); font-size:0.9rem; text-align:center; padding:2rem 0;">No trips yet.<br>Plan your first adventure!</p>';
            clearHistoryBtn.classList.add('hidden');
            return;
        }

        clearHistoryBtn.classList.remove('hidden');
        
        history.forEach((trip) => {
            const item = document.createElement('div');
            item.className = 'history-item';
            item.innerHTML = `
                <div class="history-item-title">${trip.title}</div>
                <div class="history-item-date">${trip.date}</div>
            `;
            item.addEventListener('click', () => displayTrip(trip));
            historyList.appendChild(item);
        });
    };

    const saveTrip = (title, markdown) => {
        const history = JSON.parse(localStorage.getItem('tripHistory')) || [];
        const date = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        
        // Add to top
        history.unshift({ title, markdown, date });
        
        // Keep only last 10 trips
        if (history.length > 10) history.pop();
        
        localStorage.setItem('tripHistory', JSON.stringify(history));
        loadHistory();
    };

    const displayTrip = (trip) => {
        resultsSection.classList.add('hidden');
        loadingSection.classList.add('hidden');
        
        resultTitle.textContent = `✨ ${trip.title}`;
        generateTime.textContent = trip.date;
        resultContent.innerHTML = marked.parse(trip.markdown);
        
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    };

    clearHistoryBtn.addEventListener('click', () => {
        localStorage.removeItem('tripHistory');
        loadHistory();
        resultsSection.classList.add('hidden');
    });

    // Initial Load
    loadHistory();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const origin = originInput.value.trim();
        const destination = destinationInput.value.trim();
        const details = detailsInput.value.trim();
        
        if (!origin || !destination) return;

        let query = `Plan a trip from ${origin} to ${destination}.`;
        if (details) {
            query += ` Additional details: ${details}`;
        }
        
        const title = `${origin} ➔ ${destination}`;

        // UI Loading State
        form.style.opacity = '0.5';
        form.style.pointerEvents = 'none';
        resultsSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        loadingSection.scrollIntoView({ behavior: 'smooth' });

        // Cycle loading messages
        let msgIndex = 0;
        loadingText.textContent = loadingMessages[msgIndex];
        loadingInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % loadingMessages.length;
            loadingText.textContent = loadingMessages[msgIndex];
        }, 2000);

        try {
            // Fetch from backend
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: query })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const data = await response.json();
            const answer = data.answer || "No itinerary generated.";

            // Save to history
            saveTrip(title, answer);

            // Display
            const timestamp = new Date().toLocaleString('en-US', { 
                month: 'short', day: 'numeric', year: 'numeric', 
                hour: '2-digit', minute: '2-digit', hour12: false 
            });
            
            resultTitle.textContent = `✨ ${title} Itinerary`;
            generateTime.textContent = timestamp;
            resultContent.innerHTML = marked.parse(answer);

            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error("Error fetching itinerary:", error);
            alert(`Failed to fetch itinerary: ${error.message}`);
            loadingSection.classList.add('hidden');
        } finally {
            // Reset UI State
            form.style.opacity = '1';
            form.style.pointerEvents = 'auto';
            clearInterval(loadingInterval);
        }
    });
});
