
loadIssues();
let currentIssueId = null;
async function loadIssues(){

    try{

        const container =
        document.getElementById(
            "issuesContainer"
        );

        container.innerHTML =
        "Loading issues...";

        const response =
        await fetch(
            "http://127.0.0.1:5000/issues"
        );

        const issues =
        await response.json();

        container.innerHTML = "";

        if(!issues.length){

            container.innerHTML =
            "No issues found 🚫";

            return;

        }

        issues.forEach(issue => {

            let imageUrl;

            if(issue.image){

                imageUrl =
                `http://127.0.0.1:5000/uploads/${issue.image}`;

            }

            else{

                imageUrl =
                "https://via.placeholder.com/400x220?text=No+Image";

            }

            container.innerHTML += `

                <div class="issue-card" 
                data-type="${issue.type}"
                data-status="${issue.status}">

                      
                    <img
                        src="${imageUrl}"
                        class="issue-image"
                    >

                    <div class="issue-content">

                        <h2 class="issue-title">
                            ${issue.title}
                        </h2>

                        <span class="issue-type">
                            ${issue.type}
                        </span>

                        <p class="issue-description">
                            ${issue.description}
                        </p>

                        <p class="issue-location">
                            📍 ${issue.location}
                        </p>

                        <select
    class="status-select"
    onchange="updateStatus(${issue.id}, this.value)">

    <option
        value="Reported"
        ${issue.status==="Reported"?"selected":""}>
        Reported
    </option>

    <option
        value="In Progress"
        ${issue.status==="In Progress"?"selected":""}>
        In Progress
    </option>

    <option
        value="Resolved"
        ${issue.status==="Resolved"?"selected":""}>
        Resolved
    </option>

</select>
                        <div class="issue-stats">

    <span id="votes-${issue.id}">
        👍 0
    </span>

    <span id="comments-${issue.id}">
        💬 0
    </span>

</div>
                        <div class="issue-actions">

    <button
        onclick="voteIssue(${issue.id})"
        class="vote-btn">

        👍 Vote

    </button>

    <button
        onclick="viewComments(${issue.id})"
        class="comment-btn">

        💬 Comments

    </button>

</div>
                    </div>

                </div>

            `;

            loadCounts(issue.id);
        });

    }

    catch(error){

        console.error(error);

        document.getElementById(
            "issuesContainer"
        ).innerHTML =
        "Failed to load data. Please try again.";
    }
}

function logout(){

    localStorage.clear();

    window.location.href =
    "login.html";
}
function goDashboard(){

    window.location.href =
    "dashboard.html";
}
async function voteIssue(issueId){

    const user =
    JSON.parse(
        localStorage.getItem("user")
    );

    const token =
    localStorage.getItem("token");

    try{

        const response =
        await fetch(
            "http://127.0.0.1:5000/vote",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":
                    `Bearer ${token}`
                },

                body:JSON.stringify({
                    issue_id: issueId,
                    user_id: user.id
                })
            }
        );

        const data =
        await response.json();

        alert(data.message);
        // refresh the displayed counts for this issue
        loadCounts(issueId);
        

    }

    catch(error){

        console.error(error);

        alert("Error voting");
    }
}
async function viewComments(issueId){
      currentIssueId = issueId;
    try{

        const commentsList =
        document.getElementById(
            "commentsList"
        );

        commentsList.innerHTML =
        "Loading comments...";

        document.getElementById(
            "commentModal"
        ).style.display =
        "block";

        const response =
        await fetch(
            `http://127.0.0.1:5000/comments/${issueId}`
        );

        const comments =
        await response.json();

        commentsList.innerHTML = "";

        if(!comments.length){

            commentsList.innerHTML =
            "No comments yet 💬";

            return;

        }

        comments.forEach(comment => {

            commentsList.innerHTML += `

                <div class="comment-item">

                    <p>
                        ${comment.comment}
                    </p>

                </div>

            `;
        });

    }

    catch(error){

        console.error(error);

        document.getElementById(
            "commentsList"
        ).innerHTML =
        "Failed to load data. Please try again.";
    }
}
function closeModal(){

    document.getElementById(
        "commentModal"
    ).style.display =
    "none";
}
async function addComment(){
    
    const comment =
    document.getElementById(
        "newComment"
    ).value;
    if(!comment.trim()){

    alert("Please enter a comment");

    return;
}

    const token =
    localStorage.getItem(
        "token"
    );

    try{

        const response =
        await fetch(
            "http://127.0.0.1:5000/comments",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json",

                    "Authorization":
                    `Bearer ${token}`
                },

                body:JSON.stringify({

                    issue_id:
                    currentIssueId,

                    comment:
                    comment

                })
            }
        );

        const data =
        await response.json();

        alert(data.message);

        document.getElementById(
            "newComment"
        ).value = "";

        viewComments(
            currentIssueId
        );
        viewComments(currentIssueId);

    }

    catch(error){

        console.error(error);
    }
}
async function loadCounts(issueId){

    try{

        const voteResponse =
        await fetch(
            `http://127.0.0.1:5000/issues/${issueId}/votes`
        );

        const voteData =
        await voteResponse.json();

        document.getElementById(
            `votes-${issueId}`
        ).innerText =
        `👍 ${voteData.votes}`;

        const commentResponse =
        await fetch(
            `http://127.0.0.1:5000/comments/count/${issueId}`
        );

        const commentData =
        await commentResponse.json();

        document.getElementById(
            `comments-${issueId}`
        ).innerText =
        `💬 ${commentData.comments}`;

    }

    catch(error){

        console.error(error);
    }
}

function searchIssues(){

    const value =
    document.getElementById(
        "searchBox"
    ).value.toLowerCase();

    const cards =
    document.querySelectorAll(
        ".issue-card"
    );

    cards.forEach(card => {

        const text =
        card.innerText.toLowerCase();

        card.style.display =
        text.includes(value)
        ? "block"
        : "none";

    });

}
function searchIssues(){

    const value =
    document.getElementById(
        "searchBox"
    ).value.toLowerCase();

    const cards =
    document.querySelectorAll(
        ".issue-card"
    );

    cards.forEach(card=>{

        card.style.display =
        card.innerText
        .toLowerCase()
        .includes(value)
        ? "block"
        : "none";

    });
}
function filterIssues(){

    const type =
    document.getElementById(
        "typeFilter"
    ).value;

    const status =
    document.getElementById(
        "statusFilter"
    ).value;

    const cards =
    document.querySelectorAll(
        ".issue-card"
    );

    cards.forEach(card => {

        const matchesType =
            !type ||
            card.dataset.type === type;

        const matchesStatus =
            !status ||
            card.dataset.status === status;

        card.style.display =
            matchesType &&
            matchesStatus
            ? "block"
            : "none";

    });

}
async function updateStatus(
    issueId,
    status
){

    const token =
    localStorage.getItem(
        "token"
    );

    try{

        const response =
        await fetch(

            `http://127.0.0.1:5000/issues/${issueId}/status`,

            {
                method:"PUT",

                headers:{
                    "Content-Type":
                    "application/json",

                    "Authorization":
                    `Bearer ${token}`
                },

                body:JSON.stringify({
                    status
                })
            }
        );

        const data =
        await response.json();

        alert(
            data.message
        );

    }

    catch(error){

        console.error(error);

    }

}