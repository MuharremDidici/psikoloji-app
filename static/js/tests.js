// Test verileri
const testData = {
    // Beck Depresyon Envanteri (BDI)
    'beck_depression': {
        title: 'Beck Depresyon Envanteri',
        description: 'Bu test, depresyon belirtilerinin şiddetini ölçmek için kullanılan, dünya çapında kabul görmüş bir değerlendirme aracıdır.',
        questions: [
            {
                text: 'Kendinizi nasıl hissediyorsunuz?',
                options: [
                    'Kendimi üzgün hissetmiyorum',
                    'Kendimi üzgün hissediyorum',
                    'Her zaman üzgünüm ve bundan kurtulamıyorum',
                    'O kadar üzgün ve mutsuzum ki dayanamıyorum'
                ]
            },
            {
                text: 'Gelecek hakkında ne düşünüyorsunuz?',
                options: [
                    'Gelecek hakkında umutsuz değilim',
                    'Gelecek hakkında umutsuzum',
                    'Gelecekten beklediğim hiçbir şey yok',
                    'Geleceğim hakkında umutsuzum ve sanki hiçbir şey düzelmeyecekmiş gibi geliyor'
                ]
            },
            {
                text: 'Geçmiş başarılarınızı nasıl değerlendiriyorsunuz?',
                options: [
                    'Kendimi başarısız görmüyorum',
                    'Çoğu kişiden daha fazla başarısızlıklarım oldu',
                    'Geriye dönüp baktığımda, çok fazla başarısızlık görüyorum',
                    'Kendimi tümüyle başarısız bir insan olarak görüyorum'
                ]
            },
            {
                text: 'Günlük aktivitelerden ne kadar zevk alıyorsunuz?',
                options: [
                    'Her zamankinden farklı değil',
                    'Eskisi kadar zevk alamıyorum',
                    'Artık hiçbir şeyden gerçek bir zevk alamıyorum',
                    'Her şey beni sıkıyor'
                ]
            },
            {
                text: 'Kendinizi suçlu hissediyor musunuz?',
                options: [
                    'Kendimi suçlu hissetmiyorum',
                    'Bazı şeyler için suçlu hissediyorum',
                    'Çoğu zaman kendimi suçlu hissediyorum',
                    'Her zaman kendimi suçlu hissediyorum'
                ]
            }
        ]
    },

    // Hamilton Anksiyete Değerlendirme Ölçeği (HAM-A)
    'hamilton_anxiety': {
        title: 'Hamilton Anksiyete Değerlendirme Ölçeği',
        description: 'Bu test, anksiyete belirtilerinin şiddetini ölçmek için kullanılan standart bir değerlendirme aracıdır.',
        questions: [
            {
                text: 'Son bir haftada endişeli bir ruh hali, kötü bir şey olacakmış hissi yaşadınız mı?',
                options: [
                    'Hiç yaşamadım',
                    'Hafif düzeyde yaşadım',
                    'Orta düzeyde yaşadım',
                    'Şiddetli düzeyde yaşadım'
                ]
            },
            {
                text: 'Gerginlik belirtileri (irkilme, ağlama eğilimi, titreme, huzursuzluk, gevşeyememe) yaşıyor musunuz?',
                options: [
                    'Hiç yaşamıyorum',
                    'Hafif düzeyde yaşıyorum',
                    'Orta düzeyde yaşıyorum',
                    'Şiddetli düzeyde yaşıyorum'
                ]
            },
            {
                text: 'Korkular (karanlıktan, yabancılardan, yalnız kalmaktan, hayvanlardan) yaşıyor musunuz?',
                options: [
                    'Hiç yaşamıyorum',
                    'Hafif düzeyde yaşıyorum',
                    'Orta düzeyde yaşıyorum',
                    'Şiddetli düzeyde yaşıyorum'
                ]
            },
            {
                text: 'Uyku sorunları (uykuya dalmada güçlük, bölünmüş uyku, doyumsuz uyku, uyanınca yorgunluk) yaşıyor musunuz?',
                options: [
                    'Hiç yaşamıyorum',
                    'Hafif düzeyde yaşıyorum',
                    'Orta düzeyde yaşıyorum',
                    'Şiddetli düzeyde yaşıyorum'
                ]
            },
            {
                text: 'Bedensel belirtiler (kas ağrıları, sertlik, diş gıcırdatma, titrek konuşma) yaşıyor musunuz?',
                options: [
                    'Hiç yaşamıyorum',
                    'Hafif düzeyde yaşıyorum',
                    'Orta düzeyde yaşıyorum',
                    'Şiddetli düzeyde yaşıyorum'
                ]
            }
        ]
    },

    // Sosyal Anksiyete Ölçeği (LSAS)
    'social_anxiety': {
        title: 'Liebowitz Sosyal Anksiyete Ölçeği',
        description: 'Bu test, sosyal durumlarda yaşanan kaygı ve kaçınma davranışlarını değerlendiren standart bir ölçektir.',
        questions: [
            {
                text: 'Topluluk önünde konuşma yaparken ne kadar kaygı hissediyorsunuz?',
                options: [
                    'Hiç kaygı hissetmiyorum',
                    'Hafif düzeyde kaygı hissediyorum',
                    'Orta düzeyde kaygı hissediyorum',
                    'Şiddetli düzeyde kaygı hissediyorum'
                ]
            },
            {
                text: 'Yabancılarla tanışırken ne kadar rahatsızlık hissediyorsunuz?',
                options: [
                    'Hiç rahatsızlık hissetmiyorum',
                    'Hafif düzeyde rahatsızlık hissediyorum',
                    'Orta düzeyde rahatsızlık hissediyorum',
                    'Şiddetli düzeyde rahatsızlık hissediyorum'
                ]
            },
            {
                text: 'Başkaları sizi izlerken bir işi yapmakta ne kadar zorlanıyorsunuz?',
                options: [
                    'Hiç zorlanmıyorum',
                    'Hafif düzeyde zorlanıyorum',
                    'Orta düzeyde zorlanıyorum',
                    'Şiddetli düzeyde zorlanıyorum'
                ]
            },
            {
                text: 'Sosyal ortamlarda ne sıklıkla kaçınma davranışı gösteriyorsunuz?',
                options: [
                    'Hiç göstermiyorum',
                    'Nadiren gösteriyorum',
                    'Sıklıkla gösteriyorum',
                    'Her zaman gösteriyorum'
                ]
            },
            {
                text: 'Otorite figürleriyle (örn. yöneticiler) konuşurken ne kadar kaygı yaşıyorsunuz?',
                options: [
                    'Hiç kaygı yaşamıyorum',
                    'Hafif düzeyde kaygı yaşıyorum',
                    'Orta düzeyde kaygı yaşıyorum',
                    'Şiddetli düzeyde kaygı yaşıyorum'
                ]
            }
        ]
    },

    // Stres Değerlendirme Ölçeği (PSS)
    'perceived_stress': {
        title: 'Algılanan Stres Ölçeği',
        description: 'Bu test, son bir ay içinde yaşadığınız stres düzeyini değerlendiren, yaygın kullanılan bir ölçektir.',
        questions: [
            {
                text: 'Son bir ay içinde, beklenmedik bir şeyin gerçekleşmesi nedeniyle ne sıklıkla üzüldünüz?',
                options: [
                    'Hiçbir zaman',
                    'Nadiren',
                    'Bazen',
                    'Çok sık'
                ]
            },
            {
                text: 'Son bir ay içinde, hayatınızdaki önemli şeyleri kontrol edemediğinizi ne sıklıkla hissettiniz?',
                options: [
                    'Hiçbir zaman',
                    'Nadiren',
                    'Bazen',
                    'Çok sık'
                ]
            },
            {
                text: 'Son bir ay içinde, kendinizi ne sıklıkla sinirli ve stresli hissettiniz?',
                options: [
                    'Hiçbir zaman',
                    'Nadiren',
                    'Bazen',
                    'Çok sık'
                ]
            },
            {
                text: 'Son bir ay içinde, kişisel sorunlarınızı ele alma yeteneğinize ne sıklıkla güvendiniz?',
                options: [
                    'Her zaman',
                    'Sıklıkla',
                    'Bazen',
                    'Hiçbir zaman'
                ]
            },
            {
                text: 'Son bir ay içinde, işlerin istediğiniz gibi gittiğini ne sıklıkla hissettiniz?',
                options: [
                    'Her zaman',
                    'Sıklıkla',
                    'Bazen',
                    'Hiçbir zaman'
                ]
            }
        ]
    },

    // Uyku Kalitesi İndeksi (PSQI)
    'sleep_quality': {
        title: 'Pittsburgh Uyku Kalitesi İndeksi',
        description: 'Bu test, son bir ay içindeki uyku kalitesi ve uyku bozukluklarını değerlendiren standart bir ölçektir.',
        questions: [
            {
                text: 'Son bir ay içinde, uykuya dalma süreniz genellikle ne kadardı?',
                options: [
                    '15 dakika veya daha az',
                    '16-30 dakika',
                    '31-60 dakika',
                    '60 dakikadan fazla'
                ]
            },
            {
                text: 'Son bir ay içinde, gece boyunca uykunuz ne sıklıkla bölündü?',
                options: [
                    'Hiç bölünmedi',
                    'Haftada birden az',
                    'Haftada 1-2 kez',
                    'Haftada 3 veya daha fazla'
                ]
            },
            {
                text: 'Son bir ay içinde, uyku kalitenizi genel olarak nasıl değerlendirirsiniz?',
                options: [
                    'Çok iyi',
                    'Oldukça iyi',
                    'Oldukça kötü',
                    'Çok kötü'
                ]
            },
            {
                text: 'Son bir ay içinde, gündüz işlevselliğinizi sürdürmekte ne kadar zorluk yaşadınız?',
                options: [
                    'Hiç zorluk yaşamadım',
                    'Çok az zorluk yaşadım',
                    'Biraz zorluk yaşadım',
                    'Çok zorluk yaşadım'
                ]
            },
            {
                text: 'Son bir ay içinde, uyku ilacı kullanma ihtiyacınız ne sıklıkta oldu?',
                options: [
                    'Hiç olmadı',
                    'Haftada birden az',
                    'Haftada 1-2 kez',
                    'Haftada 3 veya daha fazla'
                ]
            }
        ]
    }
};

