document.addEventListener('DOMContentLoaded', function() {
    function typeWriter(element, text, delay = 100) {
        let i = 0;
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, delay);
            }
        }
        type();
    }

    const text1 = "Hi! Boost Your Brainpower With Me!";
    const text2 = "";
    
    const typewriterText = document.getElementById('typewriter-text');
    const typewriterText2 = document.getElementById('typewriter-text2');

    typeWriter(typewriterText, text1, 100);
    setTimeout(() => {
        typeWriter(typewriterText2, text2, 50);
    }, text1.length * 100 + 500);
});

