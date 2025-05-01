console.log("JS loaded");

async function submitApplication() {
    const name = document.getElementById('name').value;
    const zipcode = document.getElementById('zipcode').value;

    const response = await fetch('/api/add_application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, zipcode })
    });

    const data = await response.json();
    document.getElementById('confirmation').innerText = `Application submitted. Your application number is ${data.application_number}`;
}

async function updateStatus() {
    const name = document.getElementById('statusName').value;
    const status = document.getElementById('newStatus').value;

    const response = await fetch('/api/update_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, status })
    });

    const data = await response.json();
    alert(data.message);
}

async function updateStatusById() {
    console.log("updateStatusById clicked ✅");

    const application_number = document.getElementById('updateAppId').value;
    const status = document.getElementById('statusDropdown').value;

    const response = await fetch('/api/update_status_by_id', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ application_number, status })
    });

    const data = await response.json();
    alert(data.message);
}


async function checkStatus() {
    const application_number = document.getElementById('checkAppId').value;

    const response = await fetch('/api/check_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ application_number })
    });

    const data = await response.json();
    document.getElementById('statusResult').innerText = "Status: " + data.status;
}

async function addNote() {
    const name = document.getElementById('noteName').value;
    const subphase = document.getElementById('subphase').value;
    const message = document.getElementById('noteMessage').value;

    const response = await fetch('/api/add_note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, subphase, message })
    });

    const data = await response.json();
    alert(data.message);
}

async function viewApplication() {
    const name = document.getElementById('viewName').value;

    const response = await fetch(`/api/notes?name=${encodeURIComponent(name)}`);
    const data = await response.json();

    const result = document.getElementById('result');
    result.textContent = JSON.stringify(data, null, 2);
}

async function viewNotesByAppId() {
    const appId = document.getElementById('noteAppId').value;

    const response = await fetch('/api/get_notes_by_id', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ application_number: appId })
    });

    const data = await response.json();
    const result = document.getElementById('noteResults');
    result.textContent = JSON.stringify(data.notes || data, null, 2);
}