// Global değişkenler
let currentTest = null;
let currentQuestionIndex = 0;
let userAnswers = {};

// Test başlatma fonksiyonu
function startTest(testType) {
    try {
        console.log('Starting test:', testType);
        
        currentTest = testData[testType];
        if (!currentTest) {
            throw new Error('Geçersiz test türü');
        }
        
        currentQuestionIndex = 0;
        userAnswers = {};
        
        // Test başlığını güncelle
        const titleElement = document.getElementById('testTitle');
        if (!titleElement) {
            throw new Error('testTitle elementi bulunamadı');
        }
        titleElement.textContent = currentTest.title;
        
        // Test başlangıç ekranını gizle
        const startScreen = document.getElementById('testStart');
        if (!startScreen) {
            throw new Error('testStart elementi bulunamadı');
        }
        startScreen.classList.add('d-none');
        
        // Soru ekranını göster
        const questionsScreen = document.getElementById('testQuestions');
        if (!questionsScreen) {
            throw new Error('testQuestions elementi bulunamadı');
        }
        questionsScreen.classList.remove('d-none');
        
        // Sonuç ekranını gizle
        const resultScreen = document.getElementById('testResult');
        if (!resultScreen) {
            throw new Error('testResult elementi bulunamadı');
        }
        resultScreen.classList.add('d-none');
        
        // İlk soruyu göster
        showCurrentQuestion();
        
        console.log('Test started successfully');
    } catch (error) {
        console.error('Error starting test:', error);
        Swal.fire({
            icon: 'error',
            title: 'Hata!',
            text: 'Test başlatılırken bir hata oluştu: ' + error.message
        });
    }
}

