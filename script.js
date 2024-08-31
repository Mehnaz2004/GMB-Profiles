document.addEventListener('DOMContentLoaded', () => {
    fetch('escape_rooms_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Debugging output
            const container = document.getElementById('escape-rooms-container');
            data.forEach(room => {
                const card = document.createElement('div');
                card.classList.add('card');

                const name = document.createElement('h2');
                name.textContent = room.name;

                const address = document.createElement('p');
                address.textContent = `Address: ${room.address}`;

                const phone = document.createElement('p');
                phone.textContent = `Phone: ${room.phone_number}`;

                const hours = document.createElement('p');
                hours.textContent = `Hours: ${room.hours_of_operation}`;

                const website = document.createElement('p');
                website.textContent = `Website: `;
                const websiteLink = document.createElement('a');
                websiteLink.href = room.website;
                websiteLink.textContent = room.website;
                websiteLink.target = '_blank';
                website.appendChild(websiteLink);

                const reviewScore = document.createElement('p');
                reviewScore.textContent = `Review Score: ${room.review_score}`;

                card.appendChild(name);
                card.appendChild(address);
                card.appendChild(phone);
                card.appendChild(hours);
                card.appendChild(website);
                card.appendChild(reviewScore);

                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error fetching the JSON data:', error);
        });
});
