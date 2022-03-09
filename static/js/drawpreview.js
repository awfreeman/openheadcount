function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
async function drawImage() {
    let c = document.getElementById("window")
    let counter = document.getElementById("counter")
    let ctx = c.getContext("2d")
    let accum 
    while (true) {
        let img = new Image()
        let url = '/previewframe'
        fetch(url)
        .then(response => response.blob())
        .then(imageBlob => {
            return URL.createObjectURL(imageBlob)})
        .then(url => {img.src=url})
        img.onload = function() {
            ctx.drawImage(img, 0, 0)
        }
        fetch('/getcount').then(response => response.text()).then(text =>{
            counter.innerHTML="Current Count:"+text
        })
        await sleep(100)
    }
}
drawImage()