// Soruları gösterme fonksiyonu
function showQuestions() {
    document.getElementById('testIntro').classList.add('d-none');
    document.getElementById('testQuestions').classList.remove('d-none');
    showCurrentQuestion();
}

// Mevcut soruyu gösterme fonksiyonu
function showCurrentQuestion() {
    if (!currentTest || !currentTest.questions) {
        console.error('Test data not loaded');
        return;
    }

    const currentQuestion = currentTest.questions[currentQuestionIndex];
    if (!currentQuestion) {
        console.error('Invalid question index:', currentQuestionIndex);
        return;
    }

    console.log('Showing question:', {
        index: currentQuestionIndex,
        question: currentQuestion,
        totalQuestions: currentTest.questions.length
    });

    const questionsDiv = document.getElementById('testQuestions');
    questionsDiv.innerHTML = `
        <div class="question-container">
            <div class="progress mb-4">
                <div class="progress-bar" role="progressbar" 
                    style="width: ${((currentQuestionIndex + 1) / currentTest.questions.length) * 100}%" 
                    aria-valuenow="${currentQuestionIndex + 1}" 
                    aria-valuemin="0" 
                    aria-valuemax="${currentTest.questions.length}">
                    Soru ${currentQuestionIndex + 1}/${currentTest.questions.length}
                </div>
            </div>
            <h4 class="question mb-4">${currentQuestion.text}</h4>
            <div class="options">
                ${currentQuestion.options.map((option, index) => `
                    <div class="answer-option ${userAnswers[currentQuestionIndex] === index ? 'selected' : ''}"
                        onclick="selectAnswer(${index})" data-answer="${index}">
                        ${option}
                    </div>
                `).join('')}
            </div>
            <div class="navigation-buttons mt-4">
                ${currentQuestionIndex > 0 ? 
                    `<button class="btn btn-secondary" onclick="previousQuestion()">
                        <i class="fas fa-arrow-left me-2"></i>Önceki
                    </button>` : 
                    '<div></div>'
                }
                ${currentQuestionIndex < currentTest.questions.length - 1 ? 
                    `<button id="nextButton" class="btn btn-primary" onclick="nextQuestion()">
                        Sonraki<i class="fas fa-arrow-right ms-2"></i>
                    </button>` :
                    `<button id="finishButton" class="btn btn-success" onclick="showResults()">
                        <i class="fas fa-check me-2"></i>Testi Bitir
                    </button>`
                }
            </div>
        </div>
    `;
}

