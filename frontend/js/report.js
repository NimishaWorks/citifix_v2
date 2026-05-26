async function reportIssue(){

    const user =
    JSON.parse(
        localStorage.getItem("user")
    );

    const token =
    localStorage.getItem("token");

    try{

        let imageFilename = null;

        const imageFile =
        document.getElementById("image").files[0];

        if(imageFile){

            const formData =
            new FormData();

            formData.append(
                "image",
                imageFile
            );

            const uploadResponse =
            await fetch(
                "http://127.0.0.1:5000/upload-image",
                {
                    method:"POST",
                    body:formData
                }
            );

            const uploadData =
            await uploadResponse.json();

            imageFilename =
            uploadData.filename;
        }

        const issueData = {

            title:
            document.getElementById("title").value,

            description:
            document.getElementById("description").value,

            type:
            document.getElementById("type").value,

            location:
            document.getElementById("location").value,

            latitude:
            parseFloat(
                document.getElementById("latitude").value
            ),

            longitude:
            parseFloat(
                document.getElementById("longitude").value
            ),

            image:
            imageFilename,

            user_id:
            user.id
        };

        const response =
        await fetch(
            "http://127.0.0.1:5000/issues",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":
                    `Bearer ${token}`
                },

                body:
                JSON.stringify(issueData)
            }
        );

        const result =
        await response.json();

        alert("Issue reported successfully!");

window.location.href =
"issues.html";

    }

    catch(error){

        console.error(error);

        alert("Error reporting issue");

    }

}
function getLocation(){

    if(!navigator.geolocation){

        alert(
            "Geolocation not supported"
        );

        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position){

            document.getElementById(
                "latitude"
            ).value =
            position.coords.latitude;

            document.getElementById(
                "longitude"
            ).value =
            position.coords.longitude;

            alert(
                "Location captured successfully"
            );

        },

        function(error){

            alert(
                "Unable to fetch location"
            );

            console.error(error);

        }

    );
}
async function getLocation(){

    if(!navigator.geolocation){

        alert(
            "Geolocation not supported"
        );

        return;
    }

    navigator.geolocation.getCurrentPosition(

        async function(position){

            const lat =
            position.coords.latitude;

            const lon =
            position.coords.longitude;

            document.getElementById(
                "latitude"
            ).value = lat;

            document.getElementById(
                "longitude"
            ).value = lon;

            try{

                const response =
                await fetch(
                    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
                );

                const data =
                await response.json();

                document.getElementById(
                    "location"
                ).value =
                data.address.city ||
                data.address.town ||
                data.address.village ||
                data.display_name;

            }

            catch(error){

                console.error(error);

            }

        },

        function(error){

            console.error(error);

            alert(
                "Unable to fetch location"
            );

        }

    );

}