console.log("Site do Neymar carregado com sucesso.");

const API_MENSAGENS = "http://localhost:5000/mensagens";

async function listarMensagens() {
    const lista = document.getElementById("listaMensagens");
    if (!lista) return;

    try {
        const resposta = await fetch(API_MENSAGENS);
        if (!resposta.ok) throw new Error("Falha ao buscar mensagens");

        const mensagens = await resposta.json();
        lista.replaceChildren();

        if (mensagens.length === 0) {
            const item = document.createElement("li");
            item.textContent = "Ainda não há mensagens.";
            lista.appendChild(item);
            return;
        }

        mensagens.forEach((mensagem) => {
            const item = document.createElement("li");
            item.textContent =
                `${mensagem.nome} (${mensagem.email}): ${mensagem.mensagem}` +
                (mensagem.data_envio ? ` — ${mensagem.data_envio}` : "");
            lista.appendChild(item);
        });
    } catch (erro) {
        document.getElementById("statusContato").textContent =
            "Não foi possível carregar as mensagens. Confira se a API está ligada.";
    }
}

const formulario = document.getElementById("formContato");

if (formulario) {
    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const dados = {
            nome: document.getElementById("nome").value.trim(),
            email: document.getElementById("email").value.trim(),
            mensagem: document.getElementById("mensagem").value.trim()
        };

        const status = document.getElementById("statusContato");

        try {
            const resposta = await fetch(API_MENSAGENS, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dados)
            });

            const resultado = await resposta.json();
            if (!resposta.ok) {
                throw new Error(resultado.erro || "Falha no cadastro");
            }

            status.textContent = "Mensagem enviada com sucesso!";
            formulario.reset();
            await listarMensagens();
        } catch (erro) {
            status.textContent =
                "Não foi possível enviar. Confira se a API e o MySQL estão funcionando.";
        }
    });

    listarMensagens();
}
