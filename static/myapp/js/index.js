document.addEventListener('DOMContentLoaded', init);
let STATUS = true;
const FRAMES = {
  happy: 18,
  // Add more emotions and frame counts as needed
};

function init() {
  let currentFrameIndex = 1;

  // Initial interval for checking emotion every 10 seconds
  setInterval(() => {
    updateFrameWithEmotion().then(() => {
      resetAnimation();
    });
  }, 5 * 1000);

  function updateFrameWithEmotion() {
    return emotion()
      .then((emotion) => {
        console.log(emotion);
        return new Promise((resolve) => {
          waitUntilTrue(() => STATUS === true, () => {
            currentFrameIndex = 1;
            const frameInterval = setInterval(() => {
              updateFrame(emotion, frameInterval, resolve);
            }, 1000 / 11);
          });
        });
      })
      .catch((error) => {
        console.error('Error fetching emotion:', error);
      });
  }

  function updateFrame(emotion, frameInterval, resolve) {
    const animationFrame = document.getElementById('animationFrame');
    const newImageSrc = `/static/myapp/img/happy/${emotion}-frame${currentFrameIndex}.png`;
    animationFrame.src = newImageSrc;
    animationFrame.alt = `Frame ${currentFrameIndex}`;

    currentFrameIndex++;

    if (currentFrameIndex > FRAMES[emotion]) {
      clearInterval(frameInterval);
      STATUS = false;
      resolve(); // Resolve the promise to continue with the next iteration
    }
  }

  function resetAnimation() {
    currentFrameIndex = 1;
    STATUS = true;
  }

  function waitUntilTrue(condition, callback) {
    if (condition()) {
      callback();
    } else {
      setTimeout(() => waitUntilTrue(condition, callback), 100);
    }
  }
}

function emotion() {
  return fetch('/myapp/emotion', {
    method: 'GET',
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.emotion);
      return data.emotion;
    });
}
