// JSON received as an array.
const downloadPlaylist = (tracks_json, playlist_name) => {
    tracks = tracks_json.map((tr) =>
        `${tr.artists[0].name} - ${tr.name}`
    );
    fileContents = tracks.join('\n');
    let txtFile = new File([fileContents], `${playlist_name}.txt`, { type: "text/plain" });
    const link = document.createElement('a');
    const fileUrl = URL.createObjectURL(txtFile);
    link.href = fileUrl;
    link.download = txtFile.name;
    link.click();
    URL.revokeObjectURL(txtFile);
}


// JSON received as an array
const downloadAllPlaylists = (playlists_json) => {
    let tracks = []
    for (pl of playlists_json) {
        tracks.push(...pl.tracks);
    }
    downloadPlaylist(tracks, "All");
}


const toggleTracks = (playlist_name) => {
    const tracksContainer = document.getElementById(playlist_name);
    
    if (tracksContainer.classList.contains('hidden')) {
        tracksContainer.classList.remove('hidden');
    }
    else {
        tracksContainer.classList.add('hidden');
    }
}