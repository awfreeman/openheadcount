function drawDot(ctx, array){
    ctx.fillStyle = 'blue'
    ctx.beginPath()
    ctx.arc(array[0], array[1], 3, 0, Math.PI * 2, true)
    ctx.fill()
}
function drawLine(ctx, array, i){
    ctx.beginPath()
    ctx.strokeStyle = 'blue'
    ctx.lineWidth = 5
    ctx.moveTo(array[i][0], array[i][1])
    if((i+1)==array.length){
        ctx.lineTo(array[0][0], array[0][1])
        ctx.stroke()
    }
    else{
        ctx.lineTo(array[i+1][0], array[i+1][1])
        ctx.stroke()
    }
}
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
    array.push([x,y])
    ctx.drawImage(img, 0, 0)
    if(array.length == 1){
        drawDot(ctx, array[0])
    }
    else{
        for(let i = 0; i<array.length; i++){
            drawDot(ctx, array[i])
            drawLine(ctx, array, i)
        }
    }
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
    ctx.clearRect(0, 0, c.width, c.height)
    ctx.drawImage(img, 0, 0)
    console.log("cleared")
})
