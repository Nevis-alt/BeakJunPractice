window.music_controls = {
    setSource: (file) => {
        document.getElementById("music").src = file;
    },
    play: () => document.getElementById("music").play(),
    pause: () => document.getElementById("music").pause(),
    getCurrentTime: () => document.getElementById("music").currentTime
};
