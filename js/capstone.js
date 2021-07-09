function buttonClicked(e) {
    e.preventDefault()
    window.model = tf.loadLayersModel(config.model_path)
    console.log("yeah")

}

function registerEventHandler(e) {
    window.document.getElementById("submit").addEventListener("click", function (e) {
        buttonClicked(e)
    })
}

window.document.addEventListener("DOMContentLoaded", registerEventHandler, false);
