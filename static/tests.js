// Test verileri
const tests = {
    beck: {
        title: 'Beck Depresyon Envanteri',
        description: 'Bu envanter kendinizi bugün dahil son bir hafta içinde nasıl hissettiğinizi araştırmaya yönelik 21 sorudan oluşmaktadır.',
        questions: [
            {
                question: '1. Hüzün',
                options: [
                    '0) Kendimi üzgün hissetmiyorum',
                    '1) Kendimi üzgün hissediyorum',
                    '2) Her zaman için üzgünüm ve kendimi bu duygudan kurtaramıyorum',
                    '3) Öylesine üzgün ve mutsuzum ki dayanamıyorum'
                ],
                type: 'radio'
            },
            {
                question: '2. Karamsarlık',
                options: [
                    '0) Gelecek ile ilgili umutsuz ve karamsar değilim',
                    '1) Gelecek ile ilgili karamsarım',
                    '2) Gelecekten beklediğim hiçbir şey yok',
                    '3) Geleceğim ile ilgili hiçbir umudum yok ve bu durum düzelmeyecek'
                ],
                type: 'radio'
            },
            {
                question: '3. Geçmiş Başarısızlıklar',
                options: [
                    '0) Kendimi başarısız görmüyorum',
                    '1) Çevremdeki birçok kişiden daha fazla başarısızlıklarım oldu',
                    '2) Geriye dönüp baktığımda, çok fazla başarısızlığım olduğunu görüyorum',
                    '3) Kendimi tümüyle başarısız bir insan olarak görüyorum'
                ],
                type: 'radio'
            },
            {
                question: '4. Zevk Alamama',
                options: [
                    '0) Her şeyden eskisi kadar zevk alabiliyorum',
                    '1) Her şeyden eskisi kadar zevk alamıyorum',
                    '2) Artık hiçbir şeyden gerçek bir zevk alamıyorum',
                    '3) Bana zevk veren hiçbir şey yok, her şey çok sıkıcı'
                ],
                type: 'radio'
            },
            {
                question: '5. Suçluluk Duyguları',
                options: [
                    '0) Kendimi suçlu hissetmiyorum',
                    '1) Arada bir kendimi suçlu hissettiğim oluyor',
                    '2) Kendimi çoğunlukla suçlu hissediyorum',
                    '3) Kendimi her an için suçlu hissediyorum'
                ],
                type: 'radio'
            },
            {
                question: '6. Cezalandırılma Duyguları',
                options: [
                    '0) Cezalandırıldığımı düşünmüyorum',
                    '1) Bazı şeyler için cezalandırılabileceğimi hissediyorum',
                    '2) Cezalandırılmayı bekliyorum',
                    '3) Cezalandırıldığımı hissediyorum'
                ],
                type: 'radio'
            },
            {
                question: '7. Kendinden Hoşnutsuzluk',
                options: [
                    '0) Kendimden hoşnutum',
                    '1) Kendimden pek hoşnut değilim',
                    '2) Kendimden hiç hoşlanmıyorum',
                    '3) Kendimden nefret ediyorum'
                ],
                type: 'radio'
            },
            {
                question: '8. Öz Eleştiri',
                options: [
                    '0) Kendimi diğer insanlardan daha kötü görmüyorum',
                    '1) Kendimi zayıflıklarım ve hatalarım için eleştiriyorum',
                    '2) Kendimi hatalarım için her zaman suçluyorum',
                    '3) Her kötü olayda kendimi suçluyorum'
                ],
                type: 'radio'
            },
            {
                question: '9. İntihar Düşünceleri veya İstekleri',
                options: [
                    '0) Kendimi öldürmek gibi düşüncelerim yok',
                    '1) Bazen kendimi öldürmeyi düşünüyorum fakat bunu yapmam',
                    '2) Kendimi öldürmek isterdim',
                    '3) Fırsatını bulsam kendimi öldürürüm'
                ],
                type: 'radio'
            },
            {
                question: '10. Ağlama',
                options: [
                    '0) Her zamankinden daha fazla ağladığımı sanmıyorum',
                    '1) Eskisine göre şu sıralarda daha fazla ağlıyorum',
                    '2) Şu sıralarda her an ağlıyorum',
                    '3) Eskiden ağlayabilirdim ama şu sıralarda istesem de ağlayamıyorum'
                ],
                type: 'radio'
            },
            {
                question: '11. Sinirlilik',
                options: [
                    '0) Her zamankinden daha sinirli değilim',
                    '1) Her zamankinden daha kolayca sinirleniyor ve kızıyorum',
                    '2) Çoğu zaman sinirliyim',
                    '3) Eskiden sinirlendiğim şeylere bile artık sinirlenemiyorum'
                ],
                type: 'radio'
            },
            {
                question: '12. İlgi Kaybı',
                options: [
                    '0) Diğer insanlara karşı ilgimi kaybetmedim',
                    '1) Eskisine göre insanlarla daha az ilgiliyim',
                    '2) Diğer insanlara karşı ilgimin çoğunu kaybettim',
                    '3) Diğer insanlara karşı hiç ilgim kalmadı'
                ],
                type: 'radio'
            },
            {
                question: '13. Kararsızlık',
                options: [
                    '0) Kararlarımı eskisi kadar kolay ve rahat verebiliyorum',
                    '1) Şu sıralarda kararlarımı vermeyi erteliyorum',
                    '2) Kararlarımı vermekte oldukça güçlük çekiyorum',
                    '3) Artık hiç karar veremiyorum'
                ],
                type: 'radio'
            },
            {
                question: '14. Değersizlik',
                options: [
                    '0) Eskisinden daha kötü göründüğümü sanmıyorum',
                    '1) Yaşlandığımı ve çekiciliğimi kaybettiğimi düşünüyor ve üzülüyorum',
                    '2) Görünüşümde artık değiştirilmesi mümkün olmayan olumsuz değişiklikler olduğunu hissediyorum',
                    '3) Çok çirkin olduğumu düşünüyorum'
                ],
                type: 'radio'
            },
            {
                question: '15. Enerji Kaybı',
                options: [
                    '0) Eskisi kadar iyi çalışabiliyorum',
                    '1) Bir işe başlayabilmek için eskisine göre kendimi daha fazla zorlamam gerekiyor',
                    '2) Hangi iş olursa olsun, yapabilmek için kendimi çok zorluyorum',
                    '3) Hiçbir iş yapamıyorum'
                ],
                type: 'radio'
            },
            {
                question: '16. Uyku Düzeninde Değişiklik',
                options: [
                    '0) Eskisi kadar rahat uyuyabiliyorum',
                    '1) Eskisi kadar rahat uyuyamıyorum',
                    '2) Her zamankinden 1-2 saat erken uyanıyorum ve tekrar uyumakta zorluk çekiyorum',
                    '3) Her zamankinden çok daha erken uyanıyor ve tekrar uyuyamıyorum'
                ],
                type: 'radio'
            },
            {
                question: '17. Yorgunluk',
                options: [
                    '0) Her zamankinden daha çabuk yorulduğumu sanmıyorum',
                    '1) Her zamankinden daha çabuk yoruluyorum',
                    '2) Yaptığım her şey beni yoruyor',
                    '3) Kendimi hiçbir şey yapamayacak kadar yorgun hissediyorum'
                ],
                type: 'radio'
            },
            {
                question: '18. İştah Değişiklikleri',
                options: [
                    '0) İştahım her zamanki gibi',
                    '1) İştahım eskisi kadar iyi değil',
                    '2) İştahım çok azaldı',
                    '3) Artık hiç iştahım yok'
                ],
                type: 'radio'
            },
            {
                question: '19. Kilo Kaybı',
                options: [
                    '0) Son zamanlarda kilo vermedim',
                    '1) İki kilodan fazla kilo verdim',
                    '2) Dört kilodan fazla kilo verdim',
                    '3) Altı kilodan fazla kilo verdim'
                ],
                type: 'radio'
            },
            {
                question: '20. Sağlık Endişeleri',
                options: [
                    '0) Sağlığım beni her zamankinden fazla endişelendirmiyor',
                    '1) Ağrı, sancı, mide bozukluğu, kabızlık gibi rahatsızlıklar beni endişelendiriyor',
                    '2) Sağlığım beni endişelendirdiği için başka şeyleri düşünmek zorlaşıyor',
                    '3) Sağlığım hakkında o kadar endişeliyim ki başka hiçbir şey düşünemiyorum'
                ],
                type: 'radio'
            },
            {
                question: '21. Cinsel İsteğin Kaybı',
                options: [
                    '0) Son zamanlarda cinsel yaşantımda dikkatimi çeken bir şey yok',
                    '1) Eskisine oranla cinsel konularla daha az ilgileniyorum',
                    '2) Cinsel konularla şimdi çok daha az ilgiliyim',
                    '3) Cinsel konulara olan ilgimi tamamen kaybettim'
                ],
                type: 'radio'
            }
        ],
        interpretation: {
            '0-9': 'Minimal depresyon',
            '10-16': 'Hafif depresyon',
            '17-29': 'Orta düzeyde depresyon',
            '30-63': 'Şiddetli depresyon'
        }
    },
    stai: {
        title: 'Durumluk Kaygı Ölçeği (STAI FORM TX-1)',
        description: 'Aşağıda kişilerin kendilerine ait duygularını anlatmada kullandıkları bir takım ifadeler verilmiştir. Her ifadeyi okuyun, sonra da o anda nasıl hissettiğinizi ifadelerin sağ tarafındaki parantezlerden uygun olanını işaretleyerek belirtin.',
        questions: [
            {
                question: '1. Şu anda sakinim',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla'],
                reverse: true
            },
            {
                question: '2. Kendimi emniyette hissediyorum',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla'],
                reverse: true
            },
            {
                question: '3. Şu anda sinirlerim gergin',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla']
            },
            {
                question: '4. Pişmanlık duygusu içindeyim',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla']
            },
            {
                question: '5. Şu anda huzur içindeyim',
                type: 'radio',
                options: ['Hiç', 'Biraz', 'Çok', 'Tamamıyla'],
                reverse: true
            }
            // Not: Gerçek testte 40 soru vardır, örnek olarak 5 soru eklenmiştir
        ],
        interpretation: {
            '20-35': 'Hafif düzeyde kaygı',
            '36-41': 'Orta düzeyde kaygı',
            '42-80': 'Yüksek düzeyde kaygı'
        }
    },
    scl90: {
        title: 'SCL-90-R Belirti Tarama Listesi',
        description: 'Aşağıda zaman zaman herkeste olabilecek yakınma ve sorunların bir listesi vardır. Lütfen her birini dikkatlice okuyunuz. Sonra bu durumun bugün de dahil olmak üzere son bir ay içinde sizi ne ölçüde huzursuz ve tedirgin ettiğini göz önüne alarak aşağıdaki tanımlamalardan uygun olanının numarasını seçiniz.',
        questions: [
            {
                question: '1. Baş ağrısı',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            {
                question: '2. Sinirlilik ya da içinin titremesi',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            {
                question: '3. Zihinden atamadığınız yineleyici hoşa gitmeyen düşünceler',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            {
                question: '4. Baygınlık veya baş dönmesi',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            },
            {
                question: '5. Cinsel arzu ve ilginin kaybı',
                type: 'radio',
                options: ['Hiç', 'Çok az', 'Orta derecede', 'Oldukça fazla', 'İleri derecede']
            }
            // Not: Gerçek testte 90 soru vardır, örnek olarak 5 soru eklenmiştir
        ],
        interpretation: {
            '0-0.5': 'Normal düzey',
            '0.5-1.5': 'Orta düzey',
            '1.5-4': 'Yüksek düzey'
        }
    }
};

// Sayfa yüklendiğinde çalışacak kod
document.addEventListener('DOMContentLoaded', function() {
    let currentTest = null;
    let currentAnswers = [];
    const testModal = new bootstrap.Modal(document.getElementById('testModal'));

    // Testi başlat
    window.startTest = function(testType) {
        currentTest = testType;
        currentAnswers = [];
        const test = tests[testType];
        
        document.getElementById('testTitle').textContent = test.title;
        const testContent = document.getElementById('testContent');
        testContent.innerHTML = '';
        
        // Test açıklamasını ekle
        const descriptionDiv = document.createElement('div');
        descriptionDiv.className = 'alert alert-info mb-4';
        descriptionDiv.textContent = test.description;
        testContent.appendChild(descriptionDiv);
        
        document.getElementById('testResult').style.display = 'none';
        document.getElementById('submitTest').style.display = 'block';
        
        // Soruları oluştur
        test.questions.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'mb-4 p-4 bg-light rounded shadow-sm question-container';
            
            const questionHeader = document.createElement('h5');
            questionHeader.className = 'mb-3 text-primary';
            questionHeader.textContent = q.question;
            questionDiv.appendChild(questionHeader);
            
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options-container d-flex flex-column gap-2';
            
            q.options.forEach((option, optIndex) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'btn btn-outline-primary text-start option-button w-100';
                button.textContent = option;
                button.value = optIndex;
                button.name = `question${index}`;
                
                button.addEventListener('click', function() {
                    // Aynı sorudaki diğer butonların seçimini kaldır
                    optionsDiv.querySelectorAll('.btn').forEach(btn => {
                        btn.classList.remove('active', 'selected');
                    });
                    // Bu butonu seçili yap
                    this.classList.add('active', 'selected');
                });
                
                optionsDiv.appendChild(button);
            });
            
            questionDiv.appendChild(optionsDiv);
            testContent.appendChild(questionDiv);
        });
        
        testModal.show();
    }

    // Test sonuçlarını hesapla
    function calculateResults() {
        const test = tests[currentTest];
        let total = 0;
        let answeredQuestions = 0;
        
        test.questions.forEach((_, index) => {
            const selected = document.querySelector(`.options-container button[name="question${index}"].selected`);
            if (selected) {
                answeredQuestions++;
                total += parseInt(selected.value);
            }
        });
        
        if (answeredQuestions < test.questions.length) {
            return 'Lütfen tüm soruları yanıtlayınız.';
        }
        
        let interpretation = '';
        Object.entries(test.interpretation).forEach(([range, desc]) => {
            const [min, max] = range.split('-').map(Number);
            if (total >= min && total <= max) {
                interpretation = desc;
            }
        });
        
        return `
            <div class="card border-0 shadow">
                <div class="card-body">
                    <h4 class="card-title text-center mb-4">Test Sonucunuz</h4>
                    <div class="result-details">
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <div class="score-box text-center p-3 bg-light rounded">
                                    <h5 class="mb-2">Toplam Puan</h5>
                                    <h2 class="text-primary mb-0">${total}</h2>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="interpretation-box text-center p-3 bg-light rounded">
                                    <h5 class="mb-2">Değerlendirme</h5>
                                    <h4 class="text-primary mb-0">${interpretation}</h4>
                                </div>
                            </div>
                        </div>
                        <div class="alert alert-warning mt-4">
                            <h5 class="alert-heading"><i class="fas fa-exclamation-triangle me-2"></i>Önemli Not</h5>
                            <p class="mb-0">Bu test sonuçları yalnızca bilgilendirme amaçlıdır ve kesin bir tanı niteliği taşımaz. 
                            Profesyonel bir değerlendirme için mutlaka bir ruh sağlığı uzmanına başvurunuz.</p>
                        </div>
                    </div>
                </div>
            </div>`;
    }

    // Testi tamamla butonu için event listener
    document.getElementById('submitTest').addEventListener('click', () => {
        const result = calculateResults();
        const resultDiv = document.getElementById('testResult');
        
        if (result === 'Lütfen tüm soruları yanıtlayınız.') {
            Swal.fire({
                icon: 'warning',
                title: 'Uyarı',
                text: result,
                confirmButtonText: 'Tamam'
            });
            return;
        }
        
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = result;
        document.getElementById('submitTest').style.display = 'none';
    });
});
