array = new Array()
let c = document.getElementById("window");
let button = document.getElementById("confirm")
let clearbutton = document.getElementById("clear")
let ctx = c.getContext("2d")
let img = new Image()
img.onload = function() {
    ctx.drawImage(img, 0, 0)
}
img.src = '/previewframe';
let lastx = null
let lasty = null
c.addEventListener('click', function(event){
    let x = event.pageX - c.offsetLeft
    let y = event.pageY - c.offsetTop
    if(lastx!=null){
        ctx.strokeStyle = 'blue'
        ctx.linewidth = 5
        ctx.beginPath()
        ctx.moveTo(lastx, lasty)
        ctx.lineTo(x, y)
        ctx.stroke()
        
    }
    lastx = x
    lasty = y
    array.push([x,y])
})
button.addEventListener('click', function(event){
    console.log(array.toString())
    
    const response = fetch("/configure", {
        method : 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(array),
        })
})
clearbutton.addEventListener('click', function(event){
    array = new Array()
    console.log("cleared")
})