// Cevap seçme fonksiyonu
function selectAnswer(answerIndex) {
    console.log('Selecting answer:', {
        questionIndex: currentQuestionIndex,
        answerIndex: answerIndex
    });
    
    // Önceki seçili cevabı kaldır
    const options = document.querySelectorAll('.answer-option');
    options.forEach(option => option.classList.remove('selected'));
    
    // Yeni cevabı seç
    const selectedOption = document.querySelector(`[data-answer="${answerIndex}"]`);
    if (selectedOption) {
        selectedOption.classList.add('selected');
    }
    
    // Cevabı kaydet (0-3 arası puan)
    userAnswers[currentQuestionIndex] = answerIndex;
    
    console.log('Current answers:', userAnswers);
    
    // Tüm sorular cevaplandı mı kontrol et
    const answeredQuestions = Object.keys(userAnswers).length;
    const totalQuestions = currentTest.questions.length;
    
    console.log('Progress:', {
        answered: answeredQuestions,
        total: totalQuestions,
        complete: answeredQuestions === totalQuestions
    });
    
    // Eğer son soruysa ve tüm sorular cevaplandıysa sonuçları göster
    if (currentQuestionIndex === currentTest.questions.length - 1 && answeredQuestions === totalQuestions) {
        const nextButton = document.querySelector('button[onclick="nextQuestion()"]');
        if (nextButton) {
            nextButton.textContent = 'Testi Bitir';
            nextButton.onclick = showResults;
        }
    }
}

// Sonraki soru fonksiyonu
function nextQuestion() {
    // Mevcut soru cevaplanmadıysa uyarı göster
    if (!(currentQuestionIndex in userAnswers)) {
        Swal.fire({
            title: 'Uyarı',
            text: 'Lütfen devam etmeden önce bir cevap seçin.',
            icon: 'warning',
            confirmButtonText: 'Tamam'
        });
        return;
    }

    // Sonraki soruya geç
    currentQuestionIndex++;
    
    console.log('Navigation:', {
        previousIndex: currentQuestionIndex - 1,
        currentIndex: currentQuestionIndex,
        totalQuestions: currentTest.questions.length
    });

    // Son soruya gelindiyse butonu güncelle
    const nextButton = document.querySelector('#nextButton');
    if (currentQuestionIndex === currentTest.questions.length - 1) {
        nextButton.textContent = 'Testi Bitir';
        nextButton.onclick = function() {
            if (currentQuestionIndex in userAnswers) {
                showResults();
            } else {
                Swal.fire({
                    title: 'Uyarı',
                    text: 'Lütfen son soruyu da cevaplayın.',
                    icon: 'warning',
                    confirmButtonText: 'Tamam'
                });
            }
        };
    }

    // Yeni soruyu göster
    showCurrentQuestion();
}

// Önceki soru fonksiyonu
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showCurrentQuestion();
    }
}

