function iniciarVoz() {

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "pt-BR";
    recognition.continuous = false;
    recognition.interimResults = false;

    let terminou = false; // 👈 controle

    recognition.onstart = () => {
        console.log("🎤 Gravando...");
    };

    recognition.onresult = (event) => {
        terminou = true;

        const texto = event.results[0][0].transcript.toLowerCase();

        console.log("✅ Você disse:", texto);

        recognition.stop(); // 👈 FORÇA PARAR

        irPara("pergunta");

        setTimeout(() => {

            const input = document.getElementById("texto");

            if (input) {
                input.value = texto;
            }

            if (texto.includes("leão") || texto.includes("leao") || texto.includes("rei da selva")){
                selecionarAnimal("leão");
            } else if (texto.includes("elefante")) {
                selecionarAnimal("elefante");
            } else if (texto.includes("girafa")) {
                selecionarAnimal("girafa");
            } else if (texto.includes("mapa") || texto.includes("onde fica") || texto.includes("localização")){                irPara("mapa");
            }

        document.getElementById("texto").value = texto;
        enviar();   // 👈 usa a mesma função do botão
        }, 200);
    };

    recognition.onerror = (event) => {
        console.error("❌ Erro:", event.error);
        recognition.stop();
    };

    recognition.onend = () => {
        console.log("⛔ Parou de ouvir");

        // 👇 se não capturou nada, evita travar
        if (!terminou) {
            console.log("⚠️ Nenhuma fala detectada");
        }
    };

    // 👇 SEGURANÇA: para sozinho depois de 4s
    setTimeout(() => {
        recognition.stop();
    }, 4000);

    recognition.start();
}

   function enviarParaBackend(texto) {
    fetch("/pergunta", {   // 👈 MUITO IMPORTANTE
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ texto: texto })
    })
    .then(res => res.json())
    .then(data => {

        console.log("📡 Resposta backend:", data); // 👈 DEBUG

        document.getElementById("resposta").innerText = data.resposta;

        // 🎟️ voucher
        if (data.voucher) {
            document.getElementById("voucher").innerText = "Código: " + data.voucher;

            if (data.mensagem) {
                document.getElementById("infoVoucher").innerText =
                    data.mensagem + " (até " + data.expira_em + ")";
            }
        }

        // 🔊 áudio (se existir)
        if (data.audio) {
            const audio = document.getElementById("audio");
            audio.src = data.audio;
            audio.play();
        }

        // 👉 abre popup automaticamente
        document.getElementById("popup").style.display = "block";

    })
    .catch(err => {
        console.error("❌ Erro na requisição:", err);
    });
} 

function selecionarAnimal(animal) {

    console.log("Animal clicado:", animal);

    // coloca no input
    const input = document.getElementById("texto");
    if (input) {
        input.value = animal;
    }

    // envia pro backend
    enviarParaBackend(animal);
}