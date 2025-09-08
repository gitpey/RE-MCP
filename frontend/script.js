document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');

    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const area = document.getElementById('area').value;
        const propertyType = document.getElementById('property-type').value;

        // Use a relative URL for the API call
        const response = await fetch(`/search?area=${area}&property_type=${propertyType}`);
        const data = await response.json();

        resultsContainer.innerHTML = ''; // Clear previous results

        if (data.results && data.results.length > 0) {
            data.results.forEach(property => {
                const propertyDiv = document.createElement('div');
                propertyDiv.className = 'property';
                propertyDiv.innerHTML = `
                    <h3>${property.address}</h3>
                    <p><strong>City:</strong> ${property.city}</p>
                    <p><strong>Region:</strong> ${property.region}</p>
                    <p><strong>Type:</strong> ${property.property_type}</p>
                    <p><strong>Price:</strong> $${property.price.toLocaleString()}</p>
                    <p><strong>Bedrooms:</strong> ${property.bedrooms}</p>
                    <p><strong>Bathrooms:</strong> ${property.bathrooms}</p>
                `;
                resultsContainer.appendChild(propertyDiv);
            });
        } else {
            resultsContainer.innerHTML = '<p>No properties found.</p>';
        }
    });
});
