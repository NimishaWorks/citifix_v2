const map = L.map(
    "map"
).setView(
    [13.0827,80.2707],
    11
);

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
        "&copy; OpenStreetMap contributors"
    }
).addTo(map);

loadIssues();

async function loadIssues(){

    try{

        const response =
        await fetch(
            "http://127.0.0.1:5000/issues"
        );

        const issues =
        await response.json();

        issues.forEach(issue => {

            L.marker([
                issue.latitude,
                issue.longitude
            ])

            .addTo(map)

            .bindPopup(`

                <b>
                    ${issue.title}
                </b>

                <br>

                ${issue.type}

                <br>

                ${issue.location}

                <br>

                Status:
                ${issue.status}

            `);

        });

    }

    catch(error){

        console.error(error);

    }

}

function goDashboard(){

    window.location.href =
    "dashboard.html";

}
if(navigator.geolocation){

    navigator.geolocation.getCurrentPosition(

        function(position){

            map.setView(

                [
                    position.coords.latitude,
                    position.coords.longitude
                ],

                14

            );

            L.marker([

                position.coords.latitude,
                position.coords.longitude

            ])

            .addTo(map)

            .bindPopup(

                "📍 You are here"

            );

        }

    );

}