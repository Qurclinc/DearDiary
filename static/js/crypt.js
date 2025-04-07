
const inputArea = document.querySelector("textarea[name='input_text']");
const outputArea = document.querySelector("textarea[name='output_text']");
const keyInput = document.querySelector("input[name='key']");

keyInput.value = "";
outputArea.value = "";

try {
    const decrypt_button = document.getElementById("decrypt-btn");
    decrypt_button.addEventListener("click", async() => {
        const inputText = inputArea.value;
        const key = keyInput.value;
        if (inputText == "") {
            alert("Введите зашифрованный текст.");
            return;
        } else if (key == "") {
            alert("Введите ключ шифрования.")
            return;
        }

        try {
            const response = await fetch("/api/v1/deardiary/decrypt", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: inputText,
                    key: key
                })
            });

            if (!response.ok) throw new Error("Ошибка при запросе");

            const data = await response.json();
            outputArea.value = data.data || "";
            outputArea.style.height = outputArea.scrollHeight + "px"
            
        }
        catch (error) {
            alert("Ошибка: Не удалось расшифровать текст")
        }
    })
} catch (err) { }

try {
    const encrypt_button = document.getElementById("encrypt-btn");
    encrypt_button.addEventListener("click", async() => {
        const inputText = inputArea.value;
        const key = keyInput.value;
        if (inputText == "") {
            alert("Введите зашифрованный текст.");
            return;
        } else if (key == "") {
            alert("Введите ключ шифрования.")
            return;
        }

        try {
            const response = await fetch("/api/v1/deardiary/encrypt", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: inputText,
                    key: key
                })
            });

            if (!response.ok) throw new Error("Ошибка при запросе");

            const data = await response.json();
            outputArea.value = data.data || "";
            outputArea.style.height = outputArea.scrollHeight + "px"
        }
        catch (error) {
            alert("Ошибка: Не удалось расшифровать текст")
        }
    })
} catch (err) {}