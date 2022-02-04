function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
async function drawImage() {
    var c = document.getElementById("window")
    var ctx = c.getContext("2d")
    while (true) {
        var img = new Image()
        let url = '/previewframe'
        let imageurl
        fetch(url)
        .then(response => response.blob())
        .then(imageBlob => {
            return URL.createObjectURL(imageBlob)})
        .then(url => {img.src=url})
        img.onload = function() {
            ctx.drawImage(img, 0, 0)
        }
        await sleep(100)
    }
}
drawImage()