// Test sonuçlarını kaydetme fonksiyonu
async function saveTestResults(testType, answers, score) {
    try {
        console.log('Saving test results:', { testType, answers, score });

        const response = await fetch('/submit_test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                test_type: testType,
                answers: answers,
                score: score
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Test results saved successfully:', result);
        return result;

    } catch (error) {
        console.error('Test sonuçları gönderilirken hata:', error);
        console.error('Error details:', error);
        
        Swal.fire({
            title: 'Hata!',
            text: 'Test sonuçları kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.',
            icon: 'error',
            confirmButtonText: 'Tamam'
        });
        
        throw error;
    }
}

// Sonuçları gösterme fonksiyonu
async function showResults() {
    try {
        // Son soru cevaplanmadıysa uyarı göster
        if (!(currentQuestionIndex in userAnswers)) {
            Swal.fire({
                title: 'Uyarı',
                text: 'Lütfen son soruyu da cevaplayın.',
                icon: 'warning',
                confirmButtonText: 'Tamam'
            });
            return;
        }

        // Tüm soruların cevaplanıp cevaplanmadığını kontrol et
        const answeredQuestions = Object.keys(userAnswers).length;
        if (answeredQuestions !== currentTest.questions.length) {
            Swal.fire({
                title: 'Uyarı',
                text: 'Lütfen tüm soruları cevaplayın.',
                icon: 'warning',
                confirmButtonText: 'Tamam'
            });
            return;
        }

        // Loading göster
        Swal.fire({
            title: 'Lütfen bekleyin...',
            text: 'Sonuçlarınız hesaplanıyor',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Sonuç hesaplama
        const rawScore = calculateScore();
        const maxPossibleScore = currentTest.questions.length * 3; // Her soru için maksimum 3 puan
        const percentage = Math.round((rawScore / maxPossibleScore) * 100);

        console.log('Final score calculation:', {
            rawScore,
            maxPossibleScore,
            percentage
        });

        // Sonuçları kaydet
        const testType = Object.keys(testData).find(key => testData[key] === currentTest);
        await saveTestResults(testType, userAnswers, percentage);

        // Loading'i kapat
        await Swal.close();

        const resultDiv = document.getElementById('testResult');
        document.getElementById('testQuestions').classList.add('d-none');
        resultDiv.classList.remove('d-none');

        // Sonuç mesajı ve öneriler
        let resultMessage, recommendations;
        if (percentage >= 75) {
            resultMessage = 'Yüksek Risk';
            recommendations = 'Profesyonel yardım almanızı öneririz. Uzman bir psikolog ile görüşmek size yardımcı olabilir.';
        } else if (percentage >= 50) {
            resultMessage = 'Orta Risk';
            recommendations = 'Bazı belirtiler gösteriyorsunuz. Bir uzmana danışmayı değerlendirebilirsiniz.';
        } else {
            resultMessage = 'Düşük Risk';
            recommendations = 'Şu an için belirgin bir risk görünmüyor. Ancak belirtileriniz artarsa bir uzmana danışabilirsiniz.';
        }

        // Sonuç grafiğini oluştur
        resultDiv.innerHTML = `
            <h4 class="mb-4">Test Sonucunuz</h4>
            <div class="result-chart">
                <canvas id="resultChart"></canvas>
            </div>
            <div class="alert ${percentage >= 75 ? 'alert-danger' : percentage >= 50 ? 'alert-warning' : 'alert-success'} mt-4">
                <h5 class="alert-heading">${resultMessage}</h5>
                <p class="mb-0">${recommendations}</p>
            </div>
            <div class="d-flex justify-content-center gap-3 mt-4">
                <a href="/tests" class="btn btn-primary">
                    <i class="fas fa-redo me-2"></i>Yeni Test
                </a>
                <a href="/test_results" class="btn btn-secondary">
                    <i class="fas fa-history me-2"></i>Tüm Sonuçlarım
                </a>
            </div>
        `;

        // Sonuç grafiğini oluştur
        const ctx = document.getElementById('resultChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Risk Seviyesi', 'Normal'],
                datasets: [{
                    data: [percentage, 100 - percentage],
                    backgroundColor: [
                        percentage >= 75 ? '#dc3545' : percentage >= 50 ? '#ffc107' : '#28a745',
                        '#e9ecef'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        // Başarılı mesajı göster
        Swal.fire({
            title: 'Test Tamamlandı!',
            text: 'Sonuçlarınız başarıyla kaydedildi.',
            icon: 'success',
            confirmButtonText: 'Tamam'
        });

    } catch (error) {
        console.error('Error showing results:', error);
        Swal.fire({
            title: 'Hata!',
            text: 'Sonuçlar gösterilirken bir hata oluştu. Lütfen tekrar deneyin.',
            icon: 'error',
            confirmButtonText: 'Tamam'
        });
    }
}

// Skor hesaplama fonksiyonu
function calculateScore() {
    let totalScore = 0;
    const answers = Object.values(userAnswers);
    
    if (answers.length === 0) {
        console.warn('No answers found');
        return 0;
    }
    
    // Her cevap için puanı topla
    for (const answer of answers) {
        if (typeof answer === 'number' && answer >= 0 && answer <= 3) {
            totalScore += answer;
        } else {
            console.warn('Invalid answer value:', answer);
        }
    }
    
    console.log('Score calculation:', {
        totalAnswers: answers.length,
        totalScore: totalScore
    });
    
    return totalScore;
}
