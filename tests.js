// Test verileri
const tests = {
    beck: {
        title: 'Beck Depresyon Envanteri',
        questions: [
            {
                question: '0 Kendimi üzgün hissetmiyorum\n1 Kendimi üzgün hissediyorum\n2 Her zaman üzgünüm ve bundan kurtulamıyorum\n3 O kadar üzgün ve mutsuzum ki dayanamıyorum',
                type: 'radio',
                options: [0, 1, 2, 3]
            },
            {
                question: '0 Gelecek hakkında umutsuz değilim\n1 Gelecek hakkında umutsuzum\n2 Gelecekten beklediğim hiçbir şey yok\n3 Geleceğim hakkında umutsuzum ve sanki hiçbir şey düzelmeyecekmiş gibi geliyor',
                type: 'radio',
                options: [0, 1, 2, 3]
            },
            // Daha fazla soru eklenebilir
        ]
    },
    stai: {
        title: 'Durumluk-Sürekli Kaygı Envanteri',
        questions: [
            {
                question: 'Şu anda sakinim',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla']
            },
            {
                question: 'Kendimi emniyette hissediyorum',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla']
            },
            // Daha fazla soru eklenebilir
        ]
    },
    scl90: {
        title: 'SCL-90 Belirti Tarama Listesi',
        questions: [
            {
                question: 'Baş ağrısı',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            {
                question: 'Sinirlilik ve içinin titremesi',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            // Daha fazla soru eklenebilir
        ]
    }
};

// Test modalını yönetmek için gerekli değişkenler
let currentTest = null;
let currentAnswers = [];
const modal = new bootstrap.Modal(document.getElementById('testModal'));

// Testi başlat
function startTest(testType) {
    currentTest = testType;
    currentAnswers = [];
    const test = tests[testType];
    
    document.getElementById('testTitle').textContent = test.title;
    const testContent = document.getElementById('testContent');
    testContent.innerHTML = '';
    document.getElementById('testResult').style.display = 'none';
    
    test.questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'mb-4';
        
        const questionText = document.createElement('p');
        questionText.className = 'mb-2';
        questionText.textContent = `Soru ${index + 1}: ${q.question}`;
        questionDiv.appendChild(questionText);
        
        if (q.type === 'radio') {
            q.options.forEach((option, optIndex) => {
                const wrapper = document.createElement('div');
                wrapper.className = 'form-check';
                
                const input = document.createElement('input');
                input.type = 'radio';
                input.className = 'form-check-input';
                input.name = `question${index}`;
                input.value = optIndex;
                input.id = `q${index}o${optIndex}`;
                
                const label = document.createElement('label');
                label.className = 'form-check-label';
                label.htmlFor = `q${index}o${optIndex}`;
                label.textContent = option;
                
                wrapper.appendChild(input);
                wrapper.appendChild(label);
                questionDiv.appendChild(wrapper);
            });
        }
        
        testContent.appendChild(questionDiv);
    });
    
    modal.show();
}

// Test sonuçlarını hesapla ve gönder
document.getElementById('submitTest').addEventListener('click', async () => {
    const resultDiv = document.getElementById('testResult');
    resultDiv.style.display = 'block';
    
    // Cevapları topla
    const answers = {};
    const test = tests[currentTest];
    let totalScore = 0;
    let answeredQuestions = 0;
    
    test.questions.forEach((_, index) => {
        const selected = document.querySelector(`input[name="question${index}"]:checked`);
        if (selected) {
            const value = parseInt(selected.value);
            answers[`question${index}`] = value;
            totalScore += value;
            answeredQuestions++;
        }
    });
    
    // Tüm soruların cevaplanıp cevaplanmadığını kontrol et
    if (answeredQuestions !== test.questions.length) {
        showMessage('error', 'Lütfen tüm soruları cevaplayınız.');
        return;
    }
    
    // Sonuç metnini oluştur
    let resultText = '';
    if (currentTest === 'beck') {
        if (totalScore <= 9) resultText = 'Minimal depresyon';
        else if (totalScore <= 18) resultText = 'Hafif depresyon';
        else if (totalScore <= 29) resultText = 'Orta düzeyde depresyon';
        else resultText = 'Şiddetli depresyon';
    } else if (currentTest === 'stai') {
        if (totalScore <= 36) resultText = 'Düşük kaygı düzeyi';
        else if (totalScore <= 72) resultText = 'Orta kaygı düzeyi';
        else resultText = 'Yüksek kaygı düzeyi';
    } else if (currentTest === 'scl90') {
        if (totalScore <= 90) resultText = 'Normal düzey';
        else if (totalScore <= 180) resultText = 'Orta düzey';
        else resultText = 'Yüksek düzey';
    }
    
    // Sonuçları göster
    resultDiv.innerHTML = `
        <div class="alert alert-info">
            <h4>Test Sonuçları</h4>
            <p>Toplam Puan: ${totalScore}</p>
            <p>Değerlendirme: ${resultText}</p>
            <p class="mb-0"><small>Not: Bu sonuçlar yalnızca bilgilendirme amaçlıdır. Kesin tanı için mutlaka bir uzmana başvurunuz.</small></p>
        </div>
    `;
    
    try {
        // CSRF token'ı al
        const csrfToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrf_token='))
            ?.split('=')[1];
            
        if (!csrfToken) {
            throw new Error('CSRF token bulunamadı');
        }
        
        // Sonuçları sunucuya gönder
        const response = await fetch('/api/submit_test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                test_type: currentTest,
                answers: answers,
                score: totalScore
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            showMessage('success', 'Test sonuçlarınız başarıyla kaydedildi.');
            // 2 saniye sonra test sonuçları sayfasına yönlendir
            setTimeout(() => {
                window.location.href = '/test_results';
            }, 2000);
        } else {
            showMessage('error', data.message || 'Test sonuçları kaydedilirken bir hata oluştu.');
            console.error('Server error:', data);
        }
    } catch (error) {
        console.error('Test gönderme hatası:', error);
        showMessage('error', 'Bir hata oluştu: ' + error.message);
    }
});

// Mesaj gösterme fonksiyonu
function showMessage(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} mt-3`;
    alertDiv.textContent = message;
    
    const resultDiv = document.getElementById('testResult');
    resultDiv.appendChild(alertDiv);
}
