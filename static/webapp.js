window.onload = initialize

let playlist
let video_list
let fet

function initialize() {
    playlist = document.getElementById('playlist')
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function generate() {
    let url = document.getElementById('url').value
    let api_url = getAPIBaseURL() + '/convert/' + encodeURI(url)
    fetch(api_url, {method: 'get'})
    .then((response) => response.json())
    .then((featur) => {
        fet = featur
        video_list = ''
        featur.playlist.forEach(element => {
            video_list += `<div><h2>${element.track_name} - ${element.track_album} by ${element.track_singer} </h2></div>
            <iframe width="420" height="315" src="${element.best_url}"></iframe>`
        });
        playlist.innerHTML = video_list
    })
}