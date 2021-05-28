const host = "127.0.0.1"
const port = "8080"
async function getStatus() {
    const result = await axios.get("http://13.209.76.100:8080/status")
    const data = result.data.data
    // console.log(data)

    const {time, cmd_string, is_finish} = data.command
    const {num1} = data.sense
    var img_cmd = document.querySelector("#cmd")
    
    img_cmd.style.backgroundSize = "contain"
    if(cmd_string === "go") {
        img_cmd.style.backgroundImage = "url('go.jpg')"
        console.log("go");
    } else if(cmd_string == "left") {
        img_cmd.style.backgroundImage = "url('left.jpg')"
        console.log("left");
    } else if(cmd_string == "right") {
        img_cmd.style.backgroundImage = "url('right.jpg')"
        console.log("right");
    } else if(cmd_string == "back") {
        img_cmd.style.backgroundImage = "url('back.jpg')"
        console.log("back");
    } else if(cmd_string == "mid") {
        img_cmd.style.backgroundImage = "url('middle.jpg')"
        console.log("middle");
    }

    const div_time = document.querySelector("#time")
    const div_time2 = document.querySelector("#time > h1")

    const date = new Date()
    div_time2.textContent = (date.getHours() + " : " + date.getMinutes() + " : " + date.getSeconds())

    //warning
    const c = div_time.classList
    
     if(num1 < 10 && c.contains("bg-primary")) {
        div_time.classList.toggle("bg-primary")
        div_time.classList.toggle("bg-danger")
     } else if ( num1 >= 10 && c.contains("bg-danger")){
        div_time.classList.toggle("bg-danger")
        div_time.classList.toggle("bg-primary")
     }
    
    console.log(num1)

    
}
setInterval(getStatus, 1000)