const user =
JSON.parse(
    localStorage.getItem("user")
);

if(user){

    document.getElementById(
        "welcomeUser"
    ).innerText =
    `Welcome ${user.name} 👋`;

}

function logout(){

    localStorage.clear();

    window.location.href =
    "login.html";

}

const dashboardLoadingMessage =
document.createElement("div");

dashboardLoadingMessage.id =
"dashboardLoadingMessage";

dashboardLoadingMessage.innerText =
"Loading dashboard...";

dashboardLoadingMessage.style.cssText =
"margin:24px 40px;padding:16px 20px;background:#fff;border-radius:16px;box-shadow:0 10px 25px rgba(0,0,0,.08);color:#163B65;font-weight:600;";

document.body.insertBefore(
dashboardLoadingMessage,
document.body.children[1]
);

loadAnalytics();
loadRecentIssues();

async function loadAnalytics(){

    const token =
    localStorage.getItem("token");

    try{

        const response =
        await fetch(
            "http://127.0.0.1:5000/analytics",
            {
                headers:{
                    Authorization:
                    `Bearer ${token}`
                }
            }
        );

        const data =
        await response.json();

        document.getElementById(
            "totalIssues"
        ).innerText =
        data.total_issues;

        document.getElementById(
            "reportedIssues"
        ).innerText =
        data.reported;

        document.getElementById(
            "resolvedIssues"
        ).innerText =
        data.resolved;

        document.getElementById(
            "inProgressIssues"
        ).innerText =
        data.in_progress;

        document.getElementById(
            "totalComments"
        ).innerText =
        data.total_comments;

        document.getElementById(
            "totalVotes"
        ).innerText =
        data.total_votes;

        const ctx =
        document.getElementById(
            "statusChart"
        );

        new Chart(ctx, {

            type: "doughnut",

            data: {

                labels: [
                    "Reported",
                    "Resolved",
                    "In Progress"
                ],

                datasets: [{

                    data: [
                        data.reported,
                        data.resolved,
                        data.in_progress
                    ]

                }]

            }

        });

        const loadingMessage =
        document.getElementById(
            "dashboardLoadingMessage"
        );

        if(loadingMessage){

            loadingMessage.remove();

        }

    }

    catch(error){

        console.error(error);

        const loadingMessage =
        document.getElementById(
            "dashboardLoadingMessage"
        );

        if(loadingMessage){

            loadingMessage.innerText =
            "Failed to load data. Please try again.";

        }

    }

}

async function loadRecentIssues(){

    try{

        const response =
        await fetch(
            "http://127.0.0.1:5000/issues"
        );

        const issues =
        await response.json();

        const tbody =
        document.getElementById(
            "recentIssuesBody"
        );

        if(!tbody){

            console.error(
                "recentIssuesBody not found"
            );

            return;

        }

        tbody.innerHTML = "";

        issues.slice(0,5).forEach(issue => {

            tbody.innerHTML += `

                <tr>

                    <td>${issue.title}</td>

                    <td>${issue.type}</td>

                    <td>${issue.status}</td>

                    <td>${issue.location}</td>

                </tr>

            `;

        });

    }

    catch(error){

        console.error(error);

    }

}