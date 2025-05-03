const input = document.getElementById('city-input');
const suggestions = document.getElementById('suggestions');

input.addEventListener('input', async function () {
    if (input.value.length < 2) {
        suggestions.innerHTML = '';
        return;
    }

    const response = await fetch(`/autocomplete/?q=${input.value}`);
    const cities = await response.json();

    suggestions.innerHTML = '';
    cities.forEach(city => {
        const div = document.createElement('div');
        div.className = 'list-group-item list-group-item-action';
        div.textContent = city.name;
        div.onclick = () => {
            input.value = city.name;
            suggestions.innerHTML = '';
        };
        suggestions.appendChild(div);
    });
});
