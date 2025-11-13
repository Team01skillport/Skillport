document.getElementById("like-button").addEventListener("click", function () {
  const videoId = this.dataset.videoId;
  console.log("AJAX RUN");

  fetch(`/lesson_video/like_video/${videoId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
});
