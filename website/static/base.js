document.getElementById('startButton').addEventListener('click', function() {
    fetch('/start-game', { method: 'POST' })
    .then(response => response.text())
    .catch(error => console.error('Error:', error));
});

document.getElementById('startButton2').addEventListener('click', function() {
    fetch('/start-game2', { method: 'POST' })
    .then(response => response.text())
    .catch(error => console.error('Error:', error));
});

function deleteNote(noteId) {
    fetch("/delete-note", {method: "POST", body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/profile";
    });
